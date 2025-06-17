import os
import nltk
from moviepy.editor import concatenate_videoclips, VideoFileClip
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# === CONFIGURATION ===
ASSET_FOLDER = r"C:\Users\harin\Downloads\WLASL\renamed_videos"  # <- CHANGE THIS
OUTPUT_VIDEO = "output.mp4"

# Make sure necessary NLTK packages are downloaded
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Optional: Define basic word mappings or deletion list for more accuracy
REMOVE_WORDS = set(stopwords.words('english')) - {"not", "no"}  # keep negations

# POS tags that are likely to be removed in gloss
UNNECESSARY_TAGS = {'DT', 'IN', 'CC', 'TO', 'PRP$', 'PRP', 'MD'}

def text_to_gloss(text: str) -> list:
    words = word_tokenize(text.lower())
    tagged = nltk.pos_tag(words)

    gloss_words = []
    for word, tag in tagged:
        if tag not in UNNECESSARY_TAGS and word.lower() not in REMOVE_WORDS:
            gloss_words.append(word)

    return gloss_words


# Pre-load asset filenames (lowercase, no extension)
available_words = {
    os.path.splitext(f.lower())[0].strip(): f
    for f in os.listdir(ASSET_FOLDER)
    if f.lower().endswith(".mp4")
}

def get_video_sequence(gloss_words):
    video_clips = []

    for word in gloss_words:
        clean_word = word.strip().lower()
        if clean_word in available_words:
            mp4_path = os.path.join(ASSET_FOLDER, available_words[clean_word])
            print(f"\u2714 Found full-word video: {clean_word}")
            video_clips.append(VideoFileClip(mp4_path))
        else:
            print(f"\u2718 Word video not found: {clean_word}. Breaking into characters...")
            char_clips = []
            for char in clean_word:
                if char in available_words:
                    char_path = os.path.join(ASSET_FOLDER, available_words[char])
                    print(f"\u2714 Found character video: {char}")
                    char_clips.append(VideoFileClip(char_path))
                else:
                    print(f"\u26a0 Missing character video: {char}")

            if char_clips:
                video_clips.extend(char_clips)

    return video_clips

# === STEP 3: Combine and Export Final Video ===
def generate_asl_video(text):
    gloss_words = text_to_gloss(text)
    print("\nGloss words:", gloss_words)
    clips = get_video_sequence(gloss_words)

    if clips:
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(OUTPUT_VIDEO)
        print(f"\u2705 Video created: {OUTPUT_VIDEO}")
    else:
        print("\u274c No valid clips found to generate video.")

# === ENTRY POINT ===
if __name__ == "__main__":
    user_input = input("Enter text to convert to ASL: ")
    generate_asl_video(user_input)