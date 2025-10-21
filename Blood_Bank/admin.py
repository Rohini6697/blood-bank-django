from django.contrib import admin
from .models import Profile, Donor

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

class DonorAdmin(admin.ModelAdmin):
    list_display = [
        'profile', 'fullname', 'age', 'blood_group', 'phonenumber', 'address', 
        'weight', 'health', 'heamoglobin', 'medications', 'tattoo', 'pregnancy',
        'travel', 'lastDonation', 'is_first_time', 'systolic', 'diastolic'
    ]

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Donor, DonorAdmin)
