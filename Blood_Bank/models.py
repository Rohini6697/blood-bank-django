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
    blood_group = models.CharField(max_length=20,null=True,blank=True)
    age = models.IntegerField(max_length=3,null=True,blank=True)
    phonenumber = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    
    

    def __str__(self):
        return f"{self.user.username} {self.role}"