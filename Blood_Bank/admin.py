from django.contrib import admin
from .models import Patient, Profile, Donor,Hospital, Request_list

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'profile', 'fullname', 'age', 'blood_group', 'phonenumber', 'address', 
        'weight', 'health', 'heamoglobin', 'medications', 'tattoo', 'pregnancy',
        'travel', 'lastDonation', 'is_first_time', 'systolic', 'diastolic'
    ]
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_name', 'contact_number', 'location')
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_name','patient_gender')

class RequestlistAdmin(admin.ModelAdmin):
    list_display = ('patient', 'unit', 'date', 'urgent', 'status')



admin.site.register(Profile, ProfileAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Request_list, RequestlistAdmin)
