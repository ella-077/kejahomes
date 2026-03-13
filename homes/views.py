from django.shortcuts import render
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

