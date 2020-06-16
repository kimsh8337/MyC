from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Count

from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, '이미 로그인이 되어있음.')
        return redirect('movies:index')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, f'{request.user.username}님 환영!')
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def signup(request):
    if request.user.is_authenticated:
        messages.warning(request, '이미 로그인이 되어있음. 회원가입 하려면 로그아웃해햐 합니다.')
        return redirect('movies:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            # messages.success(request, '회원가입이 완료되었습니다. 로그인이 가능합니다.')
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, '로그아웃!')
    return redirect('movies:index')

def profile(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
<<<<<<< HEAD
    context = {
        'user':user
    }
    return render(request, 'accounts/profile.html', context)
=======
    posts = user.post_set.all()
    saved = user.selcted_movies.all()
    watched = user.watched_movies.all()

    context = {
        'user':user,
        'post_cnt': len(posts),
        'posts': posts,
        'saved_cnt': len(saved),
        'saved': saved,
        'watched_cnt': len(watched),
        'watched': watched,
        }
    return render(request, 'accounts/profile.html', context)

def saved(requset, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    saved = user.selcted_movies.all()
    watched = user.watched_movies.all()
    movie_titles = []
    watched_list = []

    for movie in saved:
        movie_titles.append(movie.id)


    context = {
        'movie_titles': movie_titles,
    }
    
    return JsonResponse(context)

def watched(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    watched = user.watched_movies.all()

    return JsonResponse(context)

>>>>>>> 3529c33202d5832a7815dd47001c5b587cd8580b

def follow(request, user_id):
    if not request.user.is_authenticated:
        messages.warning(request, '로그인해야함!')
        return redirect('accounts:profile', user_id)
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    if user != request.user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
    return redirect('accounts:profile', user.pk)