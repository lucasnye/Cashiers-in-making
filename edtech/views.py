from django.shortcuts import render

def index(request):
    return render(request, "edtech/index.html")
def real_time_transcription(request):
    return render(request, "edtech/rtt.html")

# Dyslexia formatting 
import os
import textwrap
from io import BytesIO

from django.http import FileResponse
from django.core.files.storage import FileSystemStorage

from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, HexColor

def dyslexia_format(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        uploaded_file = request.FILES['pdf']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)

        # Extract text
        reader = PdfReader(file_path)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        # Normalize
        normalized_text = ' '.join(full_text.split())

        # Convert to dyslexia-friendly PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        def init_text_object():
            p.setFillColor(HexColor("#F5F5DC"))
            p.rect(0, 0, width, height, fill=1)
            p.setFont("Helvetica", 14)
            p.setFillColor(black)
            textobject = p.beginText(50, height - 50)
            textobject.setCharSpace(1.5)
            textobject.setWordSpace(5)
            textobject.setLeading(22)
            return textobject

        textobject = init_text_object()
        for line in textwrap.wrap(normalized_text, width=90):
            if textobject.getY() < 50:
                p.drawText(textobject)
                p.showPage()
                textobject = init_text_object()
            textobject.textLine(line)

        p.drawText(textobject)
        p.showPage()
        p.save()
        buffer.seek(0)
        os.remove(file_path)

        return FileResponse(buffer, as_attachment=True, filename='dyslexia_friendly.pdf')
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

from django.shortcuts import render
import os, shutil
from django.shortcuts import render
from django.conf import settings
from .text_to_ASL import ASLVideoGenerator

def asl_converter(request):
    video_url = None
    if request.method == "POST":
        text = request.POST.get("text_input", "")
        if text:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            asset_folder = os.path.join(BASE_DIR, 'assets', 'renamed_videos')

            generator = ASLVideoGenerator(asset_folder)
            output_path = os.path.join(settings.MEDIA_ROOT, "output.mp4")
            temp_output = generator.generate_video(text, output_path="temp_output.mp4")

            if temp_output and os.path.exists(temp_output):
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                shutil.move(temp_output, output_path)
                video_url = settings.MEDIA_URL + "output.mp4"

    return render(request, "edtech/asl_converter.html", {"video_url": video_url})
