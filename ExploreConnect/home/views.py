from django.shortcuts import render, get_object_or_404
from .models import Destination, DestinationDetails

def home(request):
    # Fetch all distinct continents and countries
    continents = Destination.objects.values('continent').distinct()
    countries = Destination.objects.values('country', 'continent').distinct()
    return render(request, 'home.html', {'continents': continents, 'countries': countries})

def language_translation(request):
    return render(request, 'language_translation.html')

def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    # Handle logout logic
    return render(request, 'login.html')

def destination_list(request):
    # Replace with logic to retrieve destinations, possibly based on request data
    destinations = Destination.objects.all()
    return render(request, 'destination.html', {'destinations': destinations})

def destination_detail(request, pk):
    # Fetch a specific destination detail
    destination = get_object_or_404(Destination, pk=pk)
    details = get_object_or_404(DestinationDetails, destination=destination)
    return render(request, 'destination_detail.html', {'destination': destination, 'details': details})
