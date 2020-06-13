from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

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

@login_required
def post_update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user == post.user:
        if request.method =='POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('posts:post_detail', post.pk)
        else:
            form = PostForm(instance=post)
        context = {
            'form':form
        }
        return render(request, 'posts/form.html', context)
    else:
        return redirect('posts:post_list')

@login_required
def post_delete(request,post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user == post.user:
        post.delete()
    return redirect('posts:post_list')

@login_required
def comments(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post.pk)

@require_POST
@login_required
def comments_delete(request, post_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('posts:post_detail', post_pk)


@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.like_users.filter(id=request.user.pk).exists():
        post.like_users.remove(request.user)
        liked = False
    else:
        post.like_users.add(request.user)
        liked = True
    context = {
        'liked': liked,
        'count': post.like_users.count(),
    }
    return JsonResponse(context)