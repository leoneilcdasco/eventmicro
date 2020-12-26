from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('channel-1', views.booking1, name='booking1'),
    path('channel-2', views.booking2, name='booking2'),
    path('channel-3/<int:__id__>', views.booking3, name='booking3'),
    path('channel-4', views.booking4, name='booking4'),
    path('channel-5', views.booking5, name='booking5'),
    path('channel-6', views.booking6, name='booking6'),
    path('channel-7', views.booking7, name='booking7'),
    path('schools', views.schools, name='schools'),
    path('register', views.register, name='register'),
    path('invite', views.invite, name='invite'),
]
