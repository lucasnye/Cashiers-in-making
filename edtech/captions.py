from moviepy import VideoFileClip
from faster_whisper import WhisperModel


def extract_audio(input_video):
    """
    Extracts audio from a video file and saves it as a wav file.
    """
    # Dynamically generate the output file name based on the input file name
    file_name = input_video.replace(".mp4", "")
    output_audio = f"audio-{file_name}.wav"
    
    try:
        # Load the video file
        video_clip = VideoFileClip(input_video)
        
        # Extract audio and write to a wav file
        video_clip.audio.write_audiofile(output_audio)
        print(f"Audio extracted to {output_audio}")
        
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")
        
    return output_audio


def generate_transcript(audio_file, model_size="small", output_file="transcript.srt"):
    """
    Generates a transcript from an audio file using the Whisper model.
    """
    
    try:
        # Load the Whisper model
        model = WhisperModel(model_size)
        # Transcribe the audio file
        segments, info = model.transcribe(audio_file, beam_size=10)
        
        # Output transcript into srt file
        with open(output_file, "w") as srt_file:
            for i, segment in enumerate(segments):
                start, end, text = segment.start, segment.end, segment.text
                srt_file.write(f"{i + 1}\n")
                srt_file.write(f"{generate_timestamp(start)} --> {generate_timestamp(end)}\n")
                srt_file.write(f"{text}\n\n")
        print(f"Transcript generated and saved to {output_file}")
    
    except Exception as e:
        print(f"An error occurred while generating transcript: {e}")
        return None
    

def generate_timestamp(time):
    """
    Converts a time in seconds to a timestamp string in the format HH:MM:SS,ms.
    """
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = time % 60
    milliseconds = (time * 1000) % 1000
    int((time - int(time)) * 1000)
    
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(milliseconds):03}"


def main():
    extracted_audio = extract_audio("testvideo.mp4")
    generate_transcript(extracted_audio)


if __name__ == "__main__":
    main()