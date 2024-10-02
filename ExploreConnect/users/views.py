from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Check if a user with the provided email exists
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, 'No user with this email exists.')
            return redirect('forgetpassword')

        try:
            # Attempt to get the Profile object associated with the user
            profile_obj = manageProfile.objects.get(user=user)
        except Profile.DoesNotExist:
            # Handle the case where the Profile does not exist
            messages.error(request, 'Profile for this user does not exist.')
            return redirect('forgetpassword')

        # Generate a token and save it to the profile
        token = str(uuid.uuid4())
        profile_obj.forget_password_token = token
        profile_obj.save()

        # Send an email with the password reset link
        send_forget_password_mail(user, token)
        messages.success(request, 'An email has been sent with a link to reset your password.')
        return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def confirmpassword(request, token):
    try:
        # Find the profile with the corresponding token
        profile_obj = Profile.objects.get(forgot_password_token=token)
        user = profile_obj.user

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect(f'/confirmpassword/{token}/')

            user.set_password(new_password)
            user.save()

            messages.success(request, 'Password has been reset successfully.')
            return redirect('login')

        return render(request, 'confirmpassword.html', {'token': token})

    except Profile.DoesNotExist:
        messages.error(request, 'Invalid or expired token.')
        return redirect('forgot_password')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "User created successfully.")
            return redirect('login')
       
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('/admin/')  # Redirect superuser to the admin page
            else:
                return redirect('home')  # Regular users redirect to the home page
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')

    return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout
