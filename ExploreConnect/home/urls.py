from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL points to the home view
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('language_translation/', views.language_translation, name='language_translation'),
    path('logout/', views.logout_view, name='logout'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destination/<int:pk>/', views.destination_detail, name='destination_detail'),
]
