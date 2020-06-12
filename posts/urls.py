from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:movie_pk>/create/', views.post_create, name='post_create'),
    path('<int:post_pk>/', views.post_detail, name='post_detail'),
    path('<int:post_pk>/update/', views.post_update, name='post_update'),
    path('<int:post_pk>/delete/', views.post_delete, name='post_delete'),

    path('<int:post_pk>/comments', views.comments, name='comments'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete',views.comments_delete, name='comments_delete'),
    path('<int:post_pk>/like/', views.like, name = 'like'),
]
