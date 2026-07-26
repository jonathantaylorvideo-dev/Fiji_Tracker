import streamlit as st
from services.supabase_client import SupabaseService
from components.gis_renderer import render_gis_map
from components.metrics_card import render_metrics_card
from core.logger import get_logger

logger = get_logger()

def render_dashboard_view() -> None:
    """Renders the primary operations monitor combining KPI metrics cards and GIS mapping."""
    st.title("📊 Fiji Infrastructure Operations Dashboard")
    st.markdown("Real-time telemetry and spatial status across regional infrastructure networks.")

    supabase_service = SupabaseService()
    
    with st.spinner("Fetching active infrastructure assets..."):
        response = supabase_service.fetch_all_assets()

    assets = response.data if response.success and response.data else []

    # Calculate summary metrics
    total_assets = len(assets)
    critical_count = sum(1 for a in assets if int(a.get("severity", 1)) >= 4)
    operational_count = sum(1 for a in assets if a.get("status") == "Operational")
    operational_pct = f"{(operational_count / total_assets * 100):.1f}%" if total_assets > 0 else "N/A"

    # Display KPI summary cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metrics_card("Total Tracked Assets", str(total_assets), delta="+2 this week")
    with col2:
        render_metrics_card("Operational Rate", operational_pct, delta="+0.5%")
    with col3:
        render_metrics_card("Critical Incidents", str(critical_count), delta="-1 resolved", help_text="Assets with severity rating >= 4")
    with col4:
        render_metrics_card("Active Regions", "4", help_text="Central, Western, Northern, Eastern")

    st.markdown("---")
    
    # Render interactive GIS map
    st.subheader("🗺️ Spatial Asset Telemetry Map")
    render_gis_map(assets)

    # Render summary table of recent assets
    if assets:
        st.markdown("---")
        st.subheader("📋 Recent Asset Log")
        st.dataframe(assets, use_container_width=True)