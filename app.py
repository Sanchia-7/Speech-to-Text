import os
from pydub import AudioSegment
import tempfile
import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================
load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
speech_region = os.getenv("AZURE_SPEECH_REGION")

# =========================
# STREAMLIT CONFIG
# =========================
st.set_page_config(
    page_title="Azure Speech to Text",
    page_icon="🎙️",
    layout="centered"
)

st.title("🎙️ Azure Speech to Text")
st.write("Convert speech or uploaded audio into **grammatically correct text** using Azure AI.")

# =========================
# SPEECH CONFIG
# =========================
def create_speech_config():
    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region
    )
    speech_config.speech_recognition_language = "en-US"

    # Enable punctuation & grammar
    speech_config.set_property(
        speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
        "TrueText"
    )
    return speech_config

# =========================
# 🎤 MICROPHONE INPUT
# =========================
st.subheader("🎤 Speak using Microphone")

if st.button("🎤 Start Speaking"):
    if not speech_key or not speech_region:
        st.error("Azure Speech Key or Region is missing.")
    else:
        with st.spinner("Listening... Please speak clearly"):
            audio_config = speechsdk.audio.AudioConfig(
                use_default_microphone=True
            )

            recognizer = speechsdk.SpeechRecognizer(
                speech_config=create_speech_config(),
                audio_config=audio_config
            )

            result = recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                st.success("Speech Recognized Successfully!")
                st.text_area(
                    "📝 Transcribed Text:",
                    value=result.text,
                    height=150
                )

            elif result.reason == speechsdk.ResultReason.NoMatch:
                st.warning("No speech could be recognized.")

            elif result.reason == speechsdk.ResultReason.Canceled:
                st.error("Speech recognition was canceled.")

# =========================
# 📂 AUDIO FILE UPLOAD
# =========================
st.divider()
st.subheader("📂 Upload Audio File (Any File Type)")

uploaded_file = st.file_uploader(
    "Upload an audio file (MP3, WAV, M4A, etc.)",
    type=None
)

if uploaded_file:
    if not speech_key or not speech_region:
        st.error("Azure Speech Key or Region is missing.")
    else:
        try:
            # -------------------------
            # Save uploaded file
            # -------------------------
            with tempfile.NamedTemporaryFile(delete=False) as input_tmp:
                input_tmp.write(uploaded_file.read())
                input_path = input_tmp.name

            # -------------------------
            # Convert ANY audio → WAV (PCM 16kHz, mono)
            # -------------------------
            audio = AudioSegment.from_file(input_path)
            audio = audio.set_channels(1).set_frame_rate(16000)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as wav_tmp:
                audio.export(wav_tmp.name, format="wav")
                wav_path = wav_tmp.name

            # -------------------------
            # Azure Continuous Recognition
            # -------------------------
            audio_config = speechsdk.audio.AudioConfig(filename=wav_path)

            recognizer = speechsdk.SpeechRecognizer(
                speech_config=create_speech_config(),
                audio_config=audio_config
            )

            full_transcript = []

            def on_recognized(evt):
                if evt.result.text:
                    full_transcript.append(evt.result.text)

            recognizer.recognized.connect(on_recognized)

            with st.spinner("Transcribing uploaded audio..."):
                recognizer.start_continuous_recognition()

                # Wait until audio finishes
                import time
                time.sleep(audio.duration_seconds + 0.5)

                recognizer.stop_continuous_recognition()

            # -------------------------
            # Display Result
            # -------------------------
            final_text = " ".join(full_transcript)

            if final_text.strip():
                st.success("Audio Transcribed Successfully!")
                st.text_area(
                    "📝 Transcribed Text:",
                    value=final_text,
                    height=220
                )
            else:
                st.warning("No speech could be recognized from this audio.")

        except Exception as e:
            st.error(
                "This file could not be processed. "
                "Please upload a valid audio file containing speech."
            )
