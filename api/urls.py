from django.urls import path
from . import views  


urlpatterns = [
    path('getAllStudents/', views.getAllStudents, name="get_all_students"),
    path('getAllTeachers/', views.getAllTeachers, name="get_all_teachers"),
    path('getAllSponsors/', views.getAllSponsors, name="get_all_sponsors"),
    path('getAllCourses/', views.getAllCourses, name="get_all_courses"),
    path('createStudent/', views.createStudent, name="post_new_student"),
    path('createTeacher/', views.createTeacher, name="post_new_teacher"),
    path('createSponsor/', views.createSponsor, name="post_new_sponsor"),
    path('createCourse/', views.createCourse, name="post_new_course"),
    path('addCourseToStudent/<str:studentId>;<str:courseId>', views.addCourseToStudent, name="add_course_to_student"),
    path('modifyStudentEval/', views.modifyStudentEval, name="modify_student_eval"),

    path('', views.home_view, name='home'), 
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='pagina_cadastro'),
    path('logout/', views.logout_view, name='logout'),

   
    path("cursos/", views.pagina_cursos_view, name="pagina_cursos"),  # menuCursos.html
    path("curso/", views.cursos_aluno_view, name="curso_aluno"),      # curso.html
    path("adicionar_curso/", views.adicionar_curso_aluno, name="adicionar_curso_aluno"),
    
    path('painel/professor/', views.area_professor_view, name='area_professor'),
    path('painel/aluno/', views.area_aluno_view, name='area_aluno'),
  
    path('desempenho/', views.desempenho_view, name='pagina_desempenho'),


    path('meus-dados/', views.dados_pessoais_view, name='meus_dados_pessoais'),

    path('presenca-eventos/', views.presenca_eventos_view, name='pagina_presenca_eventos'),


    path('professor/aluno/<int:aluno_id>/desempenho/', views.editar_desempenho_aluno_view, name='editar_desempenho_aluno'),
    path('professor/aluno/<int:aluno_id>/presenca-eventos/', views.editar_calendario_aluno_view, name='editar_calendario_aluno'),

    path('aluno/salvar-justificativas/', views.salvar_justificativas_aluno_view, name='salvar_justificativas_aluno'),

    path('duvidas/', views.duvidas, name='pagina_duvidas'),

    
]   