from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def index(request):
    return render(request,'index.html')

# Registration View
def register(request):
    if request.method == "POST":
         form = UserCreationForm(request.POST)
         if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            messages.success(request, 'Registration successful.')
            return redirect('login')  # Redirect to a success page
         else:
            form = UserCreationForm()
            return render(request, 'register.html', {'form': form})
       
        
        # Check if the user already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User already exists')
                return redirect('register')

        # Create a new user
            user = User.objects.create_user(username=name, email=email, password=password, first_name=name)
            user.save()
            messages.success(request, 'User registered successfully! Please log in.')
            return redirect('login')  # Redirect to login page after registration

    return render(request, 'register.html')

# Login View
def login(request):
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')  # Redirect back to login on failure

    return render(request, 'login.html')

# Home Page View
def hello(request):
    return render(request, 'hello.html')
