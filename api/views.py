from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse 
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Teacher, Sponsor, Course 
from .serializers import StudentSerializer, TeacherSerializer, SponsorSerializer, CourseSerializer 
import json 

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import get_user_model 
from django.contrib import messages
from django.core.validators import validate_email 
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.decorators import login_required 

from .forms import EditarDadosPessoaisForm 
from django.contrib.auth import get_user_model


User = get_user_model() 


@api_view(["GET"])
def getAllStudents(request):
    if request.method != "GET":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def getAllTeachers(request):
    if request.method != "GET":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def getAllSponsors(request):
    if request.method != "GET":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    sponsor = Sponsor.objects.all()
    serializer = SponsorSerializer(sponsor, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def getAllCourses(request):
    if request.method != "GET":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    course = Course.objects.all()
    serializer = CourseSerializer(course, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["POST"])
def createStudent(request): 
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST) # Retornar erros de validação

@api_view(["POST"])
def createTeacher(request): 
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def createSponsor(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = SponsorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def createCourse(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"]) 
def addMissedClass(request):
    if request.method != "PUT":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)

    return Response({"message": "Função addMissedClass não implementada"}, status.HTTP_501_NOT_IMPLEMENTED)



def home_view(request):
 
    return render(request, 'home.html') 

def desempenho_view(request):
  
    return render(request, 'desempenho.html')

def pagina_cursos_view(request): 
    cursos = Course.objects.all()
    return render(request, 'menuCursos.html', {'cursos': cursos})

def curso_detalhe_view(request, curso_id): 

    return render(request, 'curso.html') 

def cadastro_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Você já está logado.")
        return redirect('home')

    form_data = {} 
    erro_para_template = None 

    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '') 
        confirmarsenha = request.POST.get('confirmarsenha', '')
        tipo_usuario = request.POST.get('tipo_usuario', '') 

        form_data = request.POST 

        if not all([nome, email, senha, confirmarsenha, tipo_usuario]):
            erro_para_template = 'Todos os campos são obrigatórios.'
        elif not erro_para_template:
            try:
                validate_email(email)
            except DjangoValidationError:
                erro_para_template = 'O formato do email é inválido.'
        elif not erro_para_template and senha != confirmarsenha:
            erro_para_template = 'As senhas não coincidem.'
        elif not erro_para_template and len(senha) < 8: 
            erro_para_template = 'A senha deve ter pelo menos 8 caracteres.'
        elif not erro_para_template and tipo_usuario not in ['aluno', 'professor']:
            # Adicione outros tipos válidos se houver (ex: 'admin', 'sponsor')
            erro_para_template = 'Por favor, selecione um tipo de usuário válido.'
        elif not erro_para_template:
            if User.objects.filter(username=email).exists():
                erro_para_template = 'Este email já está cadastrado como nome de usuário.'
            elif User.objects.filter(email=email).exists(): 
                erro_para_template = 'Este email já está cadastrado.'
        
        if erro_para_template:
            messages.error(request, erro_para_template) 
            return render(request, 'cadastro.html', {'erro': erro_para_template, 'form_data': form_data})
        else:
            try:
                partes_nome = nome.split(' ', 1)
                first_name = partes_nome[0]
                last_name = partes_nome[1] if len(partes_nome) > 1 else ''

                user = User.objects.create_user(
                    username=email, 
                    email=email,
                    password=senha,
                    first_name=first_name,
                    last_name=last_name
                )
                
          
                if hasattr(user, 'profile'):
                    user.profile.tipo_usuario = tipo_usuario
                    user.profile.save()
                else:

                    Profile.objects.create(user=user, tipo_usuario=tipo_usuario)
                
           

                messages.success(request, 'Cadastro realizado com sucesso! Por favor, faça o login.')
                return redirect('login') # Nome da sua URL de login

            except Exception as e:
                print(f"Erro ao criar usuário ou perfil: {e}") 
                erro_para_template = 'Ocorreu um erro ao criar sua conta. Tente novamente.'
                messages.error(request, erro_para_template)
                return render(request, 'cadastro.html', {'erro': erro_para_template, 'form_data': form_data})

    return render(request, 'cadastro.html', {'form_data': form_data if request.method == 'POST' else {}})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home') 

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                messages.success(request, f"Bem-vindo(a) de volta, {user.first_name or user.username}!")
                next_url = request.GET.get('next') 
                if next_url:
                    return redirect(next_url)
                return redirect('home') 
            else:
                messages.error(request, "Email (nome de usuário) ou senha inválidos.")
        else:
            messages.error(request, "Verifique os dados inseridos.")
    else:
        form = AuthenticationForm()
    

    return render(request, 'login.html', {'form': form}) 


@login_required
def logout_view(request):

    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('home') 


@login_required
def area_aluno_view(request):
    return render(request, 'aluno.html') 

@login_required
def area_professor_view(request):
  
    return render(request, 'professor.html') 



@login_required
def area_aluno_view(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.tipo_usuario != 'aluno':
        messages.error(request, "Acesso não autorizado à área do aluno.")
        return redirect('home')
    # Adicione contexto específico para alunos se necessário
    return render(request, 'aluno.html') # Crie este template

@login_required
def area_professor_view(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.tipo_usuario != 'professor':
        messages.error(request, "Acesso não autorizado à área do professor.")
        return redirect('home') 

    return render(request, 'professor.html')



@login_required
def dados_pessoais_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditarDadosPessoaisForm(request.POST, user=user)
        if form.is_valid():
            email_alterado = False
            senha_alterada = False

            novo_email = form.cleaned_data.get('email').lower()
            if novo_email and novo_email != user.email.lower():
              
                if hasattr(user, 'username') and user.username == user.email:
                    user.username = novo_email
                user.email = novo_email
                email_alterado = True
            
      
            nova_senha1 = form.cleaned_data.get('nova_senha1')
            if nova_senha1:
                user.set_password(nova_senha1)
                senha_alterada = True
            
            if email_alterado or senha_alterada:
                user.save()
                if senha_alterada:

                    update_session_auth_hash(request, user)
                messages.success(request, 'Seus dados foram atualizados com sucesso!')
            else:
                messages.info(request, 'Nenhuma alteração foi detectada nos seus dados.')
            
            return redirect('meus_dados_pessoais') 
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
          
            
    else:
        form = EditarDadosPessoaisForm(user=user, initial={'email': user.email})

    context = {
        'form': form,
        
    }
    return render(request, 'dados_pessoais.html', context)


@login_required 
def presenca_eventos_view(request):
   
    context = {}
    return render(request, 'presencaEventos.html', context)