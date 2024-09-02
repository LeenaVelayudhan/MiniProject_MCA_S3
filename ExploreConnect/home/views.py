from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from googletrans import Translator
from gtts import gTTS
import os
import uuid
from .models import Destination, Attraction

def continent_list(request):
    # Assuming the Destination model has a field 'continent'
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

def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    return render(request, 'destination.html', {'destination': destination})

def attraction_detail(request, pk):
    attraction = get_object_or_404(Attraction, pk=pk)
    return render(request, 'attraction_detail.html', {'attraction': attraction})

def home(request):
    # Example query using valid fields
    destinations = Destination.objects.all()  # Replace this with your actual query
    return render(request, 'home.html', {'destinations': destinations})

def language_translation(request):
    return render(request, 'language_translation.html')
def destinations(request):
    return render(request, 'destination.html')

def profile(request):
    return render(request, 'profile.html')

def logout_view(request):
    # Handle logout logic
    return render(request, 'login.html')

def translate_audio(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        input_language = request.POST.get('input_language')
        output_language = request.POST.get('output_language')

        print(f"Received input_text: {input_text}, input_language: {input_language}, output_language: {output_language}")

        if input_text and input_language and output_language:
            try:
                translator = Translator()
                translated = translator.translate(input_text, src=input_language, dest=output_language)
                translated_text = translated.text

                print(f"Translated text: {translated_text}")

                tts = gTTS(text=translated_text, lang=output_language)
                audio_filename = f"{uuid.uuid4()}.mp3"
                audio_filepath = os.path.join('media', audio_filename)
                tts.save(audio_filepath)

                return JsonResponse({
                    'translated_text': translated_text,
                    'audio_path': f'/media/{audio_filename}',
                })

            except Exception as e:
                print(f"Error during translation: {e}")
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Missing data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
