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
    path('request_blood_hospital/',views.request_blood_hospital,name='request_blood_hospital'),
    path('request_history/',views.request_history,name='request_history'),
    path('hospital_reports/',views.hospital_reports,name='hospital_reports'),
    path('profile_update/<int:hospital_id>',views.profile_update,name='profile_update'),
    path('hospital_details/<int:hospital_id>/',views.hospital_details,name='hospital_details'),







    path('donordashboard/',views.donordashboard,name='donordashboard'),
    path('update_donor/<int:donor_id>/',views.update_donor,name='update_donor'),
    path('donation_history/',views.donation_history,name='donation_history'),
    path('donor_eligibility/',views.donor_eligibility,name='donor_eligibility'),
    path('request_appointment/',views.request_appoinment,name='request_appointment'),
    path('donor_notification/',views.donor_notification,name='donor_notification'),
    path('donor_details/<int:donor_id>/', views.donor_details, name='donor_details'),






    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('search_blood/',views.search_blood,name='search_blood'),
    path('request_blood/',views.request_blood,name='request_blood'),
    path('request_update/<int:patient_id>/',views.request_update,name='request_update'),
    path('received_history/',views.received_history,name='received_history'),
    path('patient_notification/',views.patient_notification,name='patient_notification'),
    path('patient_details/<int:patient_id>/',views.patient_details,name='patient_details'),

]
