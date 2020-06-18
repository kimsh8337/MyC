from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('<int:user_id>/profile/', views.profile, name='profile'),
    path('<int:user_id>/settings/', views.settings, name='settings'),
    # path('<int:user_id>/profile/saved/', views.saved, name='saved'),
    # path('<int:user_id>/profile/watched/', views.watched, name='watched'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
]