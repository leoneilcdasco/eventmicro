from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

GENDER_CHOICES = (
    ('-', 'None'),
    ('M', 'Male'),
    ('F', 'Female')
)

def event_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/event_<id>/<filename>
    return 'uploads/event_{0}/{1}'.format(instance.id, filename)

class Event(models.Model):
    name = models.CharField(max_length=250)
    photo      = models.ImageField(upload_to=event_upload_path, default='web-defaults/placeholder.png')
    event_date = models.DateTimeField(default=datetime.now)
    organizer  = models.CharField(max_length=250, blank=True)
    tagline    = models.CharField(max_length=512)
    details    = models.TextField(blank=True)
    invitation = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    event         = models.ForeignKey(Event, on_delete=models.CASCADE)
    # Account information
    first_name    = models.CharField(max_length=250)
    last_name     = models.CharField(max_length=250)
    email         = models.CharField(max_length=250)
    gender        = models.CharField(max_length=5, choices=GENDER_CHOICES, default='-')
    phone         = models.CharField(max_length=250, default=True)
    dob           = models.CharField(max_length=250, default=True)
    others        = models.TextField(blank=True)

    is_paid       = models.BooleanField(default=False)
    registration_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    