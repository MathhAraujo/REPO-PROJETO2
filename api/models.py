from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # Se fosse refatorar para AUTH_USER_MODEL

# SEU CÓDIGO ORIGINAL User Abstrato (com ressalvas sobre AUTH_USER_MODEL)
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100, default="John Doe") # Considere usar 'username' para compatibilidade
    userEmail = models.EmailField() # Considere usar 'email'
    userJoinDate = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"Nome: {self.userName} | Id: {self.userId}"

    # Adicionar uma propriedade para identificar o tipo pode ser útil
    @property
    def tipo_usuario(self):
        if hasattr(self, 'student'): # Checa se é uma instância de Student através da relação reversa
            return 'aluno'
        elif hasattr(self, 'teacher'): # Checa se é uma instância de Teacher
            return 'professor'
        elif hasattr(self, 'admin'):
            return 'admin'
        elif hasattr(self, 'sponsor'):
            return 'sponsor'
        return 'desconhecido' # Fallback

class Admin(User):
    lastJoined = models.DateTimeField(auto_now_add=True)

    @property
    def tipo_display(self): 
        return "admin"

class Student(User):
    studentAge = models.PositiveIntegerField(default=0)
    classesMissedCount = models.IntegerField(default=0)
    classesMissed = models.TextField(default="", blank=True)

    @property
    def tipo_display(self):
        return "aluno"

class Teacher(User):
    teacherSubject = models.CharField(max_length=100)
    teacherSchedule = models.TextField(null=True)

    @property
    def tipo_display(self):
        return "professor"

# ... (Sponsor e Course)




from django.db import models
from django.conf import settings 
from django.db.models.signals import post_save
from django.dispatch import receiver


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
 

    def __str__(self):
        return f'{self.user.username} - Perfil ({self.get_tipo_usuario_display()})'

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



class StudentData(models.Model): 
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)

    
    studentAge = models.PositiveIntegerField(default=0, null=True, blank=True)
    classesMissedCount = models.IntegerField(default=0, null=True, blank=True)
    classesMissed = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Dados Aluno: {self.user_profile.user.username}"

class TeacherData(models.Model): # Renomeado
    user_profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    
    teacherSubject = models.CharField(max_length=100, blank=True, null=True)
    teacherSchedule = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Dados Professor: {self.user_profile.user.username}"



class Course(models.Model): 
    courseTitle = models.CharField(max_length=100)
    courseImage = models.ImageField(default="fallback.jpeg", blank=True, upload_to='course_images/') 

    courseDescription = models.TextField() 
    courseTests = models.TextField(blank=True)

    def __str__(self):
        return self.courseTitle




class Sponsor(User):
    sponsorDescription = models.TextField()

class Course(models.Model):
    courseTitle = models.CharField(max_length=100)
    courseImage = models.ImageField(default="fallback.jpeg", blank=True)
    couseDescription = models.TextField()
    courseTests = models.TextField(blank = True)

    def __str__(self):
        return f"Title: {self.courseTitle} | Image: {self.courseImage} | Description: {self.couseDescription}"