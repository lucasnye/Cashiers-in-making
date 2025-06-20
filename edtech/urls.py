from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("rtt/", views.real_time_transcription, name="rtt"), 
    path("dyslexia/", views.dyslexia_format, name="dyslexia"),
    path("text_to_speech/", views.text_to_speech_view, name="text_to_speech"),
    path("asl-converter/", views.asl_converter, name="asl_converter")
    ]

