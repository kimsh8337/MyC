from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Movie, Rating, Genre
from .forms import RatingForm

# movies = Movie.objects.all()
# Create your views here.
def index(request):
    movies = Movie.objects.order_by('-popularity')
    genres = Genre.objects.all()
    user_selected = []
    user_watched = []
    saved_unseen = []

    if request.user.is_authenticated:
        # 사용자가 찜한 영화
        selected_movies = request.user.selcted_movies.all()
        
        # 찜한 영화 1개 이상이 아니면 보이지 않게

        # 사용자가 본 영화
        
        watched_movies = request.user.watched_movies.all()
        for movie in watched_movies:
            user_watched.append(movie)
        
        # 1. 찜했는데 안본영화 나열
        
        for movie in selected_movies:
            if movie not in watched_movies:
                saved_unseen.append(movie)

        # 2. 찜한 정보를 바탕으로 장르 추천
        user_genres = {}
        for movie in selected_movies:
            user_selected.append(movie)
            tmp = movie.genre_ids.all()
            key = tmp[0].name
            if key not in user_genres:
                user_genres[key] = 1
            else:
                user_genres[key] += 1
        # 모두 15개 영화가 나올때 까지 while 반복
        
        print(user_genres)
        print(user_watched)
        print(user_selected)
        print(saved_unseen)

    # 3. 찜한 목록 중 기준 추천
    context = {
        'movie_top': movies[0],
        'movies_top3': movies[1:4],
        'saved' : saved_unseen,
    }
    return render(request, 'movies/index.html', context)

def genre(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()
    context = {
        'movies': movies,
        'genres': genres,
    }
    return render(request, 'movies/genre.html', context)

def genre_filter(request, genre_pk):
    movies = Movie.objects.values('id').all()
    movies_cnt = len(movies)
    movies_list = [0] * movies_cnt
    genre = get_object_or_404(Genre, pk=genre_pk)
    movie_list = []
    hide_movie = []

    for movie in genre.movie_genres.all():
        movie_list.append(movie.id)

    for i in range(movies_cnt):
        if movies[i]['id'] not in movie_list:
            hide_movie.append(movies[i]['id'])

    context = {
        'hide_cnt': len(hide_movie), 
        'selected_movie': movie_list,
        'hide_movie': hide_movie,

    }
    return JsonResponse(context)

def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    ratings = movie.rating_set.order_by('-pk')
    form = RatingForm()
    context = {
        'movie': movie,
        'ratings': ratings,
        'form': form,
    }
    return render(request, 'movies/movie_detail.html', context)

@require_POST
def rating_create(request, movie_pk):
    if request.user.is_authenticated:
        form = RatingForm(request.POST)
        movie = get_object_or_404(Movie, pk=movie_pk)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.movie = movie 
            rating.save()
            messages.success(request, '의견이 잘 반영되었습니다.')
            return redirect('movies:movie_detail', movie_pk)
    else:
        messages.warning(request, 'Rating 작성을 위해서는 로그인이 필요합니다.')
        return redirect('accounts:login')

@login_required
def rating_update(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, id=rating_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    ratings = movie.rating_set.order_by('-pk')

    if request.user != rating.user:
        messages.warning(request, '본인만 수정이 가능합니다.')
        return redirect('movies:movie_detail', movie_pk)
    
    if request.method =='POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            updated_rating = form.save(commit=False)
            updated_rating.save()
            messages.success(request, '의견이 수정되었습니다.')
            return redirect('movies:movie_detail', movie_pk)
    else:
        form = RatingForm(instance=rating)
    context = {
        'movie': movie,
        'ratings': ratings,
        'form': form,
    }
    return render(request, 'movies/movie_detail.html', context)

@login_required
@require_POST
def rating_delete(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    if request.user == rating.user:
        rating.delete()
    return redirect('movies:movie_detail', movie_pk)

def movie_select(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.selected_users.filter(id=request.user.pk).exists():
        movie.selected_users.remove(request.user)
        select = False
    else:
        movie.selected_users.add(request.user)
        select = True
    context = {
        'select': select,
        'count': movie.selected_users.count()
    }
    return JsonResponse(context)

def movie_watch(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.watched_users.filter(id=request.user.pk).exists():
        movie.watched_users.remove(request.user)
        watch = False
    else:
        movie.watched_users.add(request.user)
        watch = True
    context = {
        'watch': watch,
        'count': movie.watched_users.count()
    }
    return JsonResponse(context)