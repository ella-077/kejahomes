import base64
import datetime

from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render

from keja import settings
from .models import Apartment

# Create your views here.
def about(request):
    return render(request,'about.html')
def agents(request):
    return render(request,'agents.html')
def contact(request):
    return render(request,'contact.html')
def index(request):
    return render(request,'index.html')
def properties(request):
    return render(request,'properties.html')
def propertysingle(request):
    return render(request,'property-single.html')
def maps(request):
    apartments = Apartment.objects.all()
    return render(request, "maps.html", {"apartments": apartments})

def mpesa_payment(request):

    phone = request.GET.get("phone")
    amount = request.GET.get("amount")

    if not phone or not amount:
        return JsonResponse({"error": "Phone and amount required"})

    if phone.startswith("0"):
        phone = "254" + phone[1:]

    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET

    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(auth_url, auth=(consumer_key, consumer_secret))
    access_token = r.json()['access_token']

    shortcode = "174379"
    passkey = settings.MPESA_PASSKEY

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://your-ngrok-url/mpesa/callback/",
        "AccountReference": "KejaHomes",
        "TransactionDesc": "Apartment Payment"
    }

    response = requests.post(stk_url, json=payload, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    return JsonResponse(response.json())

