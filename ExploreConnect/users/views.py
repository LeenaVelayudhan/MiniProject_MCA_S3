from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth import login
from django.contrib.auth import authenticate
def login(request):
    error_message=None
    if request.POST:

        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email,password=password)
        if user:
            return redirect('/hello')
            
        else:
            error_message='Invalid Credential'
    return render(request,'login.html')
def register(request):
    user=None
    error_message=None
    if request.POST:
        username=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        try:
             User.objects.create_user(username=username,email=email,password=password)
             return redirect('/login')
        except Exceptionas  as e:
            error_message=str(e)

    return render(request,'register.html',{'user':user})


def hello(request):
    
     return render(request,'hello.html')