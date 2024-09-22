from django.shortcuts import render, get_object_or_404
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




def language_translation(request):
    return render(request, 'language_translation.html')

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

            return JsonResponse({
                'translated_text': translated_text,
                'audio_path': f'/media/{audio_filename}'
            })

        except Exception as e:
            print(f"Translation Error: {e}")  # Debugging
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

