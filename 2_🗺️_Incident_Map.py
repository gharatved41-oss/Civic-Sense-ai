"""
pages/2_🗺️_Incident_Map.py
Displays all reported incidents on an interactive map, color-coded by status.
"""

import streamlit as st
import pandas as pd
import database as db
import auth
import style

st.set_page_config(page_title="Incident Map", page_icon="🗺️", layout="wide")
auth.require_login()
db.init_db()
style.inject_css()

style.hero("🗺️ Incident Map",
           "All civic issues reported by citizens, plotted by location.",
           eyebrow="Live Overview")

col1, col2 = st.columns(2)
with col1:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "In Progress", "Resolved"])
with col2:
    all_incidents_df = db.get_incidents()
    categories = ["All"] + sorted(all_incidents_df["category"].unique().tolist()) if not all_incidents_df.empty else ["All"]
    category_filter = st.selectbox("Filter by category", categories)

df = db.get_incidents(status=status_filter, category=category_filter)
df = df.dropna(subset=["lat", "lon"])

if df.empty:
    st.info("No incidents match the selected filters.")
else:
    STATUS_COLORS = {
        "Pending": [228, 87, 46],       # coral
        "In Progress": [242, 169, 59],  # amber
        "Resolved": [46, 158, 100],     # green
    }
    map_df = df.copy()
    map_df["color"] = map_df["status"].map(STATUS_COLORS)

    try:
        import pydeck as pdk

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[lon, lat]",
            get_fill_color="color",
            get_radius=120,
            get_line_color=[255, 255, 255],
            line_width_min_pixels=2,
            stroked=True,
            pickable=True,
        )
        view_state = pdk.ViewState(
            latitude=map_df["lat"].mean(),
            longitude=map_df["lon"].mean(),
            zoom=11,
        )
        tooltip = {
            "html": "<b>{category}</b> ({priority})<br/>{location_text}<br/>Status: {status}",
            "style": {"backgroundColor": style.INK, "color": "white", "borderRadius": "8px"},
        }
        st.pydeck_chart(pdk.Deck(
            layers=[layer], initial_view_state=view_state, tooltip=tooltip,
        ))
    except Exception:
        st.map(map_df.rename(columns={"lat": "latitude", "lon": "longitude"}))

    st.markdown(
        f"""
        <div style="margin: 4px 0 18px 0;">
            <span class="cs-legend-item"><span class="cs-dot" style="background:{style.CORAL};"></span>Pending</span>
            <span class="cs-legend-item"><span class="cs-dot" style="background:{style.AMBER};"></span>In Progress</span>
            <span class="cs-legend-item"><span class="cs-dot" style="background:{style.GREEN};"></span>Resolved</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("#### 📋 Incident List")
    for _, row in df.iterrows():
        st.markdown(style.render_incident_card(row), unsafe_allow_html=True)
