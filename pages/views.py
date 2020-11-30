import traceback 
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
    day   = date.day
    month = date.strftime('%B')
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
    print('DEBUG>>> booking3(): rendering page for info session')
    
    #TODO count access log

    start_date = REG_START_DATE
    end_date   = REG_END_DATE
    delta      = timedelta(days=1)
    event_list = []

    calendar = start_date
    while calendar <= end_date:
        school_events = Event.objects.filter(date=calendar, school__extra=0).order_by('date', 'start_time')
        if school_events:
            session = { 'day'     : date_text(calendar),
                        'events'  : school_events }
            event_list.append(session)

        calendar += delta

    context = { 'event_list' : event_list }
    return render(request, 'book_infosession.html', context)

# -----------------------------------------------------------------------------
# Render booking for guidance counselor
# -----------------------------------------------------------------------------
def booking2(request):
    print('DEBUG>>> booking2(): rendering page for guidance counselor')
    context = {}

    #TODO count access log

    return render(request, 'book_guidance_counselor.html', context)

# -----------------------------------------------------------------------------
# Render booking for course counselor
# -----------------------------------------------------------------------------
def booking3(request, __id__=0):
    print('DEBUG>>> booking1(): rendering page for course counselor')
    context = {}

    #TODO count access log
    
    school = School.objects.filter(id=__id__).first()
    context = { 'school' : school }

    return render(request, 'book_course_counselor.html', context)

# -----------------------------------------------------------------------------
# Render booking for shows and seminar
# -----------------------------------------------------------------------------
def booking4(request):
    print('DEBUG>>> booking4(): rendering page for shows & seminar')

    #TODO count access log

    start_date = REG_START_DATE
    end_date   = REG_END_DATE
    delta      = timedelta(days=1)
    event_list = []

    calendar = start_date
    while calendar <= end_date:
        extra_events  = Event.objects.filter(date=calendar, school__extra=1).order_by('date', 'start_time')
        if extra_events:
            session = { 'day'     : date_text(calendar),
                        'events'  : extra_events }
            event_list.append(session)

        calendar += delta

    context = { 'event_list' : event_list }
    return render(request, 'book_shows_seminar.html', context)

# -----------------------------------------------------------------------------
# Render schools for course counselor selection
# -----------------------------------------------------------------------------
def schools(request):
    print('DEBUG>>> schools(): rendering page for schools')
    context = {}

    #TODO count access log
    schools = School.objects.filter(extra=0).all().order_by('id')

    context = { 'schools' : schools }
    return render(request, 'schools.html', context)

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
    err_fno = 0
    status  = 200
    event   = None

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
            courses       = request.POST.getlist('course')
            inquiry       = request.POST.get('inquiry', '')

            #phone         = request.POST['phone']
            #dob           = request.POST['dob']
            #gender        = request.POST['gender']
            #participant_type  = request.POST['participant_type']
            #participant_other = request.POST['participant_other']
            #attendees     = request.POST['attendees']
            #info_source   = request.POST['info_source']
            #info_other    = request.POST['info_other']


            if courses:
                context['course_ids'] = [ int(i) for i in courses ]
                interested_in = ','.join(courses)
            else:
                interested_in = ''
            
            # Perform input validation
            if isBlank(event_id):
                print('1 >> event_id = ' + event_id)
                err_fno = 1
                raise Exception("No data exception")
            else:
                event = Event.objects.filter(id=event_id).first()

            if isBlank(first_name):
                print('2 >> first_name = ' + first_name)
                err_fno = 2
                raise Exception("No data exception")
            if isBlank(last_name):
                print('3 >> last_name = ' + last_name)
                err_fno = 3
                raise Exception("No data exception")
            if isBlank(email):
                print('4 >> email = ' + email)
                err_fno = 4
                raise Exception("No data exception")
            if isBlank(email_verify):
                print('5 >> email_verify = ' + email_verify)
                err_fno = 5
                raise Exception("No data exception")
            if email != email_verify:
                print('5 >> email <> email_verify')
                err_fno = 5
                raise Exception("Invalid data exception")
            #if isBlank(phone):
            #    print('6 >> phone = ' + phone)
            #    err_fno = 6
            #    raise Exception("No data exception")
            #if isBlank(dob):
            #    print('7 >> dob = ' + dob)
            #    err_fno = 7
            #    raise Exception("No data exception")
            #if isBlank(gender) or gender == '-':
            #    print('8 >> gender = ' + gender)
            #    err_fno = 8
            #    raise Exception("Invalid data exception")
            #if int(participant_type) == 0:
            #    print('9 >> participant_type =' +  participant_type)
            #    err_fno = 9
            #    raise Exception("Invalid data exception")
            #if int(attendees) == 0:
            #    print('10 >> attendees =' +  attendees)
            #    err_fno = 10
            #    raise Exception("Invalid data exception")

            #dob_date = datetime.strptime(dob, '%Y-%m-%d')
            
            if event:
                #new_values = {  'phone' : phone, 'dob' : dob_date, 'gender' : gender, 'question' : inquiry, 
                #                'participant_type' : participant_type, 'participant_other' : participant_other, 
                #                'infosource_type' : info_source, 'infosource_other' : info_other, 
                #                'attendees' : attendees, 'interested_in' : interested_in,  }

                new_values = {  'question' : inquiry, 'interested_in' : interested_in  }
                participant, created = Participant.objects.update_or_create( event=event, first_name=first_name, 
                                                    last_name=last_name, email=email,  defaults=new_values)

                for course_id in courses:
                    course = Course.objects.filter(id=course_id).first()
                    course_participant, created = CourseParticipant.objects.get_or_create(course=course, participant=participant)

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

                #Send email invite
                invite = {  'date'       : event.date,
                            'school'     : event.school,
                            's_time'     : event.start_time,
                            'e_time'     : event.end_time,
                            'calendar'   : event.calendar_time(),
                            'name'       : str(participant.first_name + ' ' + participant.last_name), 
                            'subject'    : event.invitation,
                            'tagline'    : event.name,
                            'details'    : event.details,
                            'photo'      : event.photo,
                            'email'      : participant.email,
                            'session_type' : session_type,
                            'link1'      : event.link1,
                            'link2'      : event.link2,
                            'link3'      : event.link3,
                            'course_invites' : course_invites }

                context['invite'] = invite
                send_registration_email_plain(invite)
                
        except:
            error = True
            context['err_fno'] = err_fno
            print ('ERROR>>> Error in field no : ' + str(err_fno))
            print (traceback.format_exc())

        if error:
            messages.error(request, 'Please provide correct registration information.')
            status = 400
        else:
            return HttpResponse(status=200)

    # GET request render the form
    else:
        event_id = request.GET['event_id']
        event    = Event.objects.filter(id=event_id).first()

    if event:
        courses = Course.objects.filter(school=event.school)
        context['event_id'] = event_id
        context['event']    = event
        context['courses']  = courses

    return render(request, '_regform.html', context, status=status)

# -----------------------------------------------------------------------------
# Email template test endpoint only
# -----------------------------------------------------------------------------
def invite(request):
    print('DEBUG>>> invite(): rendering invite email HTML')
    
    start = datetime(2020, 10, 26, 10, 30)
    end   = datetime(2020, 10, 26, 11, 30)

    course_invites = [ 'Link 1', 'Link 2', 'Link 3' ]

    invite = {  'date' : datetime.today(),
                'school'     : 'SCHOOL OF XXX ',
                's_time'     : '1:00 PM',
                'e_time'     : '2:00 PM',
                'subject'    : 'Test invite subject',
                'calendar'   : {'start' : start, 'end' : end },
                'name'       : 'Sirhc Someroda', 
                'invitation' : 'Zoom invite here https://zoom/meeting/1245',
                'tagline'    : 'Test Tagline',
                'details'    : 'The quick brown fox jump over the lazy dog near the bank of the river.',
                'photo'      : 'web-defaults/placeholder.png',
                'email'      : 'sirhcsomeroda@gmail.com',
                'session_type' : 'Diplomas',
                'link1'      : 'http://link1/vimeo',
                'link2'      : 'http://link2/zoom',
                'link3'      : 'http://link3/zoom',
                'course_invites' : course_invites }

    context = { 'invite' : invite }
    send_registration_email_plain(invite)

    return render(request, 'email_invite_plain.html', context)