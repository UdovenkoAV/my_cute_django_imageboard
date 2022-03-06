from .models import PostA, PostB
from .forms import APostForm, BPostForm, ANewThreadForm, BNewThreadForm


class BoardSettings:
    name = 'board'
    slug = 'board'
    model = ''
    post_form = ''
    new_thread_form = ''
    threads_in_page = 10
    default_username = 'Anonymous'
    bump_limit = 500


class ABoardSettings(BoardSettings):
    name = 'Anime'
    slug = 'a'
    model = PostA
    post_form = APostForm
    new_thread_form = ANewThreadForm


class BBoardSettings(BoardSettings):
    name = 'Random'
    slug = 'b'
    model = PostB
    post_form = BPostForm
    new_thread_form = BNewThreadForm


boards = {
    'a': ABoardSettings,
    'b': BBoardSettings,
}
