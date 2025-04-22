from django.contrib import admin
from django.urls import path, include
from . import views
from .views import home_view

urlpatterns = [
    path('getAll/', views.get_users, name="get_all_users"),
    path('postUser/', views.postUser, name="post_new_user"),
    path('', home_view, name='home'),
]




