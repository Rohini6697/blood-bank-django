from .models import Profile
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login

from .forms import UserForm

# Create your views here.

#-----------------Home Page-----------------
def home(request):
    

    return render(request,'home.html')

#-----------------Sign up Page-----------------
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(user=user,role = form.cleaned_data['role'])






            # form.save()

            # Profile.objects.create()

            return redirect('signin')
    else:
        form = UserForm()
    return render(request,'signup.html',{'form' : form})

#-----------------Sign In Page-----------------
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            if user.is_superuser:
                return redirect('admindashboard')
            else:
                role = user.profile.role
                if role == 'patient':
                    return redirect('patientdashboard')
                elif role == 'hospital':
                    return redirect('hospitaldashboard')
                else:
                    return redirect('donordashboard')
        else:
            return render(request,'signin.html',{'error':'Invalid username or password'})
    return render(request,'signin.html')

#-----------------Sign In Page-----------------
def learnmore(request):
    return render(request,'learnmore.html')

#-----------------admin dashboard Page-----------------
def admindashboard(request):
    return render(request,'admin_dashboard.html')

#-----------------patient dashboard Page-----------------
def patientdashboard(request):
    return render(request,'patient_dashboard.html')

#-----------------hospital dashboard Page-----------------
def hospitaldashboard(request):
    return render(request,'hospital_dashboard.html')

#-----------------donor dashboard Page-----------------
def donordashboard(request):
    return render(request,'donor_dashboard/donor_dashboard.html')

def update_donor(request):
    
    return render(request,'donor_dashboard/update_donor.html')

def donation_history(request):
    return render(request,'donor_dashboard/donation _history.html')

def donor_eligibility(request):
    return render(request,'donor_dashboard/donor_eligibility.html')

def request_appoinment(request):
    return render(request,'donor_dashboard/request_appointment.html')