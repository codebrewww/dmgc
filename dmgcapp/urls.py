from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('foodlist/<int:today_string>', views.foodlist, name='foodlist'),
    path('profile', views.profile, name='profile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
]