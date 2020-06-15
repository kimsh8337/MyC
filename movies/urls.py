from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.index, name='index'),
    # movie
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/selected/', views.movie_select, name='movie_select'),
    path('<int:movie_pk>/watched/', views.movie_watch, name='movie_watch'),
    path('genre/', views.genre, name='genre'),
    path('genre/<int:genre_pk>/', views.genre_filter, name='genre_filter'),
    # rating
    path('<int:movie_pk>/rating_create/', views.rating_create, name='rating_create'),
    path('<int:movie_pk>/rating_delete/<int:rating_pk>/', views.rating_delete, name='rating_delete'),
    path('<int:movie_pk>/rating_update/<int:rating_pk>/', views.rating_update, name='rating_update'),
]
