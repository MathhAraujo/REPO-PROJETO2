from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
import json


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
    return render(request, 'cadastro.html')

def menucursos_view(request):
    return render(request, 'menuCursos.html')
