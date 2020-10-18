from datetime import datetime, timedelta 

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import ordinal

from .models import *
from .services import *

# -----------------------------------------------------------------------------
# GLOBAL CONSTANTS
# -----------------------------------------------------------------------------

REG_START_DATE = datetime(2021, 1, 1)
REG_END_DATE   = datetime(2021, 12, 31)

# -----------------------------------------------------------------------------
# Formats date for display DAY MON YEAR
# -----------------------------------------------------------------------------
def date_text(date):
    year  = date.year
    day   = ordinal(date.day)
    month = date.strftime('%b').upper()
    return ('%s %s %s' % (day, month, year))

# -----------------------------------------------------------------------------
# Default page showing all available Webinars
# -----------------------------------------------------------------------------
def index(request):
    print('DEBUG>>> index(): rendering registration default page')
    context = {}
    return render(request, 'index.html', context)

# -----------------------------------------------------------------------------
# Render booking for live info session
# -----------------------------------------------------------------------------
def booking1(request):
    print('DEBUG>>> booking1(): rendering page for info session')
    context = {}
    return render(request, 'book_infosession.html', context)

# -----------------------------------------------------------------------------
# Render booking for guidance counselor
# -----------------------------------------------------------------------------
def booking2(request):
    print('DEBUG>>> booking2(): rendering page for guidance counselor')
    context = {}
    return render(request, 'book_counselor_1.html', context)

# -----------------------------------------------------------------------------
# Render booking for course counselor
# -----------------------------------------------------------------------------
def booking3(request):
    print('DEBUG>>> booking3(): rendering page for course counselor')

    start_date = REG_START_DATE
    end_date   = REG_END_DATE
    delta      = timedelta(days=1)
    event_list = []

    calendar = start_date
    while calendar <= end_date:
        events = Event.objects.filter(date=calendar).order_by('date', 'start_time')
        if events:
            session = { 'day'     : date_text(calendar),
                        'events'  : events }
            event_list.append(session)
        calendar += delta

    context = { 'event_list' : event_list }
    return render(request, 'book_counselor_2.html', context)

# -----------------------------------------------------------------------------
# Check blank string data
# -----------------------------------------------------------------------------
def isBlank (data):
    return not (data and data.strip())

# -----------------------------------------------------------------------------
# Webinar form registration request handler
# -----------------------------------------------------------------------------
def register(request):
    print('DEBUG>>> register(): Registration API endpoint')
    context = {}
    error   = False

    # POST request save data
    if request.method == 'POST':
        context['values']   = request.POST
        context['event_id'] = request.POST['event_id']

        try:
            event_id      = request.POST['event_id']
            first_name    = request.POST['first_name']
            last_name     = request.POST['last_name']
            email         = request.POST['email']
            email_verify  = request.POST['email_verify']
            phone         = request.POST['phone']
            dob           = request.POST['dob']
            gender        = request.POST['gender']
            participant_type  = request.POST['participant_type']
            participant_other = request.POST['participant_other']
            attendees   = request.POST['attendees']
            inquiry     = request.POST['inquiry']
            info_source = request.POST['info_source']
            info_other  = request.POST['info_other']
            #course      = request.POST['course']

            # Perform input validation
            if isBlank(event_id):
                print('1 >> event_id = ' + event_id)
                raise Exception("No data exception")
            if isBlank(first_name):
                print('2 >> first_name = ' + first_name)
                raise Exception("No data exception")
            if isBlank(last_name):
                print('3 >> last_name = ' + last_name)
                raise Exception("No data exception")
            if isBlank(email):
                print('4 >> email = ' + email)
                raise Exception("No data exception")
            if isBlank(email_verify):
                print('5 >> email_verify = ' + email_verify)
                raise Exception("No data exception")
            if isBlank(phone):
                print('6 >> phone = ' + phone)
                raise Exception("No data exception")
            if isBlank(dob):
                print('7 >> dob = ' + dob)
                raise Exception("No data exception")
            if email != email_verify:
                print('8 >> email <> email_verify')
                raise Exception("Invalid data exception")

            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            
            event = Event.objects.filter(id=event_id).first()
            if event:
                participant, created = Participant.objects.get_or_create( event=event, first_name=first_name, 
                                                    last_name=last_name, email=email, 
                                                    phone=phone, dob=dob_date, gender=gender)
        except:
            error = True

        if error:
            messages.error(request, 'Please provide correct registration information.')
            return render(request, '_regform.html', context, status=400)
        else:
            return HttpResponse(status=200)

    # GET request render the form
    else:
        event_id = request.GET['event_id']
        event    = Event.objects.filter(id=event_id)

    if event:
        courses = Course.objects.filter(school=event.first().school)
        context['event_id'] = event_id
        context['courses']  = courses

    print(event_id)
    return render(request, '_regform.html', context)

# -----------------------------------------------------------------------------
# Email template test endpoint only
# -----------------------------------------------------------------------------
def invite(request):
    print('DEBUG>>> invite(): rendering invite email HTML')
    
    invite = {  'start_date' : datetime.today(),
                'name'       : 'Sirhc Someroda', 
                'invitation' : 'Zoom invite here https://zoom/meeting/1245',
                'tagline'    : 'Test Tagline',
                'details'    : 'The quick brown fox jump over the lazy dog near the bank of the river.',
                'photo'      : 'web-defaults/placeholder.png',
                'email'      : 'sirhcsomeroda@gmail.com' }

    context = { 'invite' : invite }
    send_registration_email(invite)
    return render(request, 'email_invite.html', context)