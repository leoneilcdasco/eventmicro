from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User

from pages.models import *
from .services import *

# -----------------------------------------------------------------------------
# login view controller - handles user login authentication 
# -----------------------------------------------------------------------------
def login(request, __username__=None):
    context = { }
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        context['username'] = username

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)      
            print('DEBUG>>> login(): redirect to report page')
            return redirect('report')
        else:
            messages.error(request, 'Invalid credentials')
            context['username'] = username
            print('DEBUG>>> login(): Invalid credentials, render login.html')
            return render(request, 'user/login.html', context)
    else:
        if __username__:
            context['username'] = __username__

        print('DEBUG>>> login(): render login.html')
        return render(request, 'user/login.html', context)

# -----------------------------------------------------------------------------
# logout view controller - ends user session 
# -----------------------------------------------------------------------------
def logout(request):
    auth.logout(request)
    messages.used = True
    messages.success(request, 'You are now logged out')
    
    return redirect('login')

# -----------------------------------------------------------------------------
# report view controller - renders organizer report page
# -----------------------------------------------------------------------------
@login_required
def report(request):
    context = { }

    schools = School.objects.all()
    context['schools']   = schools
    context['data']      = chartdata()
    context['total']     = totalregistration()
    context['interests'] = courseinterest()

    return render(request, 'report.html', context)

# -----------------------------------------------------------------------------
# attendees view controller - renders attendees list page
# -----------------------------------------------------------------------------
@login_required
def attendees(request, __id__=0):
    context = { }

    schools = School.objects.all()
    context['schools'] = schools

    if __id__ == 0:
        active_school = 'All Schools'
    else:
        active_school = School.objects.filter(id=__id__).first()
        
    context['active_school'] = active_school
    context['userlist'] = userlist(__id__)

    return render(request, 'attendees.html', context)