from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("rtt/", views.real_time_transcription, name="rtt")
]