from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_id>/profile', views.profile, name='profile'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
]