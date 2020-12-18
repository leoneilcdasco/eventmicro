from django.urls import path
from . import views

urlpatterns = [
    path('organizer', views.login, name='organizer'),
    path('login', views.login, name='login'),
    path('login/<str:__username__>', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('report', views.report, name='report'),
    path('attendees/<int:__id__>', views.attendees, name='attendees'),
    path('reminder/<int:__id__>', views.reminder, name='reminder'),
]