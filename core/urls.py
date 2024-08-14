from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('generate-hairstyle/', views.generate_hairstyle, name='generate_hairstyle'),
]