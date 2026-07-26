import streamlit as st

def render_metrics_card(label: str, value: str, delta: str = None, help_text: str = None) -> None:
    """Renders a modular KPI card helper function with optional delta metrics and contextual help."""
    st.metric(label=label, value=value, delta=delta, help=help_text)