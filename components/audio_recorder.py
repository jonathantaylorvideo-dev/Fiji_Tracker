import streamlit as st
from typing import Optional
from core.logger import get_logger

logger = get_logger()

def render_audio_recorder() -> Optional[bytes]:
    """Renders a hybrid audio ingestion component supporting both live microphone capture 
    and pre-recorded file uploads, returning raw audio bytes with defensive error handling 
    and built-in audio playback previews.
    """
    st.subheader("🎙️ Hybrid Audio Ingestion Portal")
    
    audio_bytes = None
    
    # Use Streamlit tabs to offer dual-mode ingestion cleanly and intuitively
    tab_live, tab_upload = st.tabs(["🎙️ Live Microphone Recording", "📁 Pre-recorded File Upload"])
    
    with tab_live:
        st.markdown("Record live field inspection telemetry directly from your hardware microphone.")
        try:
            live_audio_file = st.audio_input("Record Infrastructure Report")
            if live_audio_file is not None:
                audio_bytes = live_audio_file.read()
                st.audio(audio_bytes, format="audio/wav")
                logger.info("Successfully captured live audio stream from native audio recorder.")
        except Exception as e:
            logger.error(f"Error during live microphone audio capture: {e}")
            st.error("⚠️ Failed to capture live audio from recording device. Please verify microphone permissions and browser access.")
            
    with tab_upload:
        st.markdown("Upload pre-recorded audio inspection files (supported formats: `.wav`, `.mp3`, `.m4a`).")
        try:
            uploaded_file = st.file_uploader(
                "Select pre-recorded audio file",
                type=["wav", "mp3", "m4a"],
                help="Upload an existing audio file of the infrastructure field report."
            )
            if uploaded_file is not None:
                audio_bytes = uploaded_file.read()
                file_extension = uploaded_file.name.split('.')[-1].lower()
                mime_type = f"audio/{'mpeg' if file_extension == 'mp3' else file_extension}"
                st.audio(audio_bytes, format=mime_type)
                logger.info("Successfully ingested pre-recorded audio file payload.")
        except Exception as e:
            logger.error(f"Error reading uploaded audio file payload: {e}")
            st.error("⚠️ Failed to read the uploaded audio file. Please verify file integrity and encoding.")
            
    return audio_bytes