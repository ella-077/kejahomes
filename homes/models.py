from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User

class Apartment(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()



class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="apartments/")


class ApartmentApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # link application to logged-in user
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50)
    apartment = models.CharField(max_length=200)
    move_in_date = models.DateField()
    employment_status = models.CharField(max_length=50)
    monthly_income = models.PositiveIntegerField()
    documents = models.FileField(upload_to='applications/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    # Payment-related fields
    price = models.PositiveIntegerField(blank=True, null=True)  # set by admin after approval
    payment_info = models.TextField(blank=True, null=True)      # e.g., Mpesa or bank instructions
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.full_name} - {self.apartment}"


class ApplicationDocument(models.Model):
    application = models.ForeignKey(
        ApartmentApplication,
        on_delete=models.CASCADE,
        related_name='uploaded_documents'  # ensures reverse lookup: application.uploaded_documents.all()
    )
    file = models.FileField(upload_to='applications/')

    def __str__(self):
        return f"{self.file.name}"