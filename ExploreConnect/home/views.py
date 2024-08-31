from django.shortcuts import render, get_object_or_404
from .models import Destination, DestinationDetails, Accommodation, DiningOption

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
    # Retrieve all destinations
    destinations = Destination.objects.all()
    return render(request, 'destination.html', {'destinations': destinations})

def destination_detail(request, pk):
    # Fetch a specific destination by its primary key (pk)
    destination = get_object_or_404(Destination, pk=pk)
    
    # Fetch associated details for the destination
    details = get_object_or_404(DestinationDetails, destination=destination)
    
    # Fetch multiple accommodations and dining options for this destination
    accommodations = Accommodation.objects.filter(destination_details=details)
    dining_options = DiningOption.objects.filter(destination_details=details)
    
    # Pass everything to the template
    return render(request, 'destination_detail.html', {
        'destination': destination,
        'details': details,
        'accommodations': accommodations,
        'dining_options': dining_options
    })
