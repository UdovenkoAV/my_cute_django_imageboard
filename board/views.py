from django.shortcuts import render, get_object_or_404, redirect
from .board_conf import boards
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .apps import BoardConfig
from django.http import Http404


def index(request):
    boards_cfg = boards.items()
    print(boards_cfg)
    return render(request, 'index.html', {'boards_cfg': boards_cfg})


def thread_list(request, board_slug):
    if board_slug not in boards.keys():
        raise Http404

    if request.method == 'POST':
        form = boards[board_slug].new_thread_form(request.POST, request.FILES)

        if form.is_valid():
            new_post(form.save(commit=False), is_oppost=True)
            return redirect('/{}/'.format(board_slug))

    else:
        form = boards[board_slug].new_thread_form(initial={"username": boards[board_slug].default_username})

    object_list = boards[board_slug].model.oppost_manager.all().order_by("-updated")
    paginator = Paginator(object_list, boards[board_slug].threads_in_page)
    page = request.GET.get('page')
    try:
        opposts = paginator.page(page)
    except PageNotAnInteger:
        opposts = paginator.page(1)
    except EmptyPage:
        opposts = paginator.page(paginator.num_pages)
    threads_dic = {oppost: oppost.posts.all().order_by('-id') for oppost in opposts}

    return render(request, 'list.html', {'threads_dic': threads_dic, 'form': form, 'page': page,
                                         'opposts': opposts, 'board_conf': boards[board_slug]})


def thread_detail(request, board_slug, id):
    if board_slug not in boards.keys():
        raise Http404
    oppost = get_object_or_404(boards[board_slug].model, id=id)
    posts = oppost.posts.all()
    if request.method == 'POST':
        form = boards[board_slug].post_form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            new_post(post, oppost=oppost)
            if len(posts) < boards[board_slug].bump_limit and post.email != 'sage':
                oppost.updated = datetime.now()
                oppost.save()
            return redirect(oppost.get_absolute_url())
    else:
        form = boards[board_slug].post_form(initial={"username": boards[board_slug].default_username})

    return render(request, 'detail.html', {'oppost': oppost, 'posts': posts, 'form': form,
                                           'board_conf': boards[board_slug]})


def new_post(post, oppost=None, is_oppost=False):
    post.oppost = oppost
    post.is_oppost = is_oppost
    post.save()
