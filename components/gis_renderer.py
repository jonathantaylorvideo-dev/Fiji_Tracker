import streamlit as st
import pydeck as pdk
import pandas as pd
from typing import List, Dict, Any
from core.logger import get_logger

logger = get_logger()

def render_gis_map(assets: List[Dict[str, Any]]) -> None:
    """Renders an interactive PyDeck scatterplot layer over a token-free basemap centered on Fiji, 
    incorporating defensive error boundaries and explicit container sizing.
    """
    try:
        # Standardized Fiji central coordinates for default viewport centering
        default_lat = -17.7134
        default_lon = 178.0650
        
        processed_rows = []
        if assets:
            for asset in assets:
                geom = asset.get("geom")
                lat, lon = None, None
                
                # Parse GeoJSON or direct coordinate pairs safely
                if isinstance(geom, dict) and "coordinates" in geom:
                    coords = geom.get("coordinates")
                    if len(coords) >= 2:
                        lon, lat = coords[0], coords[1]
                elif "latitude" in asset and "longitude" in asset:
                    lat, lon = asset.get("latitude"), asset.get("longitude")
                
                if lat is not None and lon is not None:
                    processed_rows.append({
                        "id": asset.get("id", "unknown"),
                        "asset_type": asset.get("asset_type", "Unknown"),
                        "latitude": float(lat),
                        "longitude": float(lon),
                        "severity": int(asset.get("severity", 1)),
                        "status": asset.get("status", "Operational"),
                        "description": asset.get("description", "No description provided.")
                    })
        
        # Fallback default reference point if dataset is empty or unparseable
        if not processed_rows:
            processed_rows.append({
                "id": "fiji-default-hub",
                "asset_type": "Fiji Central Reference",
                "latitude": default_lat,
                "longitude": default_lon,
                "severity": 1,
                "status": "Operational",
                "description": "Default reference coordinate for Fiji infrastructure network."
            })

        df = pd.DataFrame(processed_rows)

        # Define PyDeck scatterplot layer with severity-scaled coloring
        scatterplot_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=["longitude", "latitude"],
            get_color="[255, 255 - (severity * 35), 50, 200]",
            get_radius=25000,
            pickable=True,
            auto_highlight=True,
        )

        # Explicit initial viewport centered on Fiji
        view_state = pdk.ViewState(
            latitude=default_lat,
            longitude=default_lon,
            zoom=7,
            pitch=30,
            bearing=0
        )

        # Construct Deck object with map_style=None to eliminate Mapbox token dependency / blank black screen failure
        r = pdk.Deck(
            layers=[scatterplot_layer],
            initial_view_state=view_state,
            map_style=None,
            tooltip={
                "html": "<b>Asset:</b> {asset_type}<br/><b>Status:</b> {status}<br/><b>Severity:</b> {severity}<br/><b>Notes:</b> {description}",
                "style": {"backgroundColor": "steelblue", "color": "white", "borderRadius": "4px"}
            }
        )

        # Render with explicit container dimensions and full width matching requirements
        st.pydeck_chart(r, use_container_width=True, height=600)
        logger.info("Successfully rendered GIS map component with token-free basemap.")

    except Exception as e:
        logger.error(f"GIS rendering exception caught: {e}")
        st.warning("⚠️ GIS map rendering encountered an error loading spatial layers. Please check system logs.")