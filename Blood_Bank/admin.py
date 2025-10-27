from django.contrib import admin
from .models import Donation_Request, Hospital_Request, Patient, Profile, Donor,Hospital, Request_list

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'profile', 'fullname', 'age', 'blood_group', 'phonenumber', 'address', 
        'weight', 'health', 'medications', 'tattoo', 'pregnancy',
        'travel', 'lastDonation', 'is_first_time'
    ]

class DonationlistAdmin(admin.ModelAdmin):
    list_display = [
        'preferred_date','preferred_time'
    ]


class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'contact_number', 'location')

class Hospital_requestAdmin(admin.ModelAdmin):
    list_display = ('Blood_group', 'unit', 'date','urgent')

class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name','patient_gender')

class RequestlistAdmin(admin.ModelAdmin):
    list_display = ('patient', 'unit', 'date', 'urgent', 'status')



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Request_list, RequestlistAdmin)
admin.site.register(Donation_Request,DonationlistAdmin )
admin.site.register(Hospital_Request,Hospital_requestAdmin )
