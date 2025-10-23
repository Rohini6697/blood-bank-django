from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('donor','Donor'),
        ('patient','Patient'),
        ('hospital','Hospital')
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='donor')

    

    def __str__(self):
        return f"{self.user.username} {self.role}"
    
class Donor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=20,null=True,blank=True)
    fullname = models.CharField(max_length=40,null=True,blank=True)
    age = models.PositiveIntegerField(null=True,blank=True)
    phonenumber = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    weight = models.PositiveIntegerField(null=True,blank=True)
    health = models.CharField(max_length=100,null=True,blank=True)
    heamoglobin = models.PositiveIntegerField(null=True, blank=True)
    medications = models.CharField(max_length=10, null=True, blank=True)   
    tattoo = models.CharField(max_length=10, null=True, blank=True)        
    pregnancy = models.CharField(max_length=10, null=True, blank=True)     
    travel = models.CharField(max_length=10, null=True, blank=True)        
    lastDonation = models.DateField(null=True, blank=True)
    is_first_time = models.BooleanField(default=False)
    systolic = models.PositiveIntegerField(null=True, blank=True)
    diastolic = models.PositiveIntegerField(null=True, blank=True)

    preferred_date = models.DateField(null=True,blank=True)
    preferred_time = models.TimeField(null=True,blank=True)

    def __str__(self):
        return f"{self.fullname} {self.blood_group}"

class Hospital(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=40,null=True,blank=True)
    contact_number = models.CharField(max_length = 20,null=True,blank=True)
    location = models.CharField(max_length=40,null=True,blank=True)

    def __str__(self):
        return f"{self.hospital_name}"
    
class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=20,null=True,blank=True)
    patient_age = models.PositiveIntegerField(null=True,blank=True)
    patient_dob = models.DateField(null=True,blank=True)
    patient_gender = models.CharField(max_length=10,null=True,blank=True)
    patient_number = models.CharField(max_length=20,null=True,blank=True)
    patient_address = models.CharField(max_length=50,null=True,blank=True)
    patient_blood_group = models.CharField(max_length=10,null=True,blank=True)
    emergency_contact_name = models.CharField(max_length=20,null=True,blank=True)
    emergency_contact_number = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return f"{self.patient_name}"
    
class Request_list(models.Model):
    patient = models.OneToOneField(Patient,on_delete=models.CASCADE)
    blood = models.CharField(max_length=10,null=True,blank=True)
    unit = models.PositiveIntegerField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    reason = models.CharField(max_length=50,null=True,blank=True)
    urgency = models.BooleanField(default=False)