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
from django.conf import settings
from .home import scrape_places  # Import the scraping function

def display_places(request):
    # Call the scraping function to get the data
    places = scrape_places()  # Fetch the scraped data
    return render(request, 'places.html', {'places': places})

def details(request, href):
    places = scrape_places()  # Fetch the scraped data
    place = next((p for p in places if p['href'] == href), None)
    
    if place:
        return render(request, 'places_list.html', {'place': place})
    else:
        return render(request, '404.html', status=404)

def country_details(request, href):
    places = scrape_places()  # Fetch the scraped data
    place = next((p for p in places if p['href'] == href), None)
    
    if place:
        return render(request, 'country_details.html', {'place': place})
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

def destination(request):
    destinations = Destination.objects.all()  # Replace this with your actual query
    return render(request, 'destination.html', {'destinations': destinations})


def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    attractions_by_category = {}

    # Group attractions by category
    for attraction in destination.attractions.all():
        category = attraction.get_category_display()
        if category not in attractions_by_category:
            attractions_by_category[category] = []
        attractions_by_category[category].append(attraction)

    return render(request, 'destination_detail.html', {
        'destination': destination,
        'attractions_by_category': attractions_by_category,
    })

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

