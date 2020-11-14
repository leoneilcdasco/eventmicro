from django.contrib import admin
from .models import *

admin.site.register(School)
admin.site.register(Course)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(CourseParticipant)
admin.site.register(CourseEvent)