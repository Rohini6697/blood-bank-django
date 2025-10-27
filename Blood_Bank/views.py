from .models import BloodStock, Donation_Request, Hospital, Hospital_Request, Patient, Profile, Donor, Request_list
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from datetime import datetime, date

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

            role = request.POST.get('role')
            Profile.objects.create(user=user, role=form.cleaned_data['role'])
            
            return redirect('signin')


            # role = user.profile.role
            # if role == 'donor':
            #     return redirect('donor_details', profile_id=profile.id)
            # if role == 'donor':
            #     if hasattr(user, 'Donor'):
            #         return redirect('donordashboard')
            #     else:
            #         return redirect('donor_details')

            # elif role == 'hospital':
            #     return redirect('hospital_details',hospital_id =profile.id )
            # elif role == 'patient':
            #     return redirect('patient_details',patient_id = profile.id )
            # else:
            #     return redirect('signin')
            


    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})


#-----------------Sign In Page-----------------
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admindashboard')
            else:
                role = user.profile.role
                if role == 'donor':
                    try:
                        donor = user.profile.donor
                        return redirect('donordashboard')
                    except Donor.DoesNotExist:
                        return redirect('donor_details', profile_id=user.profile.id)

                elif role == 'hospital':
                    try:
                        hospital = user.profile.hospital
                        return redirect('hospitaldashboard')
                    except Hospital.DoesNotExist:
                        return redirect('hospital_details', hospital_id=user.profile.id)
                elif role == 'patient':
                    try:
                        patient = user.profile.patient
                        return redirect('patient_dashboard')
                    except Patient.DoesNotExist:
                        return redirect('patient_details', patient_id=user.profile.id)
        else:
            return render(request,'signin.html',{'error':'Invalid username or password'})
    return render(request,'signin.html')

#-----------------Sign In Page-----------------
def learnmore(request):
    return render(request,'learnmore.html')

#-----------------admin dashboard Page-----------------
def admindashboard(request):
    donor = Donor.objects.all().count()
    hospital = Hospital.objects.all().count()
    patient = Patient.objects.all().count()
    return render(request,'admin_dashboard/admin_dashboard.html',{'donor':donor,'hospital':hospital,'patient':patient})


def manage_users(request):
    donoation_request = Donation_Request.objects.filter(status = 'requested').count()
    request_list = Request_list.objects.filter(status = 'requested').count()
    hospital_request = Hospital_Request.objects.filter(status = 'requested').count()
    return render(request,'admin_dashboard/manage_users.html',{
        'donoation_request':donoation_request,
        'request_list':request_list,
        'hospital_request':hospital_request
        })
    


def manage_hospitals(request):
    hospital_request = Hospital_Request.objects.all()


    return render(request,'admin_dashboard/manage_hospitals.html',{'hospital_request':hospital_request})


def manage_hospital_request(request, h_id):
    hospital_request = get_object_or_404(Hospital_Request, id=h_id)

    # Approve Request
    if request.method == "POST":
        if hospital_request.status != "approved":  # Avoid double approval
            # Get blood stock for the requested group
            blood_stock = get_object_or_404(BloodStock, blood_group=hospital_request.blood_group)

            if blood_stock.unit >= hospital_request.unit:
                blood_stock.unit -= hospital_request.unit   # Deduct stock
                blood_stock.save()

                hospital_request.status = "approved"
                hospital_request.save()

    return redirect('manage_hospitals') 

def manage_hospitals_delete(request, h_id):
    hospital_request = get_object_or_404(Hospital_Request, id=h_id)
    hospital_request.delete()
    return redirect('manage_hospitals')




def manage_donors(request):
    donation_request = Donation_Request.objects.all()
    return render(request,'admin_dashboard/manage_donors.html',{'donation_request':donation_request})

def manage_donors_update(request, h_id):
    donation_request = get_object_or_404(Donation_Request, id=h_id)
    donation_request.status = 'approved'
    donation_request.save()
    return redirect('manage_donors')

def manage_donors_delete(request, h_id):
    donation_request = get_object_or_404(Donation_Request, id=h_id)
    donation_request.delete()
    return redirect('manage_donors')



def manage_patients(request):
    request_list = Request_list.objects.all()
    return render(request,'admin_dashboard/manage_patients.html',{'request_list':request_list})

def manage_patients_update(request, h_id):
    request_list = get_object_or_404(Request_list, id=h_id)
    request_list.status = 'approved'
    request_list.save()
    return redirect('manage_patients')

def manage_patients_delete(request, h_id):
    request_list = get_object_or_404(Request_list, id=h_id)
    request_list.delete()
    return redirect('manage_patients')





def blood_stock(request):
    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        units = request.POST.get('units')

        stock,created = BloodStock.objects.get_or_create(blood_group=blood_group)

        if created:
            stock.unit = units
        else:
            stock.unit += int(units)
        stock.save()

    stocks = BloodStock.objects.all()

    return render(request,'admin_dashboard/blood_stock.html',{'stocks':stocks})




def blood_stock_update(request,id):
    blood_stock = get_object_or_404(BloodStock, id=id)
    if request.method == 'POST':
        # blood_stock.blood_group = request.POST.get('blood_group')
        blood_stock.unit = request.POST.get('units')
        blood_stock.save()
        return redirect('blood_stock')
        

    return render(request,'admin_dashboard/blood_stock_update.html',{'blood_stock':blood_stock})


def blood_stock_delete(request,id):
    blood_stock = get_object_or_404(BloodStock,id=id)
    blood_stock.delete()        
    return redirect('blood_stock')


def report_page(request):
    return render(request,'admin_dashboard/report_page.html')


import matplotlib
matplotlib.use('Agg')  # Use backend for no GUI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import Profile, Donor, Hospital, Patient, Request_list, Hospital_Request

def generate_graph(x, y, title, xlabel, ylabel):
    plt.figure(figsize=(5, 3))
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

def report_page(request):
    # Total counts
    total_donors = Donor.objects.count()
    total_hospitals = Hospital.objects.count()
    total_patients = Patient.objects.count()
    total_requests = Request_list.objects.count()

    # 2️⃣ Blood Stock (Example Static — Replace with your BloodStock Model later)
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    units = [10, 5, 12, 7, 15, 6, 4, 3]  # Replace with real data from Blood Stock model
    blood_stock_graph = generate_graph(blood_groups, units, 'Blood Stock by Type', 'Blood Group', 'Units')

    # 3️⃣ Donors per Blood Group
    groups = []
    donor_counts = []
    for group in blood_groups:
        count = Donor.objects.filter(blood_group=group).count()
        groups.append(group)
        donor_counts.append(count)
    donor_graph = generate_graph(groups, donor_counts, 'Donors by Blood Group', 'Blood group', 'Number')

    # 5️⃣ Requests (Approved / Rejected / Pending)
    statuses = ['approved', 'rejected', 'requested']
    status_counts = [
        Hospital_Request.objects.filter(status='approved').count() + Request_list.objects.filter(status='approved').count(),
        Hospital_Request.objects.filter(status='rejected').count() + Request_list.objects.filter(status='rejected').count(),
        Hospital_Request.objects.filter(status='requested').count() + Request_list.objects.filter(status='requested').count(),
    ]
    request_status_graph = generate_graph(statuses, status_counts, 'Request Status Overview', 'Status', 'Count')

    return render(request, 'admin_dashboard/report_page.html', {
        'total_donors': total_donors,
        'total_hospitals': total_hospitals,
        'total_patients': total_patients,
        'total_requests': total_requests,
        'blood_stock_graph': blood_stock_graph,
        'donor_graph': donor_graph,
        'request_status_graph': request_status_graph,
    })




#-----------------patient dashboard Page-----------------
def patient_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    patient = Patient.objects.filter(profile=profile).first() 
    return render(request,'patient_dashboard/patient_dashboard.html',{'patient': patient})

def search_blood(request):
    profile = get_object_or_404(Profile, user=request.user)
    patient = Patient.objects.filter(profile=profile).first() 




    return render(request,'patient_dashboard/search_blood.html',{'patient': patient})

def request_blood(request):
    profile = Profile.objects.get(user=request.user)
    patient = Patient.objects.get(profile=profile)

    # requestlist = get_object_or_404(Request_list)
    # requestlist = 

    if request.method == 'POST':
        units = request.POST.get('units')
        required_date = request.POST.get('required_date')
        urgent = request.POST.get('urgent') == 'on'
        reason = request.POST.get('reason')


        if urgent:
            request_date = date.today()  # current date for urgent requests
        else:
            required_date = request.POST.get('required_date')
            if required_date:
                request_date = datetime.strptime(required_date, "%Y-%m-%d").date()
            else:
                request_date = None 






        Request_list.objects.create(
            patient=patient,
            unit = units,
            date = request_date,
            urgent = urgent,
            reason = reason
        )

        
        return redirect('received_history')

    return render(request,'patient_dashboard/request_blood.html',{'patient': patient})

def request_update(request):
    # patient = get_object_or_404(Patient,id=patient_id)
    profile = Profile.objects.get(user = request.user)
    patient = Patient.objects.get(profile=profile)
    if request.method == 'POST':
        patient.patient_name = request.POST.get('fullName')
        patient.patient_age = request.POST.get('age')
        patient.patient_dob = request.POST.get('dob')
        patient.patient_gender = request.POST.get('gender')
        patient.patient_number = request.POST.get('contact')
        patient.patient_address = request.POST.get('address')
        patient.patient_blood_group = request.POST.get('bloodGroup')
        patient.emergency_contact_name = request.POST.get('emergencyContact')
        patient.patient_name = request.POST.get('fullName')
        patient.emergency_contact_number = request.POST.get('emergencyNumber')

        patient.save()
        return redirect('received_history')


    return render(request,'patient_dashboard/request_update.html',{'patient':patient})

def received_history(request):
    profile = Profile.objects.get(user=request.user)
    patient = Patient.objects.get(profile=profile)
    request_list = Request_list.objects.filter(patient = patient)

    return render(request,'patient_dashboard/received_history.html',{'patient': patient,'request_list':request_list})

def patient_notification(request):
    profile = get_object_or_404(Profile, user=request.user)
    patient = Patient.objects.filter(profile=profile).first() 
    return render(request,'patient_dashboard/patient_notification.html',{'patient': patient})

def patient_details(request,patient_id):
    profile = get_object_or_404(Profile,id = patient_id)
    patient,created = Patient.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        patient.patient_name = request.POST.get('fullName')
        patient.patient_age = int(request.POST.get('age')) if request.POST.get('age') else None
        patient.patient_dob = request.POST.get('dob')
        patient.patient_gender = request.POST.get('gender')
        patient.patient_number = request.POST.get('contact')
        patient.patient_address = request.POST.get('address')
        patient.patient_blood_group = request.POST.get('bloodGroup')
        patient.emergency_contact_name = request.POST.get('emergencyContact')
        patient.emergency_contact_number = request.POST.get('emergencyNumber')
        patient.save()
        return redirect('patient_dashboard')


    return render(request,'patient_dashboard/patient_details.html',{'patient':patient,'profile':profile})





#-----------------hospital dashboard Page-----------------
def hospitaldashboard(request):
    profile = request.user.profile
    hospital = get_object_or_404(Hospital, profile=profile)
    return render(request,'hospital_dashboard/hospital_dashboard.html',{'hospital':hospital})

from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Hospital, Hospital_Request

def request_blood_hospital(request):
    profile = request.user.profile
    hospital = Hospital.objects.filter(profile=profile).first()

    if not hospital:
        return render(request, 'hospital_dashboard/request_blood_hospital.html', {
            'error': 'No hospital is associated with this profile.'
        })

    if request.method == 'POST':
        Blood_group = request.POST.get('blood_group')
        unit = request.POST.get('units')
        urgent = request.POST.get('urgent') == 'on'

        if urgent:
            request_date = date.today()  # ✅ Correct
        else:
            required_date = request.POST.get('date')
            request_date = datetime.strptime(required_date, "%Y-%m-%d").date() if required_date else None

        Hospital_Request.objects.create(
            hospital=hospital,
            Blood_group=Blood_group,
            unit=unit,
            date=request_date,
            urgent=urgent
        )

        return redirect('request_history')

    return render(request, 'hospital_dashboard/request_blood_hospital.html', {'hospital': hospital})


def request_history(request):
    profile = request.user.profile
    hospital = get_object_or_404(Hospital, profile=profile)
    request_history = Hospital_Request.objects.filter(hospital=hospital)

    return render(request, 'hospital_dashboard/request_history.html', {
        'hospital': hospital,
        'request_history': request_history
    })

def hospital_reports(request):
    profile = request.user.profile
    hospital = get_object_or_404(Hospital, profile=profile)
    return render(request,'hospital_dashboard/hospital_reports.html',{'hospital':hospital})

def profile_update(request,hospital_id):
    hospital = get_object_or_404(Hospital,id=hospital_id)


    return render(request,'hospital_dashboard/profile_update.html',{'hospital':hospital})


def hospital_details(request, hospital_id):
    # hospital = get_object_or_404(Hospital, id=hospital_id)
    # profile = get_object_or_404(Profile,id = hospital_id)
    # hospital,created = Hospital.objects.get_or_create(profile=profile)
    profile = Profile.objects.get(user = request.user)
    hospital, created = Hospital.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        hospital.hospital_name = request.POST.get('hospital_name')
        hospital.contact_number = request.POST.get('contact')
        hospital.location = request.POST.get('location')
        hospital.save()
        return redirect('hospitaldashboard')

    return render(request, 'hospital_dashboard/hospital_details.html', {'hospital': hospital})
#-----------------donor dashboard Page-----------------
@login_required
def donordashboard(request):
    # Ensure the profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Ensure the donor exists
    donor, created = Donor.objects.get_or_create(profile=profile)

    return render(request, 'donor_dashboard/donor_dashboard.html', {
        'profile': profile,
        'donor': donor
    })
# @login_required
@login_required
def update_donor(request, donor_id):
    # Get the Donor first
    donor = get_object_or_404(Donor, id=donor_id)
    profile = donor.profile  # Get the related profile
    user = profile.user      # Get the related user

    if request.method == 'POST':
        # --- Update User model fields ---
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
        donor.tattoo = request.POST.get('tattoo') == 'on'
        donor.pregnancy = request.POST.get('pregnancy') == 'on'
        donor.travel = request.POST.get('travel') == 'on'
        donor.systolic = int(request.POST.get('systolic')) if request.POST.get('systolic') else None
        donor.diastolic = int(request.POST.get('diastolic')) if request.POST.get('diastolic') else None

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

    return render(request, 'donor_dashboard/update_donor.html', {
        'profile': profile,
        'user': user,
        'donor': donor
    })

# def update_donor(request, donor_id):
#     # Get the Profile object
#     profile = get_object_or_404(Profile, id=donor_id ,role='hospital')
    
#     try:
#         hospital = Hospital.objects.get(profile=profile)
#     except Hospital.DoesNotExist:
#         # Handle the case if the hospital object is missing
#         hospital = None 
    
#     # Get the linked Donor object or create one if it doesn't exist
#     donor, created = Donor.objects.get_or_create(profile=profile)

#     if request.method == 'POST':
#         # --- Update User model fields ---
#         user = profile.user
#         user.username = request.POST.get('fullname')
#         user.email = request.POST.get('email')
#         user.save()

#         # --- Update Profile model fields ---
#         profile.phonenumber = request.POST.get('phone')
#         profile.age = request.POST.get('age')
#         profile.blood_group = request.POST.get('bloodgroup')
#         profile.address = request.POST.get('address')
#         profile.save()

#         # --- Update Donor model fields ---
#         donor.weight = request.POST.get('weight')
#         donor.health = request.POST.get('health')
#         donor.heamoglobin = request.POST.get('heamoglobin')
#         donor.medications = request.POST.get('medications')
#         donor.tattoo = request.POST.get('tattoo')
#         donor.pregnancy = request.POST.get('pregnancy')
#         donor.travel = request.POST.get('travel')
#         donor.systolic = request.POST.get('systolic')
#         donor.diastolic = request.POST.get('diastolic')

#         # Last donation and first-time checkbox
#         if request.POST.get('first_time') == 'on':
#             donor.is_first_time = True
#             donor.lastDonation = None
#         else:
#             donor.is_first_time = False
#             last_donation = request.POST.get('lastDonation')
#             donor.lastDonation = datetime.strptime(last_donation, "%Y-%m-%d").date() if last_donation else None

#         donor.save()

#         return redirect('donordashboard')

#     # Pass profile, user, and donor to template
#     return render(request, 'donor_dashboard/update_donor.html', {
#         'profile': profile,
#         'user': profile.user,
#         'donor': donor
#     })

def donation_history(request):
    profile = request.user.profile
    donor = Donor.objects.get(profile=profile)

    donation = Donation_Request.objects.filter(donor = donor)
    
    return render(request, 'donor_dashboard/donation_history.html', {
        'profile': profile,
        'donor': donor,
        'donation':donation
    })

# def donation_history(request):
#     profile = request.user.profile
#     donor, created = Donor.objects.get_or_create(profile=profile)

#     return render(request,'donor_dashboard/donation_history.html', {
#         'profile': profile,
#         'donor': donor
#     })


def request_appointment(request):
    # person = Donation_Request.objects.get(user = request.user)
    profile = Profile.objects.get(user = request.user)
    donor = Donor.objects.get(profile=profile)
    if request.method == 'POST':
        
        date = request.POST.get('date')
        time = request.POST.get('time')

        Donation_Request.objects.create(
            donor=donor,
            preferred_date = date,
            preferred_time = time
        )
        return redirect('donation_history')
    return render(request, 'donor_dashboard/request_appointment.html',{'donor': donor})

# def request_appointment(request):
#     profile = get_object_or_404(Profile, user=request.user)

#     donor, created = Donor.objects.get_or_create(profile=profile)

#     update_url = f"/update_donor/{donor.id}/" 

#     if request.method == 'POST':
#         preferred_date = request.POST.get('preferred_date')
#         preferred_time = request.POST.get('preferred_time')

#         return redirect('donordashboard')

#     return render(request, 'donor_dashboard/request_appointment.html', {
#         'profile': profile,
#         'donor': donor,
#         'update_url': update_url
#     })

# def request_appoinment(request):
#     profile = request.user.profile
#     donor, created = Donor.objects.get_or_create(profile=profile)
    
#     if request.method == 'POST':
#         donor.preferred_date = request.POST.get('date')
#         donor.preferred_time = request.POST.get('time')
#         donor.save()

#         return redirect('donordashboard')
#     return render(request,'donor_dashboard/request_appointment.html',{'profile': profile})
def donor_notification(request):
    # Get the profile of the logged-in user
    profile = get_object_or_404(Profile, user=request.user)

    # Get or create the Donor object
    donor, created = Donor.objects.get_or_create(profile=profile)

    # Now donor.id is guaranteed to exist
    update_url = f"/update_donor/{donor.id}/"  # or use: reverse('update_donor', args=[donor.id])

    # Fetch notifications here if you have a model for it
    notifications = []  # replace with actual query

    return render(request, 'donor_dashboard/donor_notification.html', {
        'profile': profile,
        'donor': donor,
        'update_url': update_url,
        'notifications': notifications
    })




def donor_details(request, profile_id):  # use profile_id
    # Get the Profile first
    profile = get_object_or_404(Profile, id=profile_id)

    # Get or create the Donor linked to this Profile
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

    return render(request, 'donor_dashboard/donor_details.html', {
        'profile': profile,
        'donor': donor
    })
