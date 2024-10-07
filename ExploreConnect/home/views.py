from django.shortcuts import render, get_object_or_404
from .models import Destination, Attraction
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings as django_settings
from googletrans import Translator
from pydub import AudioSegment
from django.views.decorators.csrf import csrf_exempt
from gtts import gTTS
import os
import uuid
from speech_recognition import Recognizer, AudioFile
import speech_recognition as sr
from collections import defaultdict
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.conf import settings
from .home import scrape_places,scrape_best_time_to_visit # Import the scraping function
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
@csrf_exempt
def search_hotels(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        
        # You can modify the URL dynamically based on the search query (for now using Mumbai)
        url = 'https://www.tripadvisor.in/Tourism-g304554-Mumbai_Maharashtra-Vacations.html'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract hotels
        hotel_section = soup.find_all('div', class_='listing_title')
        hotels = []
        for hotel in hotel_section:
            hotel_name = hotel.text.strip()
            hotel_link = hotel.find('a')['href']
            full_link = f"https://www.tripadvisor.in{hotel_link}"
            hotels.append({'name': hotel_name, 'link': full_link})

        # Pass hotels to template
        return render(request, 'search_hotels.html', {'hotels': hotels})

    # return render(request, 'search.html')

def fetch_restaurants(place):
    # TripAdvisor Scraper API URL for searching restaurants
    url = "https://tripadvisor-scraper.p.rapidapi.com/restaurants/search"

    # Your RapidAPI key
    headers = {
        "x-rapidapi-host": "tripadvisor-scraper.p.rapidapi.com",
        "x-rapidapi-key": "YOUR_API_KEY"  # Replace with your actual API key
    }

    # Parameters for the API call
    params = {
        "query": place  # Query for searching restaurants
    }

    # Make the GET request to the TripAdvisor Scraper API
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response data as JSON
        data = response.json()
        
        # Extract relevant information (this may vary depending on the API response structure)
        restaurants = []
        for restaurant in data['restaurants']:  # Assuming the response has a 'restaurants' key
            restaurant_info = {
                'name': restaurant.get('name'),
                'image': restaurant.get('image'),  # Replace with the correct key for the image
                'details': restaurant.get('details')  # Replace with the correct key for the details
            }
            restaurants.append(restaurant_info)
        
        return restaurants
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return []  # Return an empty list on failure

    
def details(request, country, city):
    # Place details for the page
    place = {
        'destination_name': city,
        'image_url': 'example_image_url.jpg',
        'country_name': country,
        'destination_description': 'Example description.',
        'href': f'/{country}/{city}/'
    }
    attractions = [...]  # Fetch attractions as needed
    
    # Call the scraping function for "best time to visit"
    best_time_info = scrape_best_time_to_visit(city)  # Assuming 'city' contains the destination name

    return render(request, 'details.html', {
        'place': place,
        'attractions': attractions,
        'best_time_info': best_time_info,  # Pass the scraped info to the template
    })

def display_places(request):
    # Get all places (scraped data or from the database)
    places = scrape_places()  # Fetch the scraped data or use your database if necessary

    # Get the search query from the request (if any)
    search_query = request.GET.get('search', '').strip().lower()

    print(f"Search Query: {search_query}")  # Debugging

    # Filter places by search query (Country or City)
    if search_query:
        filtered_places = [
            place for place in places 
            if search_query in place.get('country_name', '').lower() or search_query in place.get('destination_name', '').lower() or search_query in place.get('continent_name', '').lower()
        ]

        print(f"Filtered Places: {filtered_places}")  # Debugging

        places = filtered_places  # Assign the filtered list to `places`

    # Sort places alphabetically by destination name (optional)
    #places = sorted(places, key=lambda x: x['destination_name'].lower())

    # Render the template with filtered places
    return render(request, 'places.html', {
        'places': places,
        'search_query': search_query  # Pass the search query back to the template
        
    })

def best_time(request, place):
    if request.method == 'POST':
        # Extract 'href' from the POST data
        href = request.POST.get('place')
        
        # Debug: print the received href
        print("Received href:", place)  # Temporary debugging print
        
        if href:
            # Call the scraping function with the extracted href
            best_time_info = scrape_best_time_to_visit(place)
            
            if best_time_info:
                return HttpResponse(f"<h1>Best Time to Visit {place}</h1><p>{best_time_info}</p>")
            else:
                return HttpResponse(f"No data available for {place}")
        else:
            return HttpResponse("Invalid destination href.")
    return HttpResponse("Invalid request method.")

def details(request, href):
    places = scrape_places()  # Fetch the scraped data
    place = next((p for p in places if p['href'] == href), None)

    if place:
        # Fetch attractions related to the place
        attractions = scrape_attractions(place['href'])

        # Pass both place and attractions to the template
        return render(request, 'places_list.html', {
            'place': place,
            'attractions': attractions  # Add this line to pass attractions to the template
        })
    else:
        return render(request, '404.html', status=404)

def scrape_attractions(place):
    base_url = 'https://www.lonelyplanet.com'
    attractions_url = f'{base_url}/{place}/attractions'  # Modify according to actual URL structure
    attractions = []

    response = requests.get(attractions_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        attraction_articles = soup.find_all('article', class_='actual-attraction-class-name')  # Replace with actual class name

        for article in attraction_articles:
            # Extract attraction name
            name_tag = article.find('h3', class_='actual-attraction-name-class')  # Replace with actual class name
            attraction_name = name_tag.text.strip() if name_tag else 'No name found'

            # Extract image URL
            img_tag = article.find('img')
            image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else 'No image found'

            # Extract additional details (e.g., description, rating, etc.)
            description_tag = article.find('p', class_='actual-attraction-description-class')  # Replace with actual class name
            attraction_description = description_tag.text.strip() if description_tag else 'No description found'
            # Extract the destination name from the href
            

            # Append the attraction data to the list
            attractions.append({
                'attraction_name': attraction_name,
                'image_url': image_url,
                'description': attraction_description,
            })

    else:
        print(f"Failed to fetch attractions: Status code {response.status_code}")

    return attractions

def country_details(request, href):
    # Fetch the scraped data for places (countries or destinations)
    places = scrape_places()
    
    # Find the specific place (country or destination) based on the href
    place = next((p for p in places if p['href'] == href), None)

    if place:
        # Fetch attractions related to the place
        attractions = scrape_attractions(place['href'])

        # Pass both place and its attractions to the template
        return render(request, 'country_details.html', {
            'place': place,
            'attractions': attractions  # Add the attractions to the context
        })
    else:
        return render(request, '404.html', status=404)


def continent_details(request, href):
    places = scrape_places()  # Fetch the scraped data
    place = next((p for p in places if p['href'] == href), None)
    
    if place:
        return render(request, 'continent_details.html', {'place': place})
    else:
        return render(request, '404.html', status=404)


def Weather(request):
    return render(request, 'Weather.html')
def Explore(request):
    return render(request, 'display.html')
def Hotels(request):
    return render(request, 'hotels.html')
def ThingstoDo(request):
    return render(request, 'thingstodo.html')
def Restaurants(request):
    return render(request, 'res.html')
def search(request):
    return render(request, 'search.html')


def home(request):

    destinations = Destination.objects.all()  # Replace this with your actual query
    return render(request, 'home.html', {'destinations': destinations})

def language_translation(request):
    return render(request, 'language_translation.html')


def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    # Handle logout logic
    return render(request, 'login.html')
@csrf_exempt
def translate_audio(request):
    if request.method == 'POST':
        try:
            translator = Translator()
            input_text = request.POST.get('input_text', '')
            output_language = request.POST.get('output_language', '')

            if not input_text or not output_language:
                return JsonResponse({'error': 'Text or target language not provided'}, status=400)

            # Translate the text
            translated = translator.translate(input_text, dest=output_language)
            translated_text = translated.text
            print(f"Translated text: {translated_text}")  # Debugging

            # Convert translated text to speech
            tts = gTTS(translated_text, lang=output_language)
            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_filepath = os.path.join(settings.MEDIA_ROOT, audio_filename)
            tts.save(audio_filepath)
            print(f"Audio_path: {audio_filepath}")

            return JsonResponse({
                
                'translated_text': translated_text,
                'audio_path': f'/media/{audio_filename}'
            })

        except Exception as e:
            print(f"Translation Error: {e}")  # Debugging
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

