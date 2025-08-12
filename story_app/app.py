import streamlit as st
from gtts import gTTS
import os
import tempfile

# --- Function to load story ---
def load_story(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().split("\n\n")  # Each paragraph = one scene

# --- Function to generate TTS ---
def generate_tts(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

# --- Streamlit App ---
st.set_page_config(page_title="Storytelling App", page_icon="📖", layout="centered")
st.title("📖 Minimal Storytelling App")
st.markdown("Enjoy simple stories with voice narration and minimal visuals.")

# Story selection
story_files = os.listdir("stories")
story_choice = st.selectbox("Choose a Story:", story_files)

if story_choice:
    story_path = os.path.join("stories", story_choice)
    scenes = load_story(story_path)

    for i, scene in enumerate(scenes):
        st.subheader(f"Scene {i+1}")
        
        # Display image if exists
        img_path = f"images/scene{i+1}.jpg"
        if os.path.exists(img_path):
            st.image(img_path, use_column_width=True)
        
        st.write(scene)

        # Generate and play TTS
        if st.button(f"▶ Play Scene {i+1}", key=f"btn{i}"):
            audio_file = generate_tts(scene)
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
