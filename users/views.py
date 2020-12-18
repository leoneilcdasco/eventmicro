from datetime import datetime

from django.http import HttpResponse, JsonResponse
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
    context = {}

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
    context = {}

    schools = School.objects.all()
    context['schools'] = schools
    context['data'] = chartdata()
    context['total'] = totalregistration()
    context['interests'] = courseinterest()

    return render(request, 'report.html', context)

# -----------------------------------------------------------------------------
# attendees view controller - renders attendees list page
# -----------------------------------------------------------------------------
@login_required
def attendees(request, __id__=0):
    context = {}

    schools = School.objects.all()
    context['schools'] = schools

    if __id__ == 0:
        active_school = 'All Schools'
    else:
        active_school = School.objects.filter(id=__id__).first()

    dataset = userlist(__id__)

    context['active_school'] = active_school
    context['userlist'] = dataset['datatable']
    context['dailycount'] = dataset['daytotal']

    return render(request, 'attendees.html', context)

# -----------------------------------------------------------------------------
# reminder view controller - sends email reminder to target participants
# -----------------------------------------------------------------------------
@login_required
def reminder(request, __id__=0):
    context = {}

    today   = datetime.now().date()
    schools = School.objects.all()
    context['schools'] = schools

    if __id__ == 0:
        active_school = 'All Schools'
    else:
        active_school = School.objects.filter(id=__id__).first()

    dataset = userlist(__id__)
    datatable = dataset['datatable']

    # Loop send email reminder per participants
    for datarow in datatable:
        event = datarow['event_obj']
        participant = datarow['participant']
        courses = participant.interested_in

        # Get session invitation link for the course
        course_invites = []
        invites = CourseEvent.objects.filter(event=event).all()
        for invite in invites:
            invitation = {}
            invitation['name'] = invite.course.name
            invitation['link'] = invite.invitation
            if str(invite.course.id) in courses:
                invitation['is_selected'] = True
            course_invites.append(invitation)
        
        session_type = "Diplomas"
        if event.school.extra == 1:
            session_type = "Specialization"

        if len(course_invites) == 0:
            course_invites = None

        # Prepare email invite reminder
        invite = {
                  'date': event.date,
                  'school': event.school,
                  's_time': event.start_time,
                  'e_time': event.end_time,
                  'calendar': event.calendar_time(),
                  'name': str(participant.first_name + ' ' + participant.last_name),
                  'subject': event.invitation,
                  'tagline': event.name,
                  'details': event.details,
                  'photo': event.photo,
                  'email' : participant.email,
                  'session_type': session_type,
                  'link1': event.link1,
                  'link2': event.link2,
                  'link3': event.link3,
                  'course_invites': course_invites
                }
        
        # Send email reminder
        if participant.reminder_on == today:
            print('Skipping already reminded today --> ' + participant.email)
            continue

        send_email_reminder(invite)

        # Update last reminder date in participant model
        print('Just reminded today --> ' + participant.email)
        Participant.objects.filter(id = participant.id).update(reminder_on = today)

    count = len(datatable)
    responseData = {
        'count': count
    }

    return JsonResponse(responseData)
