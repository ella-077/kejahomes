from datetime import datetime  # timezone fixed
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ApartmentApplicationForm
from .models import ApartmentApplication, Apartment


# ---------------- STATIC PAGES ----------------
def about(request):
    return render(request, 'about.html')


def agents(request):
    return render(request, 'agents.html')


def contact(request):
    return render(request, 'contact.html')


def index(request):
    return render(request, 'index.html')


def properties(request):
    return render(request, 'properties.html')


def propertysingle(request):
    return render(request, 'property-single.html')


# ---------------- MAP VIEW ----------------
def maps(request):
    apartments = Apartment.objects.all()
    return render(request, "maps.html", {"apartments": apartments})


# ---------------- APPLY VIEW ----------------
@login_required
def apply(request):
    if request.method == 'POST':
        form = ApartmentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            messages.success(request, "Application submitted successfully!")
            return redirect('apply')  # important to avoid resubmission
    else:
        form = ApartmentApplicationForm()

    return render(request, 'apply.html', {'form': form})


# ---------------- USER APPLICATIONS ----------------
@login_required
def myapplications(request):
    """
    Admin sees all applications; normal users see only their own.
    Admin can approve/reject applications and add payment instructions.
    """
    if request.user.is_superuser:
        applications = ApartmentApplication.objects.all().order_by('-submitted_at')
    else:
        applications = ApartmentApplication.objects.filter(user=request.user).order_by('-submitted_at')

    # Handle admin POST actions
    if request.method == 'POST' and request.user.is_superuser:
        app_id = request.POST.get('application_id')
        action = request.POST.get('action')
        payment_info = request.POST.get('payment_info', '').strip()
        app = get_object_or_404(ApartmentApplication, id=app_id)

        if action == 'approve':
            app.status = 'approved'
            app.approved_at = timezone.now()
            if payment_info:
                app.payment_info = payment_info
        elif action == 'reject':
            app.status = 'rejected'

        app.save()
        messages.success(request, f"Application {app.status} successfully.")
        return redirect('my-applications')

    return render(request, 'myapplications.html', {'applications': applications})


# ---------------- PAYMENT INSTRUCTIONS ----------------
@login_required
def payment_instructions(request, app_id):
    app = get_object_or_404(ApartmentApplication, id=app_id, user=request.user)

    if app.status != 'approved':
        return render(request, 'payment_not_ready.html', {'application': app})

    return render(request, 'payment_instructions.html', {'application': app})


# ---------------- LOGIN ----------------
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# ---------------- REGISTRATION ----------------
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('index')  # redirect after successful registration

    return render(request, 'register.html')  # renders **only registration form**


# ---------------- LOGOUT ----------------
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


# ---------------- ADMIN REQUIRED DECORATOR ----------------
def admin_required(user):
    return user.is_superuser


@user_passes_test(admin_required)
def manage_applications(request):
    """
    Admin-only page to manage all applications (alternative to inline approve/reject)
    """
    applications = ApartmentApplication.objects.all().order_by('-submitted_at')

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        action = request.POST.get('action')
        application = get_object_or_404(ApartmentApplication, id=app_id)
        if action == 'approve':
            application.status = 'approved'
        elif action == 'reject':
            application.status = 'rejected'
        application.save()
        messages.success(request, f"Application {application.status}.")
        return redirect('manage_applications')

    return render(request, 'manage_applications.html', {'applications': applications})

