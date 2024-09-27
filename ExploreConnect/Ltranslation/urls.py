from django.urls import path
from Ltranslation import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   # path('', views.home, name='home'),  
   # path('home/', views.home, name='home'),
    #path('profile/', views.profile, name='profile'),
    path('language_translation/', views.language_translation, name='language_translation'),
    #path('logout/', views.logout_view, name='logout'),
    #path('destinations/', views.destination, name='destination'),
    #path('destination/<int:id>/', views.destination_detail, name='destination_detail'),
     path('language_translation/translate_audio/', views.translate_audio, name='translate_audio'), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)