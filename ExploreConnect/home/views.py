from django.shortcuts import render, get_object_or_404
from .models import Destination, Attraction
from django.http import JsonResponse
from googletrans import Translator
from gtts import gTTS
import os
import uuid
from speech_recognition import Recognizer, AudioFile
import speech_recognition as sr

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

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Destination, Attraction

def destination(request):
    destinations = Destination.objects.all()  # Replace this with your actual query
    return render(request, 'destination.html', {'destinations': destinations})
def attraction_detail(request, pk):
    attraction = get_object_or_404(Attraction, id=id)
    print(attraction)
    return render(request, 'attraction_detail.html', {'attraction': attraction})
def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    print(destination)  
    return render(request, 'destination_detail.html', {'destination': destination})
def home(request):
    # Example query using valid fields
    destinations = Destination.objects.all()  # Replace this with your actual query
    return render(request, 'home.html', {'destinations': destinations})

def language_translation(request):
    return render(request, 'language_translation.html')


def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    # Handle logout logic
    return render(request, 'login.html')



def translate_audio(request):
    if request.method == 'POST':
        try:
            # Step 1: Retrieve the uploaded audio file and input/output languages
            audio_file = request.FILES.get('audio')
            input_language = request.POST.get('input_language')
            output_language = request.POST.get('output_language')

            print(f"Received input_language: {input_language}, output_language: {output_language}")

            # Ensure all required data is present
            if not audio_file or not input_language or not output_language:
                return JsonResponse({'error': 'Missing data'}, status=400)

            # Step 2: Convert audio to text using SpeechRecognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio_data = recognizer.record(source)
                input_text = recognizer.recognize_google(audio_data, language=input_language)

            print(f"Recognized input_text: {input_text}")

            # Step 3: Translate the text to the target language
            translator = Translator()
            translated = translator.translate(input_text, src=input_language, dest=output_language)
            translated_text = translated.text

            print(f"Translated text: {translated_text}")

            # Step 4: Convert the translated text to speech using gTTS
            tts = gTTS(text=translated_text, lang=output_language)
            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_filepath = os.path.join('media', audio_filename)
            tts.save(audio_filepath)

            # Step 5: Return the path to the translated audio file
            return JsonResponse({
                'translated_text': translated_text,
                'audio_path': f'/media/{audio_filename}',
            })

        except Exception as e:
            print(f"Error during translation: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
