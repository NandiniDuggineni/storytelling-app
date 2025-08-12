import streamlit as st
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="Storytelling App", page_icon="📖")

# Detect root directory where the script runs
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_story(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [scene.strip() for scene in f.read().split("\n\n") if scene.strip()]

def generate_tts(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

st.title("📖 Minimal Storytelling App")

# Build absolute path to 'stories' folder
stories_dir = os.path.join(ROOT_DIR, "stories")

# Debug info — optional, remove if you want
st.write(f"Looking for stories in: `{stories_dir}`")

if not os.path.isdir(stories_dir):
    st.error(f"Stories folder not found at `{stories_dir}`. Please upload the 'stories' folder.")
else:
    story_files = [f for f in os.listdir(stories_dir) if f.endswith(".txt")]
    if not story_files:
        st.warning(f"No story files found in `{stories_dir}`.")
    else:
        story_choice = st.selectbox("Choose a Story:", stor_
