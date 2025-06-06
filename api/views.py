# Bibliotecas padrão
import json

# Django - Core
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
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
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def createTeacher(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    serializer = TeacherSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def createSponsor(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    serializer = SponsorSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def createCourse(request):
    if request.method != "POST":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    serializer = CourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(status.HTTP_201_CREATED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
    
@api_view(["PUT"])
def addCourseToStudent(request, studentId, courseId):
    if request.method != "PUT":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    student = Student.objects.get(userId = studentId)

    serializer = StudentSerializer(student)

    studentData = serializer.data
    studentData.coursesRegistred = studentData.coursesRegistred + "|" + courseId
    studentData.coursesEval = studentData.couseresEval + "|" + "5"

    newSerializer = StudentSerializer(data = studentData)
    if newSerializer.is_valid():
        newSerializer.save()
        return Response(status.HTTP_202_ACCEPTED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
    

@api_view(["PUT"])
def modifyStudentEval(request, studentId, courseId, newEval):
    if request.method != "PUT":
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)
    
    student = Student.objects.first(id = studentId)

    serializer = StudentSerializer(student)

    studentData = serializer.data
    
    studentCourses = studentData.coursesReg
    studentEval = studentData.coursesEval

    coursesStr = studentCourses.split("|")
    evalStr = studentEval.split("|")
    newEvalStr = ""

    for i in range(len(coursesStr)):
        if coursesStr[i] == courseId:
            evalStr[i] = newEval
        newEvalStr = newEvalStr + evalStr[i] + "|"
    
    studentData.coursesEval = newEvalStr

    newSerializer = StudentSerializer(data = studentData)
    if newSerializer.is_valid():
        newSerializer.save()
        return Response(status.HTTP_202_ACCEPTED)
    else:
        return Response(status.HTTP_400_BAD_REQUEST)
    

@api_view(["PUT"])
def addMissedClass(request):
    if request.method != "PUT":
        return Response(status.HTTP_501_NOT_IMPLEMENTED)

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
                return redirect('login') # Nome da URL de login
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
@login_required # Garante que apenas o aluno logado veja seu calendário
def presenca_eventos_view(request):
    user = request.user
    dados_json_para_template = "{}" # Default: calendário vazio

    if hasattr(user, 'profile') and user.profile.dados_calendario_json:
        try:

            dados_dict = json.loads(user.profile.dados_calendario_json)
            dados_json_para_template = json.dumps(dados_dict) 
        except (json.JSONDecodeError, TypeError):
            messages.warning(request, "Seus dados de calendário parecem estar corrompidos ou não foram definidos. Exibindo calendário padrão.")

        except AttributeError:

            messages.error(request, "Seu perfil não tem dados de calendário configurados.")
    elif hasattr(user, 'profile'):
        messages.info(request, "Seu calendário de presença ainda não tem marcações.")
    else:
        messages.error(request, "Perfil de usuário não encontrado para carregar o calendário.")
    context = {
        'dados_calendario_do_aluno_json': dados_json_para_template
    }
    return render(request, 'presencaEventos.html', context)

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
    aluno = get_object_or_404(User, pk=aluno_id)
    
    profile = getattr(aluno, 'profile', None)
    if not profile or profile.tipo_usuario != 'aluno':
        messages.error(request, "Usuário inválido ou não é um aluno.")
        return redirect('area_professor') 
    if request.method == 'POST':
        dados_json_recebidos = request.POST.get('dados_calendario')

        if dados_json_recebidos:
            try:
                novos_dados_calendario_dict = json.loads(dados_json_recebidos)
                profile.dados_calendario_json = json.dumps(novos_dados_calendario_dict)
                profile.save()
                
               
                nome_display_aluno = aluno.get_full_name().strip()
                if not nome_display_aluno:
                    nome_display_aluno = aluno.username
                
                messages.success(request, f"Calendário de {nome_display_aluno} atualizado com sucesso!")
                return redirect('editar_calendario_aluno', aluno_id=aluno.id)
            except json.JSONDecodeError:
                messages.error(request, "Erro: Formato de dados do calendário inválido recebido.")
            except Exception as e:
                messages.error(request, f"Erro inesperado ao salvar o calendário: {e}")
                print(f"Erro ao salvar calendário para {aluno.username}: {e}")
        else:
            messages.warning(request, "Nenhum dado de calendário foi recebido para salvar.")

    dados_para_template_dict = {}
    try:
        if profile.dados_calendario_json:
            dados_para_template_dict = json.loads(profile.dados_calendario_json)
    except json.JSONDecodeError:
        messages.warning(request, "Dados de calendário corrompidos. Exibindo calendário vazio.")
    except AttributeError: 
        messages.error(request, "Perfil do aluno não possui campo 'dados_calendario_json'. Verifique modelos e migrações.")

    context = {
        'aluno': aluno,
        'dados_presenca_aluno_json': json.dumps(dados_para_template_dict), 
    } 
    return render(request, 'editar_calendario_aluno.html', context)


    
@login_required 
def salvar_justificativas_aluno_view(request):
    user_profile = getattr(request.user, 'profile', None)

    if not user_profile:
        messages.error(request, "Perfil de usuário não encontrado. Não foi possível salvar as justificativas.")
        return redirect('home') 
    dados_calendario_json_string = request.POST.get('dados_calendario_justificado')

    if dados_calendario_json_string:
        try:
            dados_para_salvar_dict = json.loads(dados_calendario_json_string)
            
            user_profile.dados_calendario_json = json.dumps(dados_para_salvar_dict)
            user_profile.save()
            
            messages.success(request, "Suas alterações no calendário foram salvas com sucesso!")
        except json.JSONDecodeError:
            messages.error(request, "Ocorreu um erro ao processar os dados do calendário. Formato inválido.")
        except Exception as e:
            messages.error(request, f"Ocorreu um erro inesperado ao salvar suas alterações: {e}")
            print(f"Erro ao salvar justificativas para {request.user.username}: {e}") 
    else:
        messages.warning(request, "Nenhum dado de calendário foi enviado para salvar.")


    return redirect('pagina_presenca_eventos') 



    #---------------------
    #ADICIONANDO DUVIDAS
    #--------------------

    #duvidas


from .models import Duvida

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser



from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse

@login_required
def duvidas(request):
    aba = request.GET.get('aba', 'Geral')
    duvidas = Duvida.objects.none()

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        texto = request.POST.get('texto')
        destinatario_form = request.POST.get('destinatario') 
        
        remetente_obj = request.user 

        if request.user.get_full_name():
            nome_remetente = request.user.get_full_name()
        else:
            nome_remetente = request.user.username
        
        if titulo and texto and destinatario_form:
            Duvida.objects.create(
                titulo=titulo,
                texto=texto,
                nome=nome_remetente,
                destinatario=destinatario_form, 
                remetente=remetente_obj 
            )
            return redirect(f"{reverse('pagina_duvidas')}?aba=Envios") 
    
    if aba == 'Envios':
        duvidas = Duvida.objects.filter(remetente=request.user).order_by('-data')
    elif aba == 'Geral':
        duvidas = Duvida.objects.filter(destinatario='Geral').order_by('-data')
    elif aba == 'Professor':
        duvidas = Duvida.objects.filter(destinatario__in=['Geral', 'Professor']).order_by('-data')
    elif aba == 'Administrador':
        duvidas = Duvida.objects.filter(destinatario__in=['Geral', 'Administrador']).order_by('-data')
    else:
        duvidas = Duvida.objects.none()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {'duvidas': duvidas}
        html_list = render_to_string('duvidas_list_partial.html', context, request=request)
        return HttpResponse(html_list)
    else:
        context = {
            'duvidas': duvidas,
            'aba_selecionada': aba, 
        }
        return render(request, 'duvidas.html', context)

#cadastrar evento
@login_required
def cadastrar_evento(request):
    if request.method == 'POST':
        data = request.POST.get('data_evento')
        descricao = request.POST.get('descricao_evento')

        Evento.objects.create(data=data, descricao=descricao)

        messages.success(request, 'Evento cadastrado com sucesso!')
        return redirect('pagina_professor')  # ou onde você quiser

    return render(request, 'pagina_professor.html')



#add curso

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def pagina_cursos_view(request):
    cursos_disponiveis = {
        "1": "Atividade 1",
        "2": "Atividade 2",
        "3": "Atividade 3",
        "4": "Atividade 4"
    }
    return render(request, "menuCursos.html", {"cursos": cursos_disponiveis})


# Página que exibe os cursos adicionados - curso.html
def cursos_aluno_view(request):
    cursos_ids = request.session.get("cursos_aluno", [])

    cursos_disponiveis = {
        "1": "Atividade 1",
        "2": "Atividade 2",
        "3": "Atividade 3",
        "4": "Atividade 4"
    }

    cursos_adicionados = [cursos_disponiveis[cid] for cid in cursos_ids if cid in cursos_disponiveis]

    return render(request, "curso.html", {"cursos": cursos_adicionados})


# View para adicionar cursos à sessão
@csrf_exempt
def adicionar_curso_aluno(request):
    if request.method == "POST":
        data = json.loads(request.body)
        curso_id = data.get("curso_id")

        if not curso_id:
            return JsonResponse({"status": "invalid data"}, status=400)

        cursos_salvos = request.session.get("cursos_aluno", [])

        if curso_id not in cursos_salvos:
            cursos_salvos.append(curso_id)
            request.session["cursos_aluno"] = cursos_salvos

        return JsonResponse({"status": "ok", "cursos": cursos_salvos})

    return JsonResponse({"status": "error"}, status=400)

@login_required
@professor_required
def novo_curso(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        descricao = request.POST.get('descricao', '').strip()

        if not nome or not descricao:
            messages.error(request, "Todos os campos são obrigatórios.")
        else:
            try:
                Course.objects.create(nome=nome, descricao=descricao)
                messages.success(request, "Curso criado com sucesso!")
                return redirect('pagina_cursos')  # ou onde quiser redirecionar
            except Exception as e:
                messages.error(request, f"Erro ao criar curso: {e}")

    return render(request, 'novo_curso.html')