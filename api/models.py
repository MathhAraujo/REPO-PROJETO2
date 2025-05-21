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
    classesMissed = models.TextField(default="", blank=True) #

class Teacher(User):
    teacherSubject = models.CharField(max_length=100)
    teacherSchedule = models.TextField(null=True)

class Sponsor(User):
    sponsorDescription = models.TextField()

class Course(models.Model):
    courseTitle = models.CharField(max_length=100)
    courseImage = models.ImageField(default="fallback.jpeg", blank=True)
    couseDescription = models.TextField()
    courseTests = models.TextField(blank = True)

    def __str__(self):
        return f"Title: {self.courseTitle} | Image: {self.courseImage} | Description: {self.couseDescription}"