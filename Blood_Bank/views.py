from .models import Profile
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from datetime import datetime

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

            profile = Profile.objects.create(user=user, role=form.cleaned_data['role'])

            return redirect('donor_details', donor_id=profile.id)

    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})


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
                    return redirect('patient_dashboard')
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
def patient_dashboard(request):
    return render(request,'patient_dashboard/patient_dashboard.html')

def search_blood(request):
    return render(request,'patient_dashboard/search_blood.html')

def request_blood(request):
    return render(request,'patient_dashboard/request_blood.html')

def request_status(request):
    return render(request,'patient_dashboard/request_status.html')

def received_history(request):
    return render(request,'patient_dashboard/received_history.html')

def patient_notification(request):
    return render(request,'patient_dashboard/patient_notification.html')





#-----------------hospital dashboard Page-----------------
def hospitaldashboard(request):
    return render(request,'hospital_dashboard.html')

#-----------------donor dashboard Page-----------------
@login_required
def donordashboard(request):
    profile = request.user.profile

    return render(request,'donor_dashboard/donor_dashboard.html',{'profile': profile})

# @login_required
@login_required
def update_donor(request, donor_id):
    # Get the logged-in user and profile to edit
    profile = get_object_or_404(Profile, id=donor_id)

    if request.method == 'POST':
        # Update User model fields
        user = profile.user
        user.username = request.POST.get('fullname')
        user.email = request.POST.get('email')
        user.save()

        # Update Profile model fields
        profile.phonenumber = request.POST.get('phone')
        profile.age = request.POST.get('age')
        profile.blood_group = request.POST.get('bloodgroup')
        profile.address = request.POST.get('address')
        profile.save()

        return redirect('donordashboard')

    return render(request, 'donor_dashboard/update_donor.html', {'profile': profile, 'donor': profile.user})


def donation_history(request):
    profile = request.user.profile

    return render(request,'donor_dashboard/donation _history.html',{'profile': profile})

def donor_eligibility(request):
    return render(request,'donor_dashboard/donor_eligibility.html')

def request_appoinment(request):
    profile = request.user.profile
    return render(request,'donor_dashboard/request_appointment.html',{'profile': profile})

def donor_notification(request):
    profile = request.user.profile
    return render(request,'donor_dashboard/donor_notification.html',{'profile': profile})


def donor_details(request, donor_id):
    profile = get_object_or_404(Profile, id=donor_id)

    if request.method == 'POST':
        profile.phonenumber = request.POST.get('phone')
        profile.blood_group = request.POST.get('bloodgroup')
        profile.address = request.POST.get('address')
        profile.health = request.POST.get('health')
        profile.medications = request.POST.get('medications')
        profile.tattoo = request.POST.get('tattoo')
        profile.pregnancy = request.POST.get('pregnancy')
        profile.travel = request.POST.get('travel')
        profile.fullname = request.POST.get('fullname')

        profile.age = int(request.POST.get('age')) if request.POST.get('age') else None
        profile.weight = int(request.POST.get('weight')) if request.POST.get('weight') else None
        profile.heamoglobin = int(request.POST.get('heamoglobin')) if request.POST.get('heamoglobin') else None
        profile.systolic = int(request.POST.get('systolic')) if request.POST.get('systolic') else None
        profile.diastolic = int(request.POST.get('diastolic')) if request.POST.get('diastolic') else None

        if request.POST.get('first_time') == 'on':
            profile.is_first_time = True
            profile.lastDonation = None
        else:
            profile.is_first_time = False
            last_donation = request.POST.get('lastDonation')
            profile.lastDonation = datetime.strptime(last_donation, "%Y-%m-%d").date() if last_donation else None

        profile.save()
        return redirect('donordashboard')

    return render(request, 'donor_dashboard/donor_details.html', {'profile': profile})
