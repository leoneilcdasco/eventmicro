from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User

def index(request):
    print('DEBUG>>> index(): rendering registration default page')
    return render(request, 'index.html')

def register(request):
    print('DEBUG>>> register(): Registration API endpoint')
    return render(request, 'index.html')