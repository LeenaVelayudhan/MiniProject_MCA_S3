from django.urls import path
from .views import display_places

urlpatterns = [
    path('places/', display_places, name='places'),
]
