from django.shortcuts import render

def index(request):
    return render(request, "edtech/index.html")
def real_time_transcription(request):
    return render(request, "edtech/rtt.html")
def dyslexia_format(request):
    return render(request, "edtech/dyslexia_upload.html")


# TTS
import os
from django.conf import settings
from django.shortcuts import render
from gtts import gTTS
from django.core.files.storage import default_storage

from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext == '.txt':
        return file.read().decode('utf-8')
    
    elif ext == '.pdf':
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    
    elif ext == '.docx':
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    else:
        raise ValueError("Unsupported file format")


def text_to_speech_view(request):
    audio_url = None

    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']

        try:
            text = extract_text_from_file(uploaded_file)

            # Generate audio file path
            audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio')
            os.makedirs(audio_dir, exist_ok=True)

            audio_path = os.path.join(audio_dir, 'output.mp3')

            # Convert text to speech
            tts = gTTS(text=text)
            tts.save(audio_path)

            # URL for frontend
            audio_url = settings.MEDIA_URL + 'audio/output.mp3'

        except Exception as e:
            return render(request, 'edtech/text_to_speech.html', {
                'error': str(e)
            })

    return render(request, 'edtech/text_to_speech.html', {
        'audio_url': audio_url
    })
