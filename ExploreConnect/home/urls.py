from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import display_places


urlpatterns = [
   # path('', views.home, name='home'),  
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('weather/', views.Weather, name='Weather'),
    path('explore/', views.Explore, name='Explore'),
    path('hotels/', views.Hotels, name='Hotels'),
    path('search/', views.search, name='search'),
    path('thingstodo/', views.ThingstoDo, name='ThingstoDo'),  # Ensure this is correct
    path('restaurants/', views.Restaurants, name='Restaurants'),
    path('language_translation/', views.language_translation, name='language_translation'),
    path('logout/', views.logout_view, name='logout'),
    path('language_translation/translate_audio/', views.translate_audio, name='translate_audio'),
    path('places/', views.display_places, name='places'), 
    path('details/<path:href>/', views.details, name='details'),  # Use <path:href> to allow slashes
    path('country/<path:href>/', views.country_details, name='country_details'),  # Use <path:href> to allow slashes
    path('continent/<path:href>/', views.continent_details, name='continent_details'),  # Use <path:href> to allow slashes
    path('best_time/<str:place>/', views.best_time, name='best_time'),  # The 'place' should be the destination_name
    path('fetch-tripadvisor/<str:place>/', views.fetch_restaurants, name='fetch_tripadvisor'),
    path('search_hotels/', views.search_hotels, name='search_hotels'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
