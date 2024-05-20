# dietitian/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_dietitian, name='register_dietitian'),
    path('login/', views.login_dietitian, name='login'),
    path('logout/', views.logout_dietitian, name='logout'),
    path('add_practice_location/', views.add_practice_location, name='add_practice_location'),
    path('list_dietitians/', views.list_dietitians, name='list_dietitians'),
    path('edit_practice_location/<int:pk>/', views.edit_practice_location, name='edit_practice_location'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_practice_location/<int:pk>/', views.delete_practice_location, name='delete_practice_location'),
    path('list_practice_locations/', views.list_practice_locations, name='list_practice_locations'),




]
