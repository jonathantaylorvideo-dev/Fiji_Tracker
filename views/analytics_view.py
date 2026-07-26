import streamlit as st
import pandas as pd
import plotly.express as px
from services.supabase_client import SupabaseService
from core.logger import get_logger

logger = get_logger()

def render_analytics_view() -> None:
    """Implements reporting interfaces, filtering tools by asset type/severity, and CSV export utilities."""
    st.title("📈 Infrastructure Analytics & Reporting")
    st.markdown("Analyze asset distributions, severity breakdowns, and export operational datasets.")

    supabase_service = SupabaseService()
    response = supabase_service.fetch_all_assets()
    assets = response.data if response.success and response.data else []

    if not assets:
        st.info("No infrastructure asset data available for analytics generation.")
        return

    df = pd.DataFrame(assets)

    # Ensure required columns exist for filtering and visualization
    if "asset_type" not in df.columns:
        df["asset_type"] = "Unknown"
    if "severity" not in df.columns:
        df["severity"] = 1
    if "status" not in df.columns:
        df["status"] = "Operational"

    # Sidebar / Top Filter Controls
    st.subheader("🔎 Filter Parameters")
    col1, col2 = st.columns(2)
    
    selected_types = col1.multiselect(
        "Filter by Asset Type",
        options=df["asset_type"].unique().tolist(),
        default=df["asset_type"].unique().tolist()
    )
    
    selected_severities = col2.slider(
        "Filter by Severity Range",
        min_value=1,
        max_value=5,
        value=(1, 5)
    )

    filtered_df = df[
        (df["asset_type"].isin(selected_types)) &
        (df["severity"] >= selected_severities[0]) &
        (df["severity"] <= selected_severities[1])
    ]

    st.markdown("---")

    # Visualizations using Plotly
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("📊 Assets by Type")
        if not filtered_df.empty:
            fig_type = px.bar(
                filtered_df["asset_type"].value_counts().reset_index(),
                x="index",
                y="asset_type",
                labels={"index": "Asset Type", "asset_type": "Count"},
                color="asset_type"
            )
            st.plotly_chart(fig_type, use_container_width=True)
        else:
            st.warning("No data matches the selected filter criteria.")

    with col_chart2:
        st.subheader("⚠️ Severity Distribution")
        if not filtered_df.empty:
            fig_sev = px.pie(
                filtered_df,
                names="severity",
                title="Proportion of Asset Severity Ratings",
                hole=0.4
            )
            st.plotly_chart(fig_sev, use_container_width=True)
        else:
            st.warning("No data matches the selected filter criteria.")

    st.markdown("---")

    # CSV Export Utility
    st.subheader("📥 Export Filtered Dataset")
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Assets as CSV",
        data=csv_data,
        file_name="fiji_infrastructure_filtered_report.csv",
        mime="text/csv",
    )