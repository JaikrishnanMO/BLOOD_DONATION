from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import AdminModel,DonorModel,PatientModel
# Create your views here.

def home(request):
    return render(request,'base/Home.html')

def admin_home(request):
    return render(request, "base/AdminHome.html")

def admin_login(request):
    print("login is .......")
    if request.method=='POST':
        print("5555")
        username= request.POST['username']
        password= request.POST['password']
        user=AdminModel.objects.filter(username=username,password=password).first()
        #AdminModel(authenticate(request, username=username, password=password))
        print(user)
        if user is not None:
            return redirect(admin_home)
        else:
            print('invalidcredinals')
    return render(request,'base/AdminLogin.html') 

def donor_login(request):
    return render(request,'base/DonorLogin.html')


def patient_login(request):
    return render(request,"base/PatientLogin.html")

def donor_registration(request):
    if request.method =='POST':
        username=request.POST.get('username')
        print(username)
        email=request.POST.get('email')
        print(email)
        blood_group=request.POST.get('blood_group')
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')
        donor_obj=DonorModel(username=username,email=email,blood_group=blood_group,phone_number=phone_number,password=password)
        donor_obj.save()


    return render(request,"base/DonorRegistration.html")