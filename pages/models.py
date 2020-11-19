from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

PARTICIPANT_TYPES = (
    (0, '-'),
    (1, 'Parent'),
    (2, 'O Level School Leaver'),
    (3, 'N Level School Leaver'),
    (4, 'ITE Graduate/Student'),
    (5, 'Secondary School Student (Level), School Teacher/Educator'),
    (100, 'Others')
)

INFOSOURCE_TYPES = (
    (0, '-'),
    (1, 'Social Media'),
    (2, 'Mailer from SP'),
    (100, 'Others')
)

GENDER_CHOICES = (
    ('-', 'None'),
    ('M', 'Male'),
    ('F', 'Female')
)

EXTRA_CHOICES = (
    (0, 'No'),
    (1, 'Yes')
)

def event_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/event_<id>/<filename>
    return 'uploads/event_{0}/{1}'.format(instance.id, filename)

def school_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/school/<filename>
    return 'uploads/school/{1}'.format(instance.id, filename)

class School(models.Model):
    name   = models.CharField(max_length=250)
    photo  = models.ImageField(upload_to=school_upload_path, default='web-defaults/placeholder.png')
    email  = models.CharField(max_length=250, blank=True)
    phone  = models.CharField(max_length=250, blank=True)
    extra  = models.IntegerField(choices=EXTRA_CHOICES, default=0)
    appointment = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name   = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    invitation  = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Event(models.Model):
    school     = models.ForeignKey(School, on_delete=models.CASCADE)
    name       = models.CharField(max_length=250)
    photo      = models.ImageField(upload_to=event_upload_path, default='web-defaults/placeholder.png')
    date       = models.DateField(default=datetime.now)
    start_time = models.TimeField(blank=True)
    end_time   = models.TimeField(blank=True)
    organizer  = models.CharField(max_length=250, blank=True)
    tagline    = models.CharField(max_length=512, blank=True)
    details    = models.TextField(blank=True)
    link1      = models.TextField(blank=True)
    link2      = models.TextField(blank=True)
    link3      = models.TextField(blank=True)
    invitation = models.TextField(blank=True, default='Singapore Polytechnic Open House 2021 – Info Session')
    def __str__(self):
        return self.name
    def calendar_time(self):

        # datetime(year, month, day, hour, minute, second, microsecond)
        start = datetime(self.date.year, self.date.month, self.date.day, \
                         self.start_time.hour, self.start_time.minute, 0, 0)

        end = datetime(self.date.year, self.date.month, self.date.day, \
                         self.end_time.hour, self.end_time.minute, 0, 0)

        return {'start' : start, 'end' : end }

class Participant(models.Model):
    event         = models.ForeignKey(Event, on_delete=models.CASCADE)
    # Account information
    first_name    = models.CharField(max_length=250)
    last_name     = models.CharField(max_length=250)
    email         = models.CharField(max_length=250)
    gender        = models.CharField(max_length=5, choices=GENDER_CHOICES, default='-')
    phone         = models.CharField(max_length=250, blank=True)
    dob           = models.DateTimeField(default=datetime.now)
    attendees     = models.IntegerField(default=1)
    participant_type  = models.IntegerField(choices=PARTICIPANT_TYPES, default=0)
    participant_other = models.TextField(blank=True)
    infosource_type   = models.IntegerField(choices=INFOSOURCE_TYPES, default=0)
    infosource_other  = models.TextField(blank=True)
    question          = models.TextField(blank=True)
    interested_in     = models.CharField(max_length=250, blank=True)

    is_paid           = models.BooleanField(default=False)
    registration_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def course_list(self):
        courses_id = []
        if self.interested_in:
            courses_id = self.interested_in.split(',')
        return courses_id

class CourseParticipant(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    def __str__(self):
        return str(self.course) + '> ' + str(self.participant)

class CourseEvent(models.Model):
    course     = models.ForeignKey(Course, on_delete=models.CASCADE)
    event      = models.ForeignKey(Event, on_delete=models.CASCADE)
    invitation = models.TextField(blank=True)
    def __str__(self):
        return str(self.course) + '> ' + str(self.event)
