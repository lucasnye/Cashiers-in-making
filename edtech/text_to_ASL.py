import os, nltk
from moviepy.editor import concatenate_videoclips, VideoFileClip
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('stopwords')

class ASLVideoGenerator:
    def __init__(self, asset_folder, output_video="output.mp4"):
        self.asset_folder = asset_folder
        self.output_video = output_video
        self.REMOVE_WORDS = set(stopwords.words('english')) - {"not", "no"}
        self.UNNECESSARY_TAGS = {'DT','IN','CC','TO','PRP$','PRP','MD'}
        self.available_words = {
            os.path.splitext(f.lower())[0].strip(): f
            for f in os.listdir(self.asset_folder)
            if f.lower().endswith(".mp4")
        }

    def text_to_gloss(self, text):
        words = word_tokenize(text.lower())
        tagged = nltk.pos_tag(words)
        return [w for w,t in tagged if t not in self.UNNECESSARY_TAGS and w not in self.REMOVE_WORDS]

    def get_video_sequence(self, gloss_words):
        clips = []
        for w in gloss_words:
            lw = w.strip().lower()
            if lw in self.available_words:
                clips.append(VideoFileClip(os.path.join(self.asset_folder, self.available_words[lw])))
            else:
                for c in lw:
                    if c in self.available_words:
                        clips.append(VideoFileClip(os.path.join(self.asset_folder, self.available_words[c])))
        return clips

    def generate_video(self, text, output_path=None):
        gloss = self.text_to_gloss(text)
        clips = self.get_video_sequence(gloss)
        if not clips:
            return None
        final = concatenate_videoclips(clips, method="compose")
        out = output_path or self.output_video
        final.write_videofile(out)
        return out
