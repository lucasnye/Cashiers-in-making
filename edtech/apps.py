from django.apps import AppConfig
from faster_whisper import WhisperModel


class EdtechConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edtech'
