from django.shortcuts import render
from .scraper import scrape_places  # Import the scraping function

def display_places(request):
    # Call the scraping function to get the data
    places_data = scrape_places()

    # Pass the data to the template
    return render(request, 'places.html', {'places': places_data})
