from django import forms
from .models import Post, PostA, PostB


class PostForm(forms.ModelForm):
    email = forms.CharField(required=False)
    file = forms.FileField(required=False)
    title = forms.CharField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'username', 'email', 'file', 'body')
        labels = {'body': 'Message'}


class APostForm(PostForm):

    class Meta:
        model = PostA
        fields = ('title', 'username', 'email', 'file', 'body')
        labels = {'body': 'Message'}


class ANewThreadForm(APostForm):
    file = forms.FileField(required=True)


class BPostForm(PostForm):

    class Meta:
        model = PostB
        fields = ('title', 'username', 'email', 'file', 'body')
        labels = {'body': 'Message'}


class BNewThreadForm(BPostForm):
    file = forms.FileField(required=True)