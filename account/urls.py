from django.urls import path
from . import views


urlpatterns = [
    path('register', views.register, name='register'),
    path('user/profile/<str:username>', views.profile, name='profile'),
    path('settings', views.edit_profile, name='edit_profile'),
    path('cancel-profile-update/', views.cancel_profile_update, name='cancel_profile_update'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    
]
