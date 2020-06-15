from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST

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
            messages.success(request, '회원가입이 완료되었습니다. 로그인이 가능합니다.')
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
    context = {
        'user':user
    }
    return render(request, 'accounts/profile.html', context)

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