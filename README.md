# Accessible EdTech Platform

## 🧠 Project Overview
Accessible EdTech is a Django-based web application designed to enhance accessibility in educational environments. It provides tools for converting text to speech, transcribing speech in real time, formatting documents for dyslexia, and generating ASL (American Sign Language) video sequences from text. The platform integrates natural language processing and media processing libraries to support diverse learning needs.

## 🚀 Features
- **Text-to-Speech Conversion**  
  Upload .txt, .pdf, or .docx files and convert the text into spoken audio using Google Text-to-Speech (gTTS).

- **Real-Time Transcription**  
  Transcribe spoken input live using browser-based speech recognition or server-side Whisper models.

- **Dyslexia-Friendly Formatting**  
  Reformat uploaded documents with styles optimized for dyslexic readers.

- **Text-to-ASL Video Generation**  
  Convert text into a sequence of ASL video clips using MoviePy and a preloaded video asset library.

## ⚙️ Setup Instructions
1. **Clone the Repository**
2. **Create a Virtual Environment**
3. **Install Dependencies**
4. **Apply Migrations**
5. **Run the Server**

## 🧪 Usage
1. Navigate to the homepage.
2. Use the sidebar to access each feature:
   - **Text-to-Speech**: Upload a document and listen to the generated audio.
   - **Real-Time Transcription**: Click start and begin speaking.
   - **Dyslexia Formatting**: Upload a document and view the reformatted output.
   - **ASL Converter**: Input text and generate an ASL video sequence.

## 📦 Dependencies
Key libraries used in this project include:
- Django, channels, daphne
- gTTS, faster-whisper, ctranslate2
- moviepy, imageio, pygame
- nltk, PyPDF2, pdfplumber, docx
- soundfile, numpy, requests

See `requirements.txt` for the full list.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
