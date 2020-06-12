from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('<int:movie_pk>/create/',views.post_create, name='post_create'),
    path('<int:post_pk>/',views.post_detail, name='post_detail'),
]