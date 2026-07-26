import streamlit as st
from core.config import settings
from core.logger import get_logger
from views.dashboard_view import render_dashboard_view
from views.ingestion_view import render_ingestion_view
from views.analytics_view import render_analytics_view

logger = get_logger()

# Initialize Streamlit page configuration
st.set_page_config(
    page_title="Fiji Infrastructure Tracker",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def validate_environment() -> None:
    """Validates required environment configurations and secrets on startup."""
    try:
        missing_keys = []
        if not settings.GEMINI_API_KEY and not st.secrets.get("GEMINI_API_KEY"):
            missing_keys.append("GEMINI_API_KEY")
        if not settings.SUPABASE_URL and not st.secrets.get("SUPABASE_URL"):
            missing_keys.append("SUPABASE_URL")
        
        if missing_keys:
            logger.warning(f"Missing recommended configuration keys: {', '.join(missing_keys)}")
    except Exception as e:
        logger.error(f"Error validating environment config: {e}")

def main() -> None:
    """Main application entry point managing global session state, configuration validation, and sidebar routing."""
    try:
        validate_environment()
        logger.info("Starting Fiji Infrastructure Tracker application session.")

        # Global session state initialization
        if "initialized" not in st.session_state:
            st.session_state.initialized = True
            st.session_state.current_user_role = "Field Operator"

        # Sidebar Navigation Routing
        st.sidebar.title("🏝️ Fiji Tracker Nav")
        st.sidebar.markdown(f"**Role:** {st.session_state.current_user_role}")
        st.sidebar.markdown("---")

        navigation_choice = st.sidebar.radio(
            "Select View",
            options=["Operations Dashboard", "Voice Ingestion Portal", "Analytics & Reporting"],
            index=0
        )

        st.sidebar.markdown("---")
        st.sidebar.info("System Status: 🟢 Online\nRegion: Fiji Central / Regional Hub")

        # View dispatcher with graceful error boundary trapping
        if navigation_choice == "Operations Dashboard":
            render_dashboard_view()
        elif navigation_choice == "Voice Ingestion Portal":
            render_ingestion_view()
        elif navigation_choice == "Analytics & Reporting":
            render_analytics_view()

    except Exception as e:
        logger.error(f"Critical application error trapped in main entry point: {e}")
        st.error("A critical application error occurred. Please consult the system logs.")

if __name__ == "__main__":
    main()