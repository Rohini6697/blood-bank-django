from django.shortcuts import redirect, render

# Create your views here.

#-----------------Home Page-----------------
def home(request):
    return render(request,'home.html')

#-----------------Sign up Page-----------------
def register(request):
    return render(request,'signup.html')

#-----------------Sign In Page-----------------
def login(request):
    return render(request,'signin.html')

#-----------------Sign In Page-----------------
def learnmore(request):
    return render(request,'learnmore.html')