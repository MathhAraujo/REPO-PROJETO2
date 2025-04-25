from django.contrib import admin
from django.urls import path, include
from . import views
from .views import home_view
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('getAllStudents/', views.getAllStudents, name="get_all_students"),
    path('getAllTeachers/', views.getAllTeachers, name="get_all_teachers"),
    path('getAllSponsors/', views.getAllSponsors, name="get_all_sponsors"),
    path('createStudent/', views.createStudent, name="post_new_student"),
    path('createTeacher/', views.createTeacher, name="post_new_teacher"),
    path('createSponsor/', views.createSponsor, name="post_new_sponsor"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('aluno/', TemplateView.as_view(template_name='aluno.html'), name='area_aluno'),
    path('desempenho/', views.desempenho_view, name='pagina_desempenho'),
    path('cadastro/', views.cadastro_view, name='pagina_cadastro'),
]