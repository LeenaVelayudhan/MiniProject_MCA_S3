from django.urls import path
from promanage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('language_translation/', views.language_translation, name='language_translation'),
    path('language_translation/translate_audio/', views.translate_audio, name='translate_audio'), 
]

