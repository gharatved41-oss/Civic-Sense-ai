"""
pages/1_📝_Report_Incident.py
Lets a logged-in citizen submit a civic incident report.
AI assistant auto-suggests category & priority from the description.
An interactive map lets the citizen click to pin the exact incident location.
"""

import streamlit as st
import database as db
import auth
import style
from ai_assistant import classify_incident, CATEGORY_KEYWORDS

st.set_page_config(page_title="Report Incident", page_icon="📝", layout="centered")
auth.require_login()
db.init_db()
style.inject_css()

try:
    import folium
    from streamlit_folium import st_folium
    MAP_PICKER_AVAILABLE = True
except ImportError:
    MAP_PICKER_AVAILABLE = False

user = st.session_state.user

style.hero("📝 Report a Civic Incident",
           "Describe the issue — our AI will suggest a category and priority automatically.",
           eyebrow="New Report")

DEFAULT_LAT, DEFAULT_LON = 19.4559, 72.8117
if "report_lat" not in st.session_state:
    st.session_state.report_lat = DEFAULT_LAT
if "report_lon" not in st.session_state:
    st.session_state.report_lon = DEFAULT_LON

categories = list(CATEGORY_KEYWORDS.keys()) + ["Other"]

# Live AI suggestion as the user types (outside the form so it updates live)
description_preview = st.text_area(
    "Describe the issue",
    key="description_input",
    placeholder="e.g. Large pothole near the bus stop causing two-wheeler accidents...",
    height=120,
)

suggested_category, suggested_priority = ("Other", "Low")
if description_preview.strip():
    suggested_category, suggested_priority = classify_incident(description_preview)
    st.markdown(
        f'<div class="cs-card" style="border-left-color:{style.AMBER};">'
        f'🤖 <b>AI suggests:</b> {style.category_badge(suggested_category)}'
        f'{style.priority_badge(suggested_priority)}'
        f'<div class="cs-card-meta" style="margin-top:6px;">You can override this below.</div></div>',
        unsafe_allow_html=True,
    )

# ---------------- LOCATION PICKER MAP ----------------
st.markdown("#### 📍 Pinpoint the Location")

if MAP_PICKER_AVAILABLE:
    st.caption("Click anywhere on the map to mark exactly where the incident occurred, "
               "or search for a place below.")

    search_col, btn_col = st.columns([4, 1])
    with search_col:
        search_query = st.text_input(
            "Search for a place", placeholder="e.g. MG Road, Virar", label_visibility="collapsed"
        )
    with btn_col:
        search_clicked = st.button("🔍 Search", use_container_width=True)

    if search_clicked and search_query.strip():
        try:
            import requests
            resp = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": search_query, "format": "json", "limit": 1},
                headers={"User-Agent": "civic-sense-ai-app"},
                timeout=6,
            )
            results = resp.json()
            if results:
                st.session_state.report_lat = float(results[0]["lat"])
                st.session_state.report_lon = float(results[0]["lon"])
                st.success(f"📍 Found: {results[0].get('display_name', search_query)}")
            else:
                st.warning("No matching place found. Try a different search or click the map directly.")
        except Exception:
            st.warning("Couldn't reach the location search service. Please click the map directly instead.")

    m = folium.Map(
        location=[st.session_state.report_lat, st.session_state.report_lon],
        zoom_start=14,
    )
    folium.Marker(
        [st.session_state.report_lat, st.session_state.report_lon],
        tooltip="Incident location",
        icon=folium.Icon(color="red", icon="exclamation-triangle", prefix="fa"),
    ).add_to(m)

    map_state = st_folium(m, height=380, width=700, key="incident_location_picker")

    if map_state and map_state.get("last_clicked"):
        clicked_lat = map_state["last_clicked"]["lat"]
        clicked_lon = map_state["last_clicked"]["lng"]
        if (round(clicked_lat, 6), round(clicked_lon, 6)) != (
            round(st.session_state.report_lat, 6), round(st.session_state.report_lon, 6)
        ):
            st.session_state.report_lat = clicked_lat
            st.session_state.report_lon = clicked_lon
            st.rerun()

    st.markdown(
        f'<div class="cs-card" style="padding:10px 16px;">📌 <b>Selected coordinates:</b> '
        f'{st.session_state.report_lat:.6f}, {st.session_state.report_lon:.6f}</div>',
        unsafe_allow_html=True,
    )
else:
    st.info("Install `folium` and `streamlit-folium` (see requirements.txt) to enable the "
            "click-to-pin map. Using manual coordinate entry for now.")

# ---------------- REPORT FORM ----------------
with st.form("report_form", clear_on_submit=True):
    default_index = categories.index(suggested_category) if suggested_category in categories else len(categories) - 1
    category = st.selectbox("Category", categories, index=default_index)

    priority_options = ["Low", "Medium", "High"]
    priority = st.selectbox(
        "Priority",
        priority_options,
        index=priority_options.index(suggested_priority) if suggested_priority in priority_options else 0,
    )

    location_text = st.text_input("Location (landmark / street / area)")

    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input(
            "Latitude", value=float(st.session_state.report_lat), format="%.6f",
            help="Auto-filled from the map above — fine-tune here if needed.",
        )
    with col2:
        lon = st.number_input(
            "Longitude", value=float(st.session_state.report_lon), format="%.6f",
            help="Auto-filled from the map above — fine-tune here if needed.",
        )

    photo = st.file_uploader("Attach a photo (optional)", type=["png", "jpg", "jpeg"])

    submitted = st.form_submit_button("🚀 Submit Report", use_container_width=True)

    if submitted:
        if not description_preview.strip() or not location_text.strip():
            st.error("Please provide both a description and a location.")
        else:
            image_name = photo.name if photo else None
            incident_id = db.add_incident(
                user_id=user["id"],
                username=user["username"],
                category=category,
                description=description_preview.strip(),
                location_text=location_text.strip(),
                lat=lat,
                lon=lon,
                priority=priority,
                image_name=image_name,
            )
            st.success(f"✅ Incident #{incident_id} reported successfully! Thank you for helping your community.")
            st.balloons()
            st.session_state.report_lat = DEFAULT_LAT
            st.session_state.report_lon = DEFAULT_LON

st.divider()
st.markdown("#### 📋 Your Past Reports")
my_reports = db.get_incidents(username=user["username"])
if my_reports.empty:
    st.caption("You haven't reported any incidents yet.")
else:
    for _, row in my_reports.iterrows():
        st.markdown(style.render_incident_card(row), unsafe_allow_html=True)

