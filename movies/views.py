from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Movie, Rating
from .forms import RatingForm

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)

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
            return redirect('movies:movie_detail', movie_pk)
    else:
        messages.warning(request, 'Rating 작성을 위해서는 로그인이 필요합니다.')
        return redirect('accounts:login')

@login_required
def rating_update(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, id=rating_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.user != rating.user:
        messages.warning(request, '작성자가 아니면 수정할 수 없습니다.')
        return redirect('movies:movie_detail', movie_pk)
    if request.method =='POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            updated_rating = form.save(commit=False)
            updated_rating.user = request.user
            updated_rating.movie = movie
            updated_rating.save()
            messages.success(request, 'Rating 수정이 완료되었습니다!')
            return redirect('movies:movie_detail', movie_pk)
    else:
        form = RatingForm(instance=rating)
    context={
        'form': form,
        'movie': movie,
    }
    return render(request, 'movies/movie_detail.html', context)


@login_required
@require_POST
def rating_delete(request, movie_pk, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    if request.user == rating.user:
        rating.delete()
    return redirect('movies:movie_detail', movie_pk)
