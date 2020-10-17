from datetime import datetime, timedelta 

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User

from .models import *
from .services import *

# -----------------------------------------------------------------------------
# Default page showing all available Webinars
# -----------------------------------------------------------------------------
def index(request):
    print('DEBUG>>> index(): rendering registration default page')

    today    = datetime.today()
    calendar = datetime(today.year, today.month, today.day)
    year     = today.year

    event_list = []
    for m in range(0, 24):     
        events = Event.objects.filter(event_date__year=calendar.year,
                                      event_date__month=calendar.month).order_by('event_date')
        if events:
            month_events = { 'month'  : calendar,
                             'events' : events }
            event_list.append(month_events)

        if calendar.month < 12:
            next_month = int(calendar.month + 1)
        else:
            next_month = 1
            year += 1

        calendar = datetime(year, next_month, 1)

    context = { 'event_list' : event_list }
    return render(request, 'index.html', context)

# -----------------------------------------------------------------------------
# Webinar form registration request handler
# -----------------------------------------------------------------------------
def register(request):
    print('DEBUG>>> register(): Registration API endpoint')

    context = {}
    if request.method == 'POST':
        event_id   = request.POST['event_id']
        first_name = request.POST['first_name']
        last_name  = request.POST['last_name']
        email      = request.POST['email']
        phone      = request.POST['phone']
        dob        = request.POST['dob']
        gender     = request.POST['gender']
        others     = request.POST['others']

        event = Event.objects.filter(id=event_id).first()
        if event:
            participant, created = Participant.objects.get_or_create( event=event, first_name=first_name, 
                                                                last_name=last_name, email=email, 
                                                                phone=phone, dob=dob, gender=gender,
                                                                others=others)
            #Send email invite
            invite = {  'event_date'  : event.event_date,
                        'name'       : str(participant.first_name + ' ' + participant.last_name), 
                        'invitation' : event.invitation,
                        'tagline'    : event.tagline,
                        'details'    : event.details,
                        'photo'      : event.photo,
                        'email'      : participant.email }

            context['invite'] = invite
            send_registration_email(invite)
    
    return render(request, 'email_invite.html', context)

# -----------------------------------------------------------------------------
# Email template test endpoint only
# -----------------------------------------------------------------------------
def invite(request):
    print('DEBUG>>> invite(): rendering invite email HTML')
    
    invite = {  'event_date' : datetime.today(),
                'name'       : 'Sirhc Someroda', 
                'invitation' : 'Zoom invite here https://zoom/meeting/1245',
                'tagline'    : 'Test Tagline',
                'details'    : 'The quick brown fox jump over the lazy dog near the bank of the river.',
                'photo'      : 'web-defaults/placeholder.png',
                'email'      : 'sirhcsomeroda@gmail.com' }

    context = { 'invite' : invite }
    send_registration_email(invite)
    return render(request, 'email_invite.html', context)