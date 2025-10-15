from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.register,name='signup'),
    path('signin/',views.login,name='signin'),
    path('learnmore/',views.learnmore,name='learnmore'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('patientdashboard/',views.patientdashboard,name='patientdashboard'),
    path('hospitaldashboard/',views.hospitaldashboard,name='hospitaldashboard'),
    path('donordashboard/',views.donordashboard,name='donordashboard')
]