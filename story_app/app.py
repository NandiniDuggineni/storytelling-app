import streamlit as st
from gtts import gTTS
import os
import tempfile
import re

st.set_page_config(page_title="Storytelling App with Two Voices", page_icon="📖")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_tts(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    temp_file.close()
    tts.save(temp_file.name)
    return temp_file.name

def parse_dialogue(story_text):
    """
    Parses lines starting with "Speaker: text" and returns list of (speaker, text)
    Lines without speaker prefix are treated as narrator with speaker 'Narrator'
    """
    dialogue = []
    lines = story_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r"^(.*?):\s*(.*)", line)
        if match:
            speaker, text = match.groups()
        else:
            speaker = "Narrator"
            text = line
        dialogue.append((speaker, text))
    return dialogue

st.title("📖 Storytelling App — Two Voices Simulation")

stories_dir = os.path.join(ROOT_DIR, "stories")

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
            with open(story_path, "r", encoding="utf-8") as f:
                story_text = f.read()

            dialogue = parse_dialogue(story_text)

            st.write("### Story Dialogue:")
            for speaker, line in dialogue:
                st.write(f"**{speaker}:** {line}")

            if st.button("▶ Play Story with Two Voices (same voice for demo)"):
                for speaker, line in dialogue:
                    audio_file = generate_tts(line)
                    with open(audio_file, "rb") as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format="audio/mp3")
