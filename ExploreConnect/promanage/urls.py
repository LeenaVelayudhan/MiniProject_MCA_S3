from django.urls import path
from promanage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manageprofile/', views.manageprofile, name='manageprofile'),

]

