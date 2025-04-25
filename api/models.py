from django.db import models

# Create your models here.
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100,default="John Doe")
    userEmail = models.EmailField()
    userJoinDate = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"Nome: {self.userName} | Id: {self.userId}"

class Admin(User):
    lastJoined = models.DateTimeField(auto_now_add=True)

class Student(User):
    studentAge = models.PositiveIntegerField(default=0)
    classesMissedCount = models.IntegerField(default=0)
    classesMissed = models.JSONField(null=True)

class Teacher(User):
    teacherSubject = models.CharField(max_length=100)
    teacherSchedule = models.JSONField(null=True)

class Sponsor(User):
    sponsorDescription = models.TextField()

class MissedClass():
    date = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"{self.date}"