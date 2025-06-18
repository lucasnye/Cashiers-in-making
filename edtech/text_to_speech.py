from gtts import gTTS
import pygame
from tempfile import NamedTemporaryFile
import os
import pdfplumber
from docx import Document

def extract_text_from_file(file_path):
    """
    Extracts and returns text from a .pdf or .docx file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: Extracted plain text.

    Raises:
        ValueError: If the file type is unsupported.
    """
    _, ext = os.path.splitext(file_path.lower())

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def text_to_speech(text):
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio = gTTS(text=text, lang='en', slow=True)
        audio.save(temp_audio.name)
    
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio.name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)