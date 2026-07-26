import streamlit as st
from datetime import datetime
from services.gemini_client import GeminiVoiceParser
from services.supabase_client import SupabaseService
from components.audio_recorder import render_audio_recorder
from core.logger import get_logger

logger = get_logger()

def render_ingestion_view() -> None:
    """Renders the voice-to-GIS capture workflow including audio input, Gemini parsing, human-in-the-loop review, and Supabase persistence."""
    st.title("📥 Voice-to-GIS Ingestion Pipeline")
    st.markdown("Record or upload field audio notes to automatically parse structural infrastructure incidents.")

    gemini_parser = GeminiVoiceParser()
    supabase_service = SupabaseService()

    audio_bytes = render_audio_recorder()

    st.markdown("---")
    st.subheader("📝 Manual Transcript Input / Fallback")
    manual_transcript = st.text_area(
        "Or enter field transcript notes directly:",
        placeholder="e.g., Bridge structural crack observed near Wainadoi. Severity level 4. Coordinates 18.15 South, 178.42 East."
    )

    transcript_to_process = None
    if audio_bytes:
        # Simulate transcription extraction if audio bytes are present (or hook into speech-to-text service)
        transcript_to_process = st.text_input("Simulated Transcript extracted from Audio Bytes:", value="Bridge structural failure near Nausori bridge, severity 4, lat -18.03, lon 178.53")
    elif manual_transcript.strip():
        transcript_to_process = manual_transcript.strip()

    if st.button("🚀 Process Payload with Gemini", type="primary"):
        if not transcript_to_process:
            st.warning("Please provide either audio input or a text transcript before processing.")
            return

        with st.spinner("Analyzing transcript with Gemini Voice Parser..."):
            parsed_payload = gemini_parser.parse_transcript(transcript_to_process)

        if not parsed_payload:
            st.error("Failed to extract structured payload from Gemini. Please check logs or refine input.")
            return

        st.success("Successfully parsed payload! Review and confirm details below:")

        # Human-in-the-loop review form
        with st.form("review_payload_form"):
            st.subheader("🔍 Human-in-the-Loop Review")
            edited_asset_type = st.text_input("Asset Type", value=parsed_payload.asset_type)
            col1, col2 = st.columns(2)
            with col1:
                edited_lat = st.number_input("Latitude", value=parsed_payload.latitude, format="%.6f")
            with col2:
                edited_lon = st.number_input("Longitude", value=parsed_payload.longitude, format="%.6f")
            
            edited_severity = st.slider("Severity Level (1-5)", min_value=1, max_value=5, value=parsed_payload.severity)
            edited_description = st.text_area("Description", value=parsed_payload.description)
            edited_status = st.selectbox("Initial Status", ["Operational", "Degraded", "Critical Failure", "Under Maintenance"], index=0)

            submitted = st.form_submit_button("💾 Confirm & Save to Supabase")
            
            if submitted:
                geom_payload = {
                    "type": "Point",
                    "coordinates": [edited_lon, edited_lat]
                }
                record_data = {
                    "asset_type": edited_asset_type,
                    "geom": geom_payload,
                    "status": edited_status,
                    "severity": edited_severity,
                    "description": edited_description,
                    "created_at": datetime.utcnow().isoformat()
                }

                with st.spinner("Saving asset record to Supabase..."):
                    db_response = supabase_service.insert_asset(record_data)

                if db_response.success:
                    st.success("Infrastructure asset successfully committed to Supabase database!")
                    logger.info("Asset record successfully persisted via ingestion view workflow.")
                else:
                    st.error(f"Failed to save record to database: {db_response.error}")