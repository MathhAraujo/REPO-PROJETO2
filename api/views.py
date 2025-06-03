from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import json
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email 
from django.core.exceptions import ValidationError as DjangoValidationError 


User = get_user_model()


# Create your views here.

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
    
@api_view(["POST"])
def createTeacher(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    serializer = TeacherSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)

@api_view(["POST"])
def createSponsor(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    serializer = SponsorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    
@api_view(["POST"])
def createCourse(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)

@api_view(["PUT"])
def addMissedClass(request):
    if request.method != "PUT":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
def home_view(request):
    return render(request, 'home.html')

def desempenho_view(request):
    return render(request, 'desempenho.html')


def cadastro_view(request):



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
            erro_para_template = 'Por favor, selecione um tipo de usuário válido (Aluno ou Professor).'

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
                

                print(f"Ação necessária: Salvar tipo '{tipo_usuario}' para o usuário '{user.username}' no seu model Profile/CustomUser.")

                login(request, user) 
                messages.success(request, f'Bem-vindo(a), {user.first_name or user.username}! Seu cadastro foi realizado com sucesso e você já está logado.')
                return redirect('home') 

            except Exception as e:
              
                print(f"Erro ao criar usuário: {e}") 
                erro_para_template = 'Ocorreu um erro inesperado ao tentar criar sua conta. Por favor, tente novamente.'
                messages.error(request, erro_para_template)
                return render(request, 'cadastro.html', {'erro': erro_para_template, 'form_data': form_data})

    return render(request, 'cadastro.html', {'form_data': form_data if request.method == 'POST' else {}})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos.'})

    return render(request, 'login.html')

    
def logout_view(request):
    logout(request)
    return redirect('login')

def menucursos_view(request):
    return render(request, 'menuCursos.html')

def cursos_view(request):
    return render(request, 'curso.html')

