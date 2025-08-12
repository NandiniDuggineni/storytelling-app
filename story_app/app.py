import streamlit as st
from gtts import gTTS
import os
import tempfile

st.set_page_config(page_title="Storytelling App", page_icon="📖")

def load_story(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [scene.strip() for scene in f.read().split("\n\n") if scene.strip()]

def generate_tts(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

st.title("📖 Minimal Storytelling App")

story_files = os.listdir("stories")
story_choice = st.selectbox("Choose a Story:", story_files)

if story_choice:
    story_path = os.path.join("stories", story_choice)
    scenes = load_story(story_path)

    # Optionally play background music (if exists)
    bg_music_path = "static/soft_music.mp3"
    if os.path.exists(bg_music_path):
        st.audio(bg_music_path, format="audio/mp3", start_time=0)

    for i, scene in enumerate(scenes):
        st.subheader(f"Scene {i+1}")

        img_path = f"static/scene{i+1}.jpg"
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)

        st.write(scene)

        if st.button(f"▶ Play Narration Scene {i+1}", key=f"play_{i}"):
            audio_file = generate_tts(scene)
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
