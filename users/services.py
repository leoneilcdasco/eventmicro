
import uuid
import vobject

from datetime import datetime, timedelta 
from email.mime.text import MIMEText

from django.conf import settings
from django.db.models import Count, Sum
from django.db.models.functions import TruncHour, TruncMonth
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from pages.models import *

# Default email subject
SUBJECT_DEFAULT = 'Singapore Polytechnic Open House 2021'

# Test email recipient
TEST_EMAIL = 'leoneil@mybuildtec.biz'

# School IDs to be excluded from the chart
NON_SCHOOL_IDS = [12, 13]

# Fixed dates of events
EVENT_DATES = [ datetime(2021, 1, 7), datetime(2021, 1, 8), datetime(2021, 1, 9) ]

# -----------------------------------------------------------------------------
# Check blank string data
# -----------------------------------------------------------------------------
def isBlank (data):
    return not (data and data.strip())

# -----------------------------------------------------------------------------
# Retrieve data for plotting to chart dashboard
# -----------------------------------------------------------------------------
def chartdata():
    print('DEBUG>>> chartdata(): retrieve summary data for chart')
    data = { }

    #x_series = list(School.objects.values_list('name', flat=True))
    x_series  = []
    y1_series = []
    y2_series = []

    # Loop in all registered schools
    schools = School.objects.all()
    for school in schools:
        y1_data = 0
        y2_data = 0

        if school.id in NON_SCHOOL_IDS:
            continue

        # Save the school name as chart x-axis label
        x_series.append(school.name)

        # Loop in all events in current school
        events = school.event_set.all()
        for event in events:
            # Get total registration in the event
            y1_data += len(event.participant_set.all())
            
            # Get total of all attendees in the event
            aggregate = event.participant_set.aggregate(total_attendees=Sum('attendees'))
            #print(aggregate['total_attendees'])
            if aggregate['total_attendees'] is not None:
                y2_data += aggregate['total_attendees']

        y1_series.append(y1_data)
        y2_series.append(y2_data)

    data['x_series']  = x_series
    data['y1_series'] = y1_series
    data['y2_series'] = y2_series

    return data

# -----------------------------------------------------------------------------
# Retrieve aggregated data to show total registration & attendees
# -----------------------------------------------------------------------------
def totalregistration():
    print('DEBUG>>> totalregistration(): retrieve total registration and attendees')
    total = {}
    count = Participant.objects.annotate(month=TruncMonth('registration_date')).values('month') \
                               .annotate(count=Count('id'), attending=Sum('attendees')).values('month', 'count', 'attending')
    registered = 0
    attending  = 0
    m1_series  = []
    m2_series  = []

    # Get total and monthly series values
    for c in count:
        registered += c['count']
        attending  += c['attending']
        m1_series.append(c['count'])
        m2_series.append(c['attending'])

    total['registered'] = registered
    total['attending']  =  attending
    total['m1_series']  =  m1_series
    total['m2_series']  =  m2_series

    return total

# -----------------------------------------------------------------------------
# Retrieve course sessions summary data-table
# -----------------------------------------------------------------------------
def courseinterest():
    print('DEBUG>>> courseinterest(): retrieve course session data-table')
    datatable = []

    # Loop in all registered schools
    schools = School.objects.all()
    for school in schools:

        if school.id in NON_SCHOOL_IDS:
            continue

        # Loop in all courses in current school
        courses = school.course_set.all()
        for course in courses:
            datarow = {}
            interested = 0
            datarow['school'] = school.name
            datarow['course'] = course.name

            interested = CourseParticipant.objects.filter(course=course).all().count()
            datarow['interested'] = interested

            # Append data row 
            datatable.append(datarow)
    
    return datatable

# -----------------------------------------------------------------------------
# Retrieve sessions attendees / user list data-table from all schools
# -----------------------------------------------------------------------------
def userlist(school_id=0):
    print('DEBUG>>> userlist(): retrieve user list data-table')
    datatable = []
    daytotal = { 'day1' : 0, 'day2' : 0, 'day3' : 0 }

    if school_id > 0:
        datatable = schoolusers(school_id)
        daytotal  = dailytotal(school_id)
    else:
        schools = School.objects.all()
        for school in schools:
            s_users = schoolusers(school.id)
            dt = dailytotal(school.id)

            daytotal['day1'] += dt['day1']
            daytotal['day2'] += dt['day2']
            daytotal['day3'] += dt['day3']

            datatable += s_users

    dataset = { 'daytotal' : daytotal, 'datatable' : datatable }
    return dataset

# -----------------------------------------------------------------------------
# Retrieve sessions attendees / user list data-table per school
# -----------------------------------------------------------------------------
def schoolusers(school_id):
    print('DEBUG>>> schoolusers(): retrieve user list data-table')
    datatable = []

    school = School.objects.filter(id=school_id).first()
    if school:
        # Loop in all events in current school
        events = school.event_set.all()
        for event in events:
            participants = Participant.objects.filter(event=event).all()
            for participant in participants:
                datarow = {}
                cp = CourseParticipant.objects.filter(participant=participant).first()
                
                datarow['event']       = event.name
                datarow['date']        = event.date
                datarow['s_time']      = event.start_time
                datarow['e_time']      = event.end_time
                datarow['participant'] = participant
                datarow['email']       = participant.email
                datarow['question']    = participant.question
                datarow['event_obj']   = event
                
                if cp:
                    datarow['course'] = cp.course.name

                datatable.append(datarow)

    return datatable

# -----------------------------------------------------------------------------
# Get summary of participants for the event dates (EVENT_DATES)
# -----------------------------------------------------------------------------
def dailytotal(school_id):
    print('DEBUG>>> dailytotal(): retrieve total registration per event dates')
    daytotal = { 'day1' : 0, 'day2' : 0, 'day3' : 0 }

    school = School.objects.filter(id=school_id).first()
    if school:
        # Loop in all events in current school
        events = school.event_set.all()
        for event in events:
            participants = Participant.objects.filter(event=event).all()
            for participant in participants:
            
                if event.date == EVENT_DATES[0].date():
                    daytotal['day1'] += 1

                if event.date == EVENT_DATES[1].date():
                    daytotal['day2'] += 1

                if event.date == EVENT_DATES[2].date():
                    daytotal['day3'] += 1

    return daytotal

# -----------------------------------------------------------------------------
# Sends email webinar reminder
# -----------------------------------------------------------------------------
def send_email_reminder(invite):
    print('DEBUG>>> send_email_reminder(): sending email reminder')

    if settings.DEBUG:
        recipient_email = TEST_EMAIL
    else:
        recipient_email = invite['email']

    # Site domain setting
    domain = 'https://' + str(Site.objects.get_current())
    context= { 'domain' : domain, 'invite' : invite, 'course_invites' : invite['course_invites'] }
 
    # Set email parameters
    #subject    = SUBJECT_DEFAULT if isBlank(invite['subject']) else invite['subject']
    from_email = 'sp-webinar@spoh21registration.com'
    to_email   = [ recipient_email ]

    text_content = invite['details']
    html_content = render_to_string('email_reminder.html', context)

    msg = EmailMultiAlternatives(SUBJECT_DEFAULT, text_content, from_email, to_email )
    msg.attach_alternative(html_content, "text/html")

    # Send SMTP outbound email to participant
    msg.send() 