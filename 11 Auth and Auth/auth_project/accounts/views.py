from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import CustomUserCreationForm
from .models import CustomUser
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    if request.user.role == 'admin':
        users = CustomUser.objects.all()
    elif request.user.role == 'manager':
        users = CustomUser.objects.filter(role='employee')
    else:
        users = None
    return render(request, 'accounts/dashboard.html', {'users': users})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    subject = "Verify Your Email - Django Auth System"
    message = f"Click the link below to verify your email:\n\n"
    message += f"http://127.0.0.1:8000/accounts/verify-email/{user.email_verification_token}/"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Disable login until verified
            user.save()
            send_verification_email(user)
            return render(request, 'accounts/email_verification_sent.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        user.is_verified = True
        user.is_active = True
        user.save()
        return redirect('login')
    except CustomUser.DoesNotExist:
        return render(request, 'accounts/email_verification_failed.html')
