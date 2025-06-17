# for STT
import json
import numpy as np
import soundfile as sf
from io import BytesIO
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from faster_whisper import WhisperModel

# for dyslexia 
import os
import textwrap
from io import BytesIO
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black, HexColor
from reportlab.pdfgen import canvas
import base64
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class LiveSTTConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for live speech-to-text transcription using Faster-Whisper.
    This consumer processes audio data in chunks, transcribes it, and sends the transcription back to the client.
    It uses a byte buffer to accumulate audio data and processes it in fixed-size chunks.
    The model is loaded lazily on the first connection to optimize resource usage.
    """
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio_buffer = bytearray()
        self.sample_rate = 16000
        self.chunk_seconds = 3  # Process every 3 seconds
        self.bytes_per_chunk = int(self.sample_rate * self.chunk_seconds * 2)  # 2 bytes/sample
        self.model = None

    async def connect(self):
        await self.accept()
        # Lazy-load model on first connection
        if not hasattr(self, 'model') or self.model is None:
            self.model = WhisperModel("tiny")

    async def disconnect(self, close_code):
        self.audio_buffer.clear()

    async def receive(self, bytes_data=None, text_data=None):
        if bytes_data:
            self.audio_buffer.extend(bytes_data)
            
            # Process when we have enough audio
            while len(self.audio_buffer) >= self.bytes_per_chunk:
                chunk = self.audio_buffer[:self.bytes_per_chunk]
                self.audio_buffer = self.audio_buffer[self.bytes_per_chunk:]
                await self.process_audio_chunk(chunk)

    async def process_audio_chunk(self, chunk_bytes):
        try:
            # Convert bytes to numpy array
            audio_array = np.frombuffer(chunk_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Create in-memory WAV file
            wav_buffer = BytesIO()
            sf.write(wav_buffer, audio_array, self.sample_rate, format='WAV')
            wav_buffer.seek(0)
            
            # Transcribe using Faster-Whisper
            segments, _ = self.model.transcribe(
                wav_buffer,
                language="en",
                beam_size=5,
                vad_filter=True,
                without_timestamps=True
            )
            
            # Send transcription to client
            transcription = " ".join([segment.text for segment in segments])
            if transcription:
                await self.send(text_data=json.dumps({
                    'transcription': transcription,
                    'is_final': False
                }))
                
        except Exception as e:
            print(f"Audio processing error: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))


class DyslexiaPDFWebSocketConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pdf_buffer = BytesIO()
        self.receiving = False

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"status": "connected"}))

    async def disconnect(self, close_code):
        self.pdf_buffer.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            message = json.loads(text_data)
            if message.get("type") == "start_upload":
                self.receiving = True
                self.pdf_buffer = BytesIO()
                await self.send(text_data=json.dumps({"status": "ready_for_pdf"}))
            elif message.get("type") == "end_upload":
                self.receiving = False
                await self.handle_pdf_processing()
        elif bytes_data and self.receiving:
            self.pdf_buffer.write(bytes_data)

    async def handle_pdf_processing(self):
        self.pdf_buffer.seek(0)

        try:
            # Extract text
            reader = PdfReader(self.pdf_buffer)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"

            # Normalize spacing
            normalized_text = ' '.join(full_text.split())

            # Prepare dyslexia-friendly PDF
            output = BytesIO()
            p = canvas.Canvas(output, pagesize=letter)
            width, height = letter

            p.setFillColor(HexColor("#F5F5DC"))  # Beige background
            p.rect(0, 0, width, height, fill=1)
            p.setFont("Helvetica", 14)
            p.setFillColor(black)

            textobject = p.beginText(50, height - 50)
            textobject.setCharSpace(1.5)
            textobject.setWordSpace(5)
            textobject.setLeading(22)

            wrapped_lines = textwrap.wrap(normalized_text, width=90)
            for line in wrapped_lines:
                if textobject.getY() < 50:
                    p.drawText(textobject)
                    p.showPage()
                    p.setFillColor(HexColor("#F5F5DC"))
                    p.rect(0, 0, width, height, fill=1)
                    p.setFont("Helvetica", 14)
                    p.setFillColor(black)
                    textobject = p.beginText(50, height - 50)
                    textobject.setCharSpace(1.5)
                    textobject.setWordSpace(5)
                    textobject.setLeading(22)
                textobject.textLine(line)

            p.drawText(textobject)
            p.showPage()
            p.save()
            output.seek(0)

            # Encode and return PDF
            encoded_pdf = base64.b64encode(output.read()).decode("utf-8")
            await self.send(text_data=json.dumps({
                "status": "complete",
                "pdf_base64": encoded_pdf
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "status": "error",
                "message": str(e)
            }))
