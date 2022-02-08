from .models import PostA, PostB
from .forms import APostForm, BPostForm, ANewThreadForm, BNewThreadForm


class DefaultConfig:
    name = 'board'
    slug = 'board'
    model = ''
    post_form = ''
    new_thread_form = ''
    threads_in_page = 10
    default_username = 'Anonymous'
    bump_limit = 500


class ABoardConfig(DefaultConfig):
    name = 'Anime'
    slug = 'a'
    model = PostA
    post_form = APostForm
    new_thread_form = ANewThreadForm


class BBoardConfig(DefaultConfig):
    name = 'Random'
    slug = 'b'
    model = PostB
    post_form = BPostForm
    new_thread_form = BNewThreadForm


boards = {
    'a': ABoardConfig,
    'b': BBoardConfig,
}
