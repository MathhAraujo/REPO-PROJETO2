# Bibliotecas padrão
import json

# Django - Core
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

# Django - Autenticação
from django.contrib.auth import login, authenticate, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Modelos e Serializers
from .models import User, Student, Teacher, Sponsor, Course, Profile, Materia, DesempenhoMateria
from .serializers import StudentSerializer, TeacherSerializer, SponsorSerializer, CourseSerializer

# Forms
from .forms import EditarDadosPessoaisForm, DesempenhoMateriaFormSet

User = get_user_model()

# API Views
@api_view(["GET"])
def getAllStudents(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def getAllTeachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def getAllSponsors(request):
    sponsors = Sponsor.objects.all()
    serializer = SponsorSerializer(sponsors, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["GET"])
def getAllCourses(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

@api_view(["POST"])
def createStudent(request): 
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def createTeacher(request): 
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def createSponsor(request):
    serializer = SponsorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def createCourse(request):
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def addMissedClass(request):
    return Response({"message": "Função addMissedClass não implementada"}, status.HTTP_501_NOT_IMPLEMENTED)

# Views públicas
def home_view(request):
    return render(request, 'home.html')

def desempenho_view(request):
    return render(request, 'desempenho.html')

def pagina_cursos_view(request): 
    cursos = Course.objects.all()
    return render(request, 'menuCursos.html', {'cursos': cursos})

def curso_detalhe_view(request, curso_id): 
    return render(request, 'curso.html')

# Cadastro e autenticação
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
        elif senha != confirmarsenha:
            erro_para_template = 'As senhas não coincidem.'
        elif len(senha) < 8:
            erro_para_template = 'A senha deve ter pelo menos 8 caracteres.'
        elif tipo_usuario not in ['aluno', 'professor']:
            erro_para_template = 'Tipo de usuário inválido.'
        else:
            try:
                validate_email(email)
                if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
                    erro_para_template = 'Email já cadastrado.'
            except DjangoValidationError:
                erro_para_template = 'Email inválido.'

        if erro_para_template:
            messages.error(request, erro_para_template) 
            return render(request, 'cadastro.html', {'erro': erro_para_template, 'form_data': form_data})

        try:
            first_name, *rest = nome.split(' ', 1)
            last_name = rest[0] if rest else ''
            user = User.objects.create_user(username=email, email=email, password=senha, first_name=first_name, last_name=last_name)
            Profile.objects.create(user=user, tipo_usuario=tipo_usuario)
            messages.success(request, 'Cadastro realizado com sucesso! Faça o login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {e}')
            return render(request, 'cadastro.html', {'erro': 'Erro ao criar conta.', 'form_data': form_data})

    return render(request, 'cadastro.html', {'form_data': form_data})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, f"Bem-vindo(a) {user.first_name or user.username}!")
                return redirect(request.GET.get('next') or 'home')
            messages.error(request, "Credenciais inválidas.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Você foi desconectado com sucesso.")
    return redirect('home')

# Áreas privadas
@login_required
def area_aluno_view(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.tipo_usuario != 'aluno':
        messages.error(request, "Acesso não autorizado.")
        return redirect('home')
    return render(request, 'aluno.html')

@login_required
def area_professor_view(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.tipo_usuario != 'professor':
        messages.error(request, "Acesso não autorizado.")
        return redirect('home')
    alunos_users = User.objects.filter(profile__tipo_usuario='aluno').select_related('profile')
    return render(request, 'professor.html', {'alunos': alunos_users})

# Dados pessoais
@login_required
def dados_pessoais_view(request):
    user = request.user
    if request.method == 'POST':
        form = EditarDadosPessoaisForm(request.POST, user=user)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            nova_senha = form.cleaned_data.get('nova_senha1')

            if email and email != user.email:
                user.email = email
                if user.username == user.email:
                    user.username = email

            if nova_senha:
                user.set_password(nova_senha)

            user.save()
            if nova_senha:
                update_session_auth_hash(request, user)

            messages.success(request, 'Dados atualizados com sucesso.')
            return redirect('meus_dados_pessoais')
        messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = EditarDadosPessoaisForm(user=user, initial={'email': user.email})

    return render(request, 'dados_pessoais.html', {'form': form})

# Presença
@login_required 
def presenca_eventos_view(request):
    return render(request, 'presencaEventos.html')

# Professor - desempenho e calendário
def professor_required(function):
    return user_passes_test(
        lambda u: u.is_authenticated and hasattr(u, 'profile') and u.profile.tipo_usuario == 'professor',
        login_url='pagina_login'
    )(function)

@login_required
@professor_required
def editar_desempenho_aluno_view(request, aluno_id):
    aluno = get_object_or_404(User, pk=aluno_id, profile__tipo_usuario='aluno')
    for materia in Materia.objects.all():
        DesempenhoMateria.objects.get_or_create(aluno=aluno, materia=materia)

    if request.method == 'POST':
        formset = DesempenhoMateriaFormSet(request.POST, queryset=DesempenhoMateria.objects.filter(aluno=aluno))
        if formset.is_valid():
            formset.save()
            messages.success(request, f"Desempenho de {aluno.get_full_name()} atualizado!")
            return redirect('area_professor')
    else:
        formset = DesempenhoMateriaFormSet(queryset=DesempenhoMateria.objects.filter(aluno=aluno))

    return render(request, 'editar_desempenho_aluno.html', {'aluno': aluno, 'desempenho_formset': formset})

@login_required
@professor_required
def editar_calendario_aluno_view(request, aluno_id):
    aluno = get_object_or_404(User, pk=aluno_id, profile__tipo_usuario='aluno')
    profile = aluno.profile

    if request.method == 'POST':
        dados = request.POST.get('dados_calendario')
        if dados:
            try:
                profile.dados_calendario_json = json.dumps(json.loads(dados))
                profile.save()
                messages.success(request, "Calendário atualizado!")
                return redirect('editar_calendario_aluno', aluno_id=aluno_id)
            except Exception as e:
                messages.error(request, f"Erro: {e}")

    try:
        dados_presenca = json.loads(profile.dados_calendario_json or '{}')
    except json.JSONDecodeError:
        dados_presenca = {}

    return render(request, 'editar_calendario_aluno.html', {
        'aluno': aluno,
        'dados_presenca_aluno_json': json.dumps(dados_presenca)
    })
