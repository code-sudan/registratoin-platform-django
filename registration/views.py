from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from secrets import randbelow
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.



USER_PASSWORD = "codesudan"

def index(request):
    return HttpResponse("This is index")


def login(request):
    pass

def logout(request):
    pass

def register_student(request):
    pass

def student_detail(request):
    pass

def register_in_program(request):
    pass