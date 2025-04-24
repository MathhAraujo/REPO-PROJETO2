"""
URL configuration for api_root project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from api import views
from api.views import home_view
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
<<<<<<< Updated upstream
    path('admin/', admin.site.urls),
    path("v1/", include("api.urls"), name="api_urls"),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
=======

    path("api/", include("api.urls"), name="api_urls"),
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('aluno/', TemplateView.as_view(template_name='aluno.html'), name='area_aluno'),
    path('desempenho/', views.desempenho_view, name='pagina_desempenho')
>>>>>>> Stashed changes
]




   