from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.register,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('learnmore/',views.learnmore,name='learnmore'),
    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('hospitaldashboard/',views.hospitaldashboard,name='hospitaldashboard'),
    path('donordashboard/',views.donordashboard,name='donordashboard'),
    path('update_donor/',views.update_donor,name='update_donor'),
    path('donation_history/',views.donation_history,name='donation_history'),
    path('donor_eligibility/',views.donor_eligibility,name='donor_eligibility'),
    path('request_appointment/',views.request_appoinment,name='request_appointment'),
    path('donor_notification/',views.donor_notification,name='donor_notification'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('search_blood/',views.search_blood,name='search_blood'),
    path('request_blood/',views.request_blood,name='request_blood')
]