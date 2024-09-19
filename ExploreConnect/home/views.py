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

def continent_list(request):
    # Fetch distinct continents from the Destination model
    continents = Destination.objects.values_list('continent', flat=True).distinct()
    
    context = {
        'continents': continents,
    }
    return render(request, 'continent_list.html', context)
def destination_list(request, continent):
    destinations = Destination.objects.filter(continent=continent)
    
    context = {
        'destinations': destinations,
        'continent': continent,
    }
    return render(request, 'destination_list.html', context)

def destination_list(request, continent):
    destinations = Destination.objects.filter(continent=continent)
    return render(request, 'destination_list.html', {'destinations': destinations, 'continent': continent})


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
            input_text = request.POST.get('text', '')
            target_language = request.POST.get('language', '')

            if not input_text or not target_language:
                return JsonResponse({'error': 'Text or target language not provided'}, status=400)

            # Translate the text
            translated = translator.translate(input_text, dest=target_language)
            translated_text = translated.text

            # Convert translated text to speech
            tts = gTTS(translated_text, lang=target_language)
            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_filepath = os.path.join('media', audio_filename)
            tts.save(audio_filepath)

            # Return the path to the audio file
            return JsonResponse({
                'translated_text': translated_text,
                'audio_path': f'/media/{audio_filename}'
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



# def translate_audio(request):
#     if request.method == 'POST':
#         input_text = request.POST.get('input_text')
#         input_language = request.POST.get('input_language')
#         output_language = request.POST.get('output_language')
        
#         # Example: Call a translation function here (you would need to implement this)
#         translated_text = your_translation_function(input_text, input_language, output_language)
        
#         return JsonResponse({
#             'translated_text': translated_text,
#             'audio_path': '/path/to/translated/audio/file'
#         })
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

