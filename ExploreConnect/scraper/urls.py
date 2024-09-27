from django.urls import path
from . import views

urlpatterns = [
    path('destinations/', views.destinations_view, name='destinations'),
    path('continent/<int:continent_id>/', views.filter_by_continent, name='filter_by_continent'),
    path('country/<int:country_id>/', views.country_detail_view, name='country_detail'),
]
