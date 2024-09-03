from django.urls import path
from home import views

urlpatterns = [
   # path('', views.home, name='home'),  
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('language_translation/', views.language_translation, name='language_translation'),
    path('logout/', views.logout_view, name='logout'),
    path('destinations/', views.destination, name='destination'),
    path('destination/<int:id>/', views.destination_detail, name='destination_detail'),
    path('attraction/<int:id>/', views.attraction_detail, name='attraction_detail'),
    path('translate/', views.language_translation, name='translate'),
   
]
