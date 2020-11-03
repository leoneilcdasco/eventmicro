from django.db.models import Count, Sum
from django.db.models.functions import TruncHour, TruncMonth

from pages.models import *

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

    if school_id > 0:
        datatable = schoolusers(school_id)
    else:
        schools = School.objects.all()
        for school in schools:
            s_users = schoolusers(school.id)
            datatable += s_users

    return datatable

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
                p_type = [ v for v in PARTICIPANT_TYPES if v[0] == participant.participant_type ][0]

                datarow['event']       = event.name
                datarow['date']        = event.date
                datarow['s_time']      = event.start_time
                datarow['e_time']      = event.end_time
                datarow['participant'] = participant
                datarow['email']       = participant.email
                datarow['phone']       = participant.phone
                datarow['type']        = p_type[1]
                datarow['attendees']   = participant.attendees
                
                datatable.append(datarow)

    return datatable
