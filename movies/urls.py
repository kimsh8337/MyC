from django.urls import path
from . import views

app_name='movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/rating_create/', views.rating_create, name='rating_create'),
    path('<int:movie_pk>/<int:rating_pk>/rating_delete/', views.rating_delete, name='rating_delete'),
    path('<int:movie_pk>/<int:rating_pk>/rating_update/', views.rating_update, name='rating_update'),
]