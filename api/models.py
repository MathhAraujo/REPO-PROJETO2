from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


# MODELOS DE USUÁRIO (Abstrato e Derivados)
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100, default="John Doe")  # Sugestão: use 'username'
    userEmail = models.EmailField()  # Sugestão: use 'email'
    userJoinDate = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"Nome: {self.userName} | Id: {self.userId}"

    @property
    def tipo_usuario(self):
        if hasattr(self, 'student'):
            return 'aluno'
        elif hasattr(self, 'teacher'):
            return 'professor'
        elif hasattr(self, 'admin'):
            return 'admin'
        elif hasattr(self, 'sponsor'):
            return 'sponsor'
        return 'desconhecido'

class Admin(User):
    lastJoined = models.DateTimeField(auto_now_add=True)

    @property
    def tipo_display(self):
        return "admin"


class Student(User):
    studentAge = models.PositiveIntegerField(default=0)
    classesMissedCount = models.IntegerField(default=0)
    classesMissed = models.TextField(default="", blank=True)
    # cursoId1|cursoId2|cursoId3|...
    coursesReg= models.TextField(default = "", blank = True)
    # desempenho1|desempenho2|desempenho3|...
    coursesEval = models.TextField(default = "", blank = True)

    @property
    def tipo_display(self):
        return "aluno"

class Teacher(User):
    teacherSubject = models.CharField(max_length=100)
    teacherSchedule = models.TextField(null=True)

    @property
    def tipo_display(self):
        return "professor"


class Sponsor(User):
    sponsorDescription = models.TextField()



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    TIPO_USUARIO_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
    ]
    tipo_usuario = models.CharField(
        max_length=15,
        choices=TIPO_USUARIO_CHOICES,
        blank=True, 
        null=True
    )
    dados_calendario_json = models.TextField(blank=True, null=True, default='{}') 
    
    def __str__(self):
        return f'{self.user.username} Profile ({self.get_tipo_usuario_display()})'

    @property
    def calendario(self):
        if self.dados_calendario_json:
            try:
                return json.loads(self.dados_calendario_json)
            except json.JSONDecodeError:
                return {} 
        return {}

    @calendario.setter
    def calendario(self, value):
        self.dados_calendario_json = json.dumps(value)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


# DADOS ESTENDIDOS DO USUÁRIO
class StudentData(models.Model):
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    studentAge = models.PositiveIntegerField(default=0, null=True, blank=True)
    classesMissedCount = models.IntegerField(default=0, null=True, blank=True)
    classesMissed = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Dados Aluno: {self.user_profile.user.username}"


class TeacherData(models.Model):
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    teacherSubject = models.CharField(max_length=100, blank=True, null=True)
    teacherSchedule = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Dados Professor: {self.user_profile.user.username}"


# MODELO DE CURSO
class Course(models.Model):
    courseTitle = models.CharField(max_length=100)
    courseImage = models.ImageField(default="fallback.jpeg", blank=True, upload_to='course_images/')
    courseDescription = models.TextField()
    courseTests = models.TextField(blank=True)

    def __str__(self):
        return self.courseTitle


# CALENDÁRIO COMO JSON (getter/setter)
@property
def calendario(self):
    if self.dados_calendario_json:
        try:
            return json.loads(self.dados_calendario_json)
        except json.JSONDecodeError:
            return {}
    return {}

@calendario.setter
def calendario(self, value):
    self.dados_calendario_json = json.dumps(value)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


# DESEMPENHO POR MATÉRIA
class Materia(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class DesempenhoMateria(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='desempenhos')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    
    NOTA_CHOICES = [
        ('', 'Não Avaliado'),
        ('muito_bom', 'Muito Bom'),
        ('bom', 'Bom'),
        ('satisfatorio', 'Satisfatório'),
        ('regular', 'Regular'),
        ('insatisfatorio', 'Insatisfatório'),
    ]
    
    nota_qualitativa = models.CharField(
        max_length=20,
        choices=NOTA_CHOICES,
        blank=True,
        default=''
    )
    faltas = models.PositiveIntegerField(default=0, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('aluno', 'materia')

    def __str__(self):
        return f"{self.aluno.username} - {self.materia.nome}: {self.get_nota_qualitativa_display()}"



   #---------------------
    #ADICIONANDO DUVIDAS
    #--------------------

    #duvidas

from django.conf import settings 

class Duvida(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    remetente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='duvidas_enviadas', null=True, blank=True)
    nome = models.CharField(max_length=100)
    destinatario = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Dúvida"
        verbose_name_plural = "Dúvidas"
