from .models import Hospital, Profile, Donor
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


            role = user.profile.role
            if role == 'patient':
                return redirect('donor_details', donor_id=profile.id)
            elif role == 'hospital':
                return redirect('hospital_details',hospital_id =profile.id )
            else:
                return redirect('signin')
            


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
    return render(request,'hospital_dashboard/hospital_dashboard.html')

def request_blood_hospital(request):
    return render(request,'hospital_dashboard/request_blood_hospital.html')

def request_history(request):
    return render(request,'hospital_dashboard/request_history.html')

def hospital_reports(request):
    return render(request,'hospital_dashboard/hospital_reports.html')

def profile_update(request):
    return render(request,'hospital_dashboard/profile_update.html')

def hospital_details(request,hospital_id):
    profile = get_object_or_404(Profile,id = hospital_id)
    hospital,created = Hospital.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        hospital.hospital_name = request.POST.get('hospital_name')
        hospital.contact_number = request.POST.get('contact')
        hospital.location = request.POST.get('location')
        hospital.save()
        return redirect('hospitaldashboard')
    return render(request,'hospital_dashboard/hospital_details.html')


#-----------------donor dashboard Page-----------------
@login_required
def donordashboard(request):
    profile = request.user.profile

    return render(request,'donor_dashboard/donor_dashboard.html',{'profile': profile})

# @login_required
@login_required
def update_donor(request, donor_id):
    # Get the Profile object
    profile = get_object_or_404(Profile, id=donor_id)
    
    # Get the linked Donor object or create one if it doesn't exist
    donor, created = Donor.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        # --- Update User model fields ---
        user = profile.user
        user.username = request.POST.get('fullname')
        user.email = request.POST.get('email')
        user.save()

        # --- Update Profile model fields ---
        profile.phonenumber = request.POST.get('phone')
        profile.age = request.POST.get('age')
        profile.blood_group = request.POST.get('bloodgroup')
        profile.address = request.POST.get('address')
        profile.save()

        # --- Update Donor model fields ---
        donor.weight = request.POST.get('weight')
        donor.health = request.POST.get('health')
        donor.heamoglobin = request.POST.get('heamoglobin')
        donor.medications = request.POST.get('medications')
        donor.tattoo = request.POST.get('tattoo')
        donor.pregnancy = request.POST.get('pregnancy')
        donor.travel = request.POST.get('travel')
        donor.systolic = request.POST.get('systolic')
        donor.diastolic = request.POST.get('diastolic')

        # Last donation and first-time checkbox
        if request.POST.get('first_time') == 'on':
            donor.is_first_time = True
            donor.lastDonation = None
        else:
            donor.is_first_time = False
            last_donation = request.POST.get('lastDonation')
            donor.lastDonation = datetime.strptime(last_donation, "%Y-%m-%d").date() if last_donation else None

        donor.save()

        return redirect('donordashboard')

    # Pass profile, user, and donor to template
    return render(request, 'donor_dashboard/update_donor.html', {
        'profile': profile,
        'user': profile.user,
        'donor': donor
    })


def donation_history(request):
    profile = request.user.profile

    return render(request,'donor_dashboard/donation _history.html',{'profile': profile})

def donor_eligibility(request):
    return render(request,'donor_dashboard/donor_eligibility.html')

def request_appoinment(request):
    profile = request.user.profile
    donor, created = Donor.objects.get_or_create(profile=profile)
    
    if request.method == 'POST':
        donor.preferred_date = request.POST.get('date')
        donor.preferred_time = request.POST.get('time')
        donor.save()

        return redirect('donordashboard')
    return render(request,'donor_dashboard/request_appointment.html',{'profile': profile})

def donor_notification(request):
    profile = request.user.profile
    return render(request,'donor_dashboard/donor_notification.html',{'profile': profile})




def donor_details(request, donor_id):
    profile = get_object_or_404(Profile, id=donor_id)
    donor, created = Donor.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        donor.fullname = request.POST.get('fullname')
        donor.age = int(request.POST.get('age')) if request.POST.get('age') else None
        donor.blood_group = request.POST.get('bloodgroup')
        donor.phonenumber = request.POST.get('phone')
        donor.address = request.POST.get('address')
        donor.weight = int(request.POST.get('weight')) if request.POST.get('weight') else None
        donor.health = request.POST.get('health')
        donor.heamoglobin = int(request.POST.get('heamoglobin')) if request.POST.get('heamoglobin') else None
        donor.medications = request.POST.get('medications')
        donor.tattoo = request.POST.get('tattoo') == 'on'
        donor.pregnancy = request.POST.get('pregnancy') == 'on'
        donor.travel = request.POST.get('travel') == 'on'
        donor.systolic = int(request.POST.get('systolic')) if request.POST.get('systolic') else None
        donor.diastolic = int(request.POST.get('diastolic')) if request.POST.get('diastolic') else None

        if request.POST.get('first_time') == 'on':
            donor.is_first_time = True
            donor.lastDonation = None
        else:
            donor.is_first_time = False
            last_donation = request.POST.get('lastDonation')
            donor.lastDonation = datetime.strptime(last_donation, "%Y-%m-%d").date() if last_donation else None

        donor.save()
        return redirect('donordashboard')

    return render(request, 'donor_dashboard/donor_details.html', {'profile': profile, 'donor': donor})
