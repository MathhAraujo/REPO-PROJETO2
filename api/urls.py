from django.contrib import admin
from django.urls import path, include
from . import views
from .views import home_view
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('getAll/', views.get_users, name="get_all_users"),
    path('postUser/', views.postUser, name="post_new_user"),
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]




