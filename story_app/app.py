import streamlit as st
from gtts import gTTS
import os
import tempfile
from PIL import Image, UnidentifiedImageError

st.set_page_config(page_title="Storytelling App", page_icon="📖")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_story(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [scene.strip() for scene in f.read().split("\n\n") if scene.strip()]

def generate_tts(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

st.title("📖 Minimal Storytelling App")

stories_dir = os.path.join(ROOT_DIR, "stories")

st.write(f"Looking for stories in: `{stories_dir}`")

if not os.path.isdir(stories_dir):
    st.error(f"Stories folder not found at `{stories_dir}`. Please upload the 'stories' folder.")
else:
    story_files = [f for f in os.listdir(stories_dir) if f.endswith(".txt")]
    if not story_files:
        st.warning(f"No story files found in `{stories_dir}`.")
    else:
        story_choice = st.selectbox("Choose a Story:", story_files)

        if story_choice:
            story_path = os.path.join(stories_dir, story_choice)
            scenes = load_story(story_path)
            full_story = "\n\n".join(scenes)

            bg_music_path = os.path.join(ROOT_DIR, "static", "soft_music.mp3")
            if os.path.exists(bg_music_path):
                st.audio(bg_music_path, format="audio/mp3", start_time=0)

            st.write(full_story)

            if st.button("▶ Play Full Story Narration"):
                audio_file = generate_tts(full_story)
                st.write(f"Generated audio file: {audio_file} (size: {os.path.getsize(audio_file)} bytes)")
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
