"""
app.py
Civic Sense AI — main entry point (Login / Registration page).

Run with:
    streamlit run app.py
"""

import streamlit as st
import database as db
import auth
import style

st.set_page_config(
    page_title="Civic Sense AI",
    page_icon="🏙️",
    layout="centered",
)

db.init_db()
auth.init_session()
style.inject_css()


def logged_in_view():
    user = st.session_state.user
    role_label = "Administrator" if user["role"] == "admin" else "Citizen"
    style.hero(
        "🏙️ Civic Sense AI",
        f"Welcome back, <b>{user['username']}</b> — signed in as {role_label}.",
        eyebrow="Community Reporting Platform",
    )

    st.markdown("#### What would you like to do?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<div class="cs-feature-card"><span class="cs-icon">📝</span>'
            '<h4>Report Incident</h4><p>File a new civic issue with AI-suggested category & priority.</p></div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/1_📝_Report_Incident.py", label="Open Report Incident", icon="📝")
        st.write("")
        st.markdown(
            '<div class="cs-feature-card"><span class="cs-icon">🗺️</span>'
            '<h4>Incident Map</h4><p>See every reported issue plotted live, color-coded by status.</p></div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/2_🗺️_Incident_Map.py", label="Open Incident Map", icon="🗺️")
    with col2:
        st.markdown(
            '<div class="cs-feature-card"><span class="cs-icon">🤖</span>'
            '<h4>AI Assistant</h4><p>Ask how to report, track, or resolve a civic concern.</p></div>',
            unsafe_allow_html=True,
        )
        st.page_link("pages/4_🤖_AI_Assistant.py", label="Open AI Assistant", icon="🤖")
        if user["role"] == "admin":
            st.write("")
            st.markdown(
                '<div class="cs-feature-card"><span class="cs-icon">📊</span>'
                '<h4>Admin Dashboard</h4><p>Review stats and manage every incident in the system.</p></div>',
                unsafe_allow_html=True,
            )
            st.page_link("pages/3_📊_Admin_Dashboard.py", label="Open Admin Dashboard", icon="📊")

    st.divider()
    if st.button("Log out"):
        auth.logout()
        st.rerun()


def login_register_view():
    style.hero(
        "🏙️ Civic Sense AI",
        "Report civic issues, track them on a live map, and get instant AI-powered guidance.",
        eyebrow="Community Reporting Platform",
    )

    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        st.markdown(
            '<div class="cs-feature-card"><span class="cs-icon">📝</span>'
            '<h4>Report</h4><p>Flag potholes, garbage, water logging & more in seconds.</p></div>',
            unsafe_allow_html=True,
        )
    with fcol2:
        st.markdown(
            '<div class="cs-feature-card"><span class="cs-icon">🗺️</span>'
            '<h4>Track</h4><p>Watch issues move from Pending to Resolved on the map.</p></div>',
            unsafe_allow_html=True,
        )
    with fcol3:
        st.markdown(
            '<div class="cs-feature-card"><span class="cs-icon">🤖</span>'
            '<h4>Get Help</h4><p>Ask the AI Assistant anything about civic reporting.</p></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    tab_login, tab_register = st.tabs(["🔑  Login", "🆕  Register"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in", use_container_width=True)
            if submitted:
                if auth.login(username, password):
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with st.expander("💡 Demo credentials"):
            st.code("Admin →   username: admin     password: admin123\n"
                    "Citizen → username: citizen   password: citizen123")

    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("Choose a username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Choose a password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account", use_container_width=True)
            if submitted:
                if not new_username or not new_password:
                    st.error("Username and password are required.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = db.create_user(new_username, new_password, new_email, role="citizen")
                    if ok:
                        st.success(msg + " You can now log in from the Login tab.")
                    else:
                        st.error(msg)


if auth.is_logged_in():
    logged_in_view()
else:
    login_register_view()
