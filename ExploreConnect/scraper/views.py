# views.py
from django.shortcuts import render
from .scraper import fetch_lonely_planet_html  # Import the function from scraper.py

def destination_list_view(request):
    # Fetch the HTML content using the function in scraper.py
    raw_html = fetch_lonely_planet_html()

    # Pass the HTML content to the template
    context = {
        'raw_html': raw_html
    }

    return render(request, 'display.html', context)
