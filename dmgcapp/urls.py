from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('search/<int:today_string>', views.search, name='search'),
    path('profile', views.profile, name='profile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('calculator/<int:today_string>', views.calculator, name='calculator'),
    # path('summary', views.)
]