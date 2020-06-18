from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

from movies.models import Movie
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
    
    if request.user.is_authenticated:
        posts = Post.objects.order_by('-pk')

        context = {
            'posts':posts
        }
        return render(request, 'posts/post_list.html', context)
    else:
        messages.info(request, '로그인이 필요한 기능입니다.')
        return redirect('movies:index')

@login_required
def post_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.movie = movie
                post.save()
                messages.success(request, '포스트가 작성되었습니다.')
                return redirect('posts:post_detail', post.pk)
        else:
            form = PostForm()
        context = {
            'form' : form
        }
        return render(request, 'posts/form.html' ,context)
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect(request, 'movies:index')



def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user.is_authenticated:
        form = CommentForm()
        context = {
            'post' : post,
            'form' : form,
        }
        return render(request, 'posts/post_detail.html', context)
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect(request, 'movies:index')

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
                messages.success(request, '포스트가 수정되었습니다.')
                return redirect('posts:post_detail', post.pk)
        else:
            form = PostForm(instance=post)
        context = {
            'form':form
        }
        return render(request, 'posts/form.html', context)
    else:
        messages.error(request, '본인만 수정이 가능합니다.')
        return redirect('posts:post_list')

@login_required
def post_delete(request,post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user == post.user:
        post.delete()
        messages.success(request, '포스트가 삭제되었습니다.')
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect('posts:post_list')

@login_required
def comments(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if request.user.is_authenticated:
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            messages.success(request, '댓글이 작성되었습니다.')
    else:
        messages.error(request, '권한이 없습니다.')
    return redirect('posts:post_detail', post.pk)

@require_POST
@login_required
def comments_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
    else:
        messages.error(request, '본인만 삭제가 가능합니다.')
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