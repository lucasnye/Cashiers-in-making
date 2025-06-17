from gtts import gTTS
import pygame
from tempfile import NamedTemporaryFile

def read_text():
    with open("../../../sampleData/sample_text_for_tts.txt", "r") as text:
        content = text.read()
        return content

def text_to_speech(text):
    with NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio = gTTS(text=text, lang='en', slow=True)
        audio.save(temp_audio.name)
    
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio.name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

if __name__ == "__main__":
    pass