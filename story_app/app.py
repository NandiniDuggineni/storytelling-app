import streamlit as st
from gtts import gTTS
from pydub import AudioSegment
import os
import tempfile

# --- Function to load story ---
def load_story(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().split("\n\n")  # Each paragraph = one scene

# --- Function to mix narration with background music ---
def mix_audio(narration_file, music_file, output_file):
    narration = AudioSegment.from_file(narration_file)
    music = AudioSegment.from_file(music_file)

    # Lower background music volume
    music = music - 15  # dB

    # Match music length to narration
    if len(music) < len(narration):
        music = music * (len(narration) // len(music) + 1)

    music = music[:len(narration)]

    # Overlay music and narration
    combined = music.overlay(narration)
    combined.export(output_file, format="mp3")

# --- Function to generate TTS with background music ---
def generate_tts_with_music(text, music_path, lang="en"):
    # Create narration file
    tts = gTTS(text=text, lang=lang)
    narration_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    tts.save(narration_file)

    # Output final audio file
    output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
    mix_audio(narration_file, music_path, output_file)
    return output_file

# --- Streamlit App ---
st.set_page_config(page_title="Storytelling App", page_icon="📖", layout="centered")
st.title("📖 Bedtime Storytelling App")
st.markdown("Enjoy bedtime stories with voice narration and soft music.")

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

        # Generate and play TTS with music
        if st.button(f"▶ Play Scene {i+1}", key=f"btn{i}"):
            music_path = "audio/soft_music.mp3"
            audio_file = generate_tts_with_music(scene, music_path)
            audio_bytes = open(audio_file, "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
