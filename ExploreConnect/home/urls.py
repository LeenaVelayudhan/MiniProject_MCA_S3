from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import display_places


urlpatterns = [
   # path('', views.home, name='home'),  
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('weather/', views.Weather, name='Weather'),
    path('explore/', views.Explore, name='Explore'),
    path('hotels/', views.Hotels, name='Hotels'),
    path('search/', views.search, name='search'),
    path('thingstodo/', views.ThingstoDo, name='ThingstoDo'),  # Ensure this is correct
    path('restaurants/', views.Restaurants, name='Restaurants'),
    path('language_translation/', views.language_translation, name='language_translation'),
    path('logout/', views.logout_view, name='logout'),
   # path('scraper/places/', views.scraper, name='scraper'),
    #path('destination/', views.destination, name='destination'),  # Missing URL pattern for destination
    #path('destination/<int:id>/', views.destination_detail, name='destination_detail'),
    path('language_translation/translate_audio/', views.translate_audio, name='translate_audio'),
    path('places/', display_places, name='places'), 

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
