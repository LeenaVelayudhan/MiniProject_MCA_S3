from django.shortcuts import render, get_object_or_404
from .models import Continent, Country

def destinations_view(request):
    continents = Continent.objects.all()
    countries = Country.objects.all()
    return render(request, 'destinations.html', {'continents': continents, 'countries': countries})

def filter_by_continent(request, continent_id):
    countries = Country.objects.filter(continent_id=continent_id)
    return render(request, 'countries_list.html', {'countries': countries})

def country_detail_view(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    attractions = country.attraction_set.all()
    accommodations = country.accommodation_set.all()
    return render(request, 'country_detail.html', {
        'country': country,
        'attractions': attractions,
        'accommodations': accommodations
    })
