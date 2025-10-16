from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.register,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('learnmore/',views.learnmore,name='learnmore'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('patientdashboard/',views.patientdashboard,name='patientdashboard'),
    path('hospitaldashboard/',views.hospitaldashboard,name='hospitaldashboard'),
    path('donordashboard/',views.donordashboard,name='donordashboard'),
    path('update_donor/',views.update_donor,name='update_donor'),
    path('donation_history/',views.donation_history,name='donation_history'),
    path('donor_eligibility/',views.donor_eligibility,name='donor_eligibility'),
    path('request_appointment/',views.request_appoinment,name='request_appointment')
]