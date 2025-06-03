from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import login_view, cadastro_view, logout_view


urlpatterns = [
    path('getAllStudents/', views.getAllStudents, name="get_all_students"),
    path('getAllTeachers/', views.getAllTeachers, name="get_all_teachers"),
    path('getAllSponsors/', views.getAllSponsors, name="get_all_sponsors"),
    path('getAllCourses/', views.getAllCourses, name="get_all_courses"),
    path('createStudent/', views.createStudent, name="post_new_student"),
    path('createTeacher/', views.createTeacher, name="post_new_teacher"),
    path('createSponsor/', views.createSponsor, name="post_new_sponsor"),
    path('createCourse/', views.createCourse, name="post_new_course"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('aluno/', TemplateView.as_view(template_name='aluno.html'), name='area_aluno'),
    path('desempenho/', views.desempenho_view, name='pagina_desempenho'),
    path('cadastro/', views.cadastro_view, name='pagina_cadastro'),
    path('menuCursos/', views.menucursos_view, name='pagina_menucursos'),
    path('cursos/', views.cursos_view, name='pagina_cursos'),
    path('login/', login_view, name='login'),
    path('cadastro/', cadastro_view, name='pagina_cadastro'),
    path('logout/', logout_view, name='logout'),

]