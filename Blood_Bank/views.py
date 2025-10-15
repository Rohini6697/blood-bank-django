from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

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
            form.save()
            return redirect('signin')
    else:
        form = UserForm()
    return render(request,'signup.html',{'form' : form})

#-----------------Sign In Page-----------------
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admindashboard')
            else:
                role = user.profile.role
                if role == 'patient':
                    return redirect('pateintdashboard')
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
    return render(request,'donor_dashboard.html')