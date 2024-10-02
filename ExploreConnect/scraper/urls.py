# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('destinations/', views.destination_list_view, name='destination_list'),
]
