from django.shortcuts import render
from django.http import JsonResponse
from googletrans import Translator

def language_translation(request):
    if request.method == 'POST':
        input_language = request.POST.get('input_language')
        output_language = request.POST.get('output_language')
        translation_text = request.POST.get('translation_text')

        translator = Translator()
        translated_text = translator.translate(translation_text, src=input_language, dest=output_language).text

        return render(request, 'language_translation.html', {
            'translated_text': translated_text,
            'input_language': input_language,
            'output_language': output_language
        })
    
    return render(request, 'language_translation.html')
