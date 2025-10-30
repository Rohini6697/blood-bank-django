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
    blood_stock = BloodStock.objects.all().count()
    return render(request,'admin_dashboard/admin_dashboard.html',{'donor':donor,'hospital':hospital,'patient':patient,'blood_stock':blood_stock})


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






def manage_hospitals_update(request, h_id):
    hospital_request = get_object_or_404(Hospital_Request, id=h_id)

    # Prevent double approval
    if hospital_request.status == 'approved':
        return redirect('manage_hospitals')

    # ✅ Correct field names
    blood_group = hospital_request.Blood_group
    requested_units = hospital_request.unit

    # ✅ Get the stock for this blood group
    stock = get_object_or_404(BloodStock, blood_group=blood_group)

    # ✅ Check and reduce stock
    if stock.unit >= requested_units:
        stock.unit -= requested_units
        stock.save()

        hospital_request.status = 'approved'
        hospital_request.save()

    else:
        # Not enough stock — optional message or status change
        hospital_request.status = 'rejected'
        hospital_request.save()

    
    return redirect('manage_hospitals')


def manage_hospitals_delete(request, h_id):
    hospital_request = get_object_or_404(Hospital_Request, id=h_id)
    hospital_request.delete()
    return redirect('manage_hospitals')




from datetime import date

def manage_donors(request):
    donation_request = Donation_Request.objects.select_related('donor').all()

    # Calculate eligibility and attach to donor
    for req in donation_request:
        donor = req.donor
        age = donor.age or 0
        weight = donor.weight or 0

        if donor.lastDonation:
            days_difference = (date.today() - donor.lastDonation).days
        else:
            days_difference = 9999  # default large number if never donated

        if (
            age < 18 or age > 60 or weight < 50
            or donor.health == "yes" or donor.medications == "yes"
            or donor.tattoo == "yes" or donor.pregnancy == "yes"
            or days_difference < 35
        ):
            req.eligibility = 'Not Eligible'
        else:
            req.eligibility = 'Eligible'

    return render(request, 'admin_dashboard/manage_donors.html', {'donation_request': donation_request})

# def manage_donors_update(request, h_id):
#     donation_request = get_object_or_404(Donation_Request, id=h_id)
#     donation_request.status = 'approved'
#     donation_request.save()
#     return redirect('manage_donors')




def accept_donor(request,h_id):
    donation_request = get_object_or_404(Donation_Request, id=h_id)
    # donation = Donation_Request.objects.all()

    # Prevent re-accepting a donor
    if donation_request.status == 'approved':
        return render(request, 'admin_dashboard/accept_donor.html', {
            'donation_request': donation_request,
            'already_approved': True
        })


    if request.method == "POST":
        appointment_date = request.POST.get("appointment_date")
        appointment_time = request.POST.get("appointment_time")

        # Save appointment info
        donation_request.appointment_date = appointment_date
        donation_request.appointment_time = appointment_time
        donation_request.status = "approved"
        donation_request.save()

        return redirect('manage_donors')

    
    return render(request,'admin_dashboard/accept_donor.html',{'donation_request':donation_request})












def manage_donors_update(request, h_id):
    donation_request = get_object_or_404(Donation_Request, id=h_id)

    # Prevent double approval
    if donation_request.status == 'donated':
        return redirect('manage_donors')

    # ✅ Correct field names
    blood_group = donation_request.donor.blood_group
    requested_units = 1

    # ✅ Get the stock for this blood group
    stock = get_object_or_404(BloodStock, blood_group=blood_group)

    # ✅ Check and reduce stock
    if stock.unit >= requested_units:
        stock.unit += requested_units
        stock.save()

        donation_request.status = 'donated'
        donation_request.save()

    else:
        # Not enough stock — optional message or status change
        donation_request.status = 'rejected'
        donation_request.save()

    return redirect('manage_donors')










def manage_donors_delete(request, h_id):
    donation_request = get_object_or_404(Donation_Request, id=h_id)
    donation_request.delete()
    return redirect('manage_donors')



def manage_patients(request):
    request_list = Request_list.objects.all()

    return render(request,'admin_dashboard/manage_patients.html',{'request_list':request_list})

from django.shortcuts import get_object_or_404, redirect
from .models import Request_list, BloodStock

def manage_patients_update(request, h_id):
    request_list = get_object_or_404(Request_list, id=h_id)

    # Take patient and their blood group
    patient = request_list.patient
    blood_group = patient.patient_blood_group
    units_requested = request_list.unit
    
    # Get stock for this blood group
    blood_stock = get_object_or_404(BloodStock, blood_group=blood_group)

    # If already approved, don’t reduce again
    if request_list.status == 'approved':
        return redirect('manage_patients')
    
    # Check if enough stock exists
    if blood_stock.unit >= units_requested:
        blood_stock.unit -= units_requested
        blood_stock.save()

        request_list.status = 'approved'
        request_list.save()
    else:
        request_list.status = 'rejected'
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
matplotlib.use('Agg')  # For non-GUI (server environment)

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render
from .models import Donor, Hospital, Patient, Request_list, Hospital_Request, BloodStock


def generate_bar_graph(x, y, title, xlabel, ylabel):
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
    plt.close()
    return base64.b64encode(image_png).decode('utf-8')


def generate_pie_chart(labels, sizes, title):
    plt.figure(figsize=(5, 3))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)  # Pie Chart
    plt.title(title)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    return base64.b64encode(image_png).decode('utf-8')


def report_page(request):
    # Total Counts
    total_donors = Donor.objects.count()
    total_hospitals = Hospital.objects.count()
    total_patients = Patient.objects.count()
    total_requests = Request_list.objects.count()

    # 1️⃣ Blood Stock - PIE CHART
    blood_stock = BloodStock.objects.all()
    blood_groups = [stock.blood_group for stock in blood_stock]
    units = [stock.unit for stock in blood_stock]
    blood_stock_graph = generate_pie_chart(blood_groups, units, 'Blood Stock Distribution')

    # 2️⃣ Donors Per Blood Group - BAR
    groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    donor_counts = [Donor.objects.filter(blood_group=group).count() for group in groups]
    donor_graph = generate_bar_graph(groups, donor_counts, 'Donors by Blood Group', 'Blood Group', 'Count')

    # 3️⃣ Status of Requests - BAR
    statuses = ['approved', 'rejected', 'requested']
    status_counts = [
        Hospital_Request.objects.filter(status='approved').count() + Request_list.objects.filter(status='approved').count(),
        Hospital_Request.objects.filter(status='rejected').count() + Request_list.objects.filter(status='rejected').count(),
        Hospital_Request.objects.filter(status='requested').count() + Request_list.objects.filter(status='requested').count(),
    ]
    request_status_graph = generate_bar_graph(statuses, status_counts, 'Request Status Overview', 'Status', 'Count')

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









import io
import base64
import matplotlib.pyplot as plt
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from .models import Hospital, Hospital_Request, BloodStock

def hospital_reports(request):
    # ✅ Fixed line here
    hospital = get_object_or_404(Hospital, profile=request.user.profile)

    # 🩸 Blood stock data
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    stocks = [
        getattr(hospital, 'a_pos', 0),
        getattr(hospital, 'a_neg', 0),
        getattr(hospital, 'b_pos', 0),
        getattr(hospital, 'b_neg', 0),
        getattr(hospital, 'ab_pos', 0),
        getattr(hospital, 'ab_neg', 0),
        getattr(hospital, 'o_pos', 0),
        getattr(hospital, 'o_neg', 0),
    ]

    # 📊 Status data
    status_counts = Hospital_Request.objects.filter(hospital=hospital).values('status').annotate(count=Count('id'))
    statuses = [s['status'] for s in status_counts]
    totals = [s['count'] for s in status_counts]

    # ✅ Summary counts
    total_requests = sum(totals)
    approved = next((s['count'] for s in status_counts if s['status'] == 'approved'), 0)
    rejected = next((s['count'] for s in status_counts if s['status'] == 'rejected'), 0)
    pending = next((s['count'] for s in status_counts if s['status'] == 'pending'), 0)

    charts = []

    # ---------- 1️⃣ PIE CHART ----------
    plt.figure(figsize=(4, 4))
    plt.pie(stocks, labels=blood_groups, autopct='%1.1f%%', startangle=90)
    plt.title('Blood Stock Distribution')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    charts.append('data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode())
    buffer.close()

    # ---------- 2️⃣ BAR CHART ----------
    plt.figure(figsize=(6, 4))
    plt.bar(blood_groups, stocks)
    plt.title('Blood Units Available per Group')
    plt.xlabel('Blood Group')
    plt.ylabel('Units')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    charts.append('data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode())
    buffer.close()

    # ---------- 3️⃣ STATUS CHART ----------
    plt.figure(figsize=(5, 4))
    plt.bar(statuses, totals, color=['#6FA8DC', '#FFD966', '#E06666'])
    plt.title('Request Status Summary')
    plt.xlabel('Status')
    plt.ylabel('Number of Requests')
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    charts.append('data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode())
    buffer.close()

    blood_data = [
        ('A+', hospital.a_pos),
        ('A-', hospital.a_neg),
        ('B+', hospital.b_pos),
        ('B-', hospital.b_neg),
        ('AB+', hospital.ab_pos),
        ('AB-', hospital.ab_neg),
        ('O+', hospital.o_pos),
        ('O-', hospital.o_neg),
    ]



    context = {
        'hospital': hospital,
        'charts': charts,
        'total_requests': total_requests,
        'approved': approved,
        'rejected': rejected,
        'pending': pending,
        'blood_data': blood_data,
    }

    return render(request, 'hospital_dashboard/hospital_reports.html', context)















def profile_update(request,hospital_id):
    hospital = get_object_or_404(Hospital,id=hospital_id)


    return render(request,'hospital_dashboard/profile_update.html',{'hospital':hospital})


def hospital_details(request, hospital_id):
    profile = Profile.objects.get(user=request.user)
    hospital, created = Hospital.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        # Basic hospital info
        hospital.hospital_name = request.POST.get('hospital_name')
        hospital.contact_number = request.POST.get('contact')
        hospital.location = request.POST.get('location')

        # 🩸 Blood stock info
        hospital.a_pos = request.POST.get('a_pos') or 0
        hospital.a_neg = request.POST.get('a_neg') or 0
        hospital.b_pos = request.POST.get('b_pos') or 0
        hospital.b_neg = request.POST.get('b_neg') or 0
        hospital.ab_pos = request.POST.get('ab_pos') or 0
        hospital.ab_neg = request.POST.get('ab_neg') or 0
        hospital.o_pos = request.POST.get('o_pos') or 0
        hospital.o_neg = request.POST.get('o_neg') or 0

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
    profile = get_object_or_404(Profile, user=request.user)
    donor, created = Donor.objects.get_or_create(profile=profile)
    update_url = f"/update_donor/{donor.id}/"  # or use: reverse('update_donor', args=[donor.id])
    notifications = []


    

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
