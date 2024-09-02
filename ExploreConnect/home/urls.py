from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL points to the home view
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('language_translation/', views.language_translation, name='language_translation'),
    path('logout/', views.logout_view, name='logout'),
    path('destinations/', views.continent_list, name='continent_list'),
    path('destinations/<str:continent>/', views.destination_list, name='destination_list'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('attraction/<int:pk>/', views.attraction_detail, name='attraction_detail'),
    path('language-translation/', views.language_translation, name='language_translation'),
    path('translate/', views.language_translation, name='translate'),
   
]
