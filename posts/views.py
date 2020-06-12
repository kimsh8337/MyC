from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from movies.models import Movie
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
    posts = Post.objects.order_by('-pk')
    context = {
        'posts':posts
    }
    return render(request, 'posts/post_list.html', context)

@login_required
def post_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.movie = movie
            post.save()
            return redirect('posts:post_detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'posts/form.html' ,context)


def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm()
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'posts/post_detail.html', context)