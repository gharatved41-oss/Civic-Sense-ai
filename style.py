"""
style.py
Shared design system for Civic Sense AI.

Theme: "Civic Blueprint" — an ink-navy + teal + amber palette that reads as
municipal/civic-tech rather than a generic AI-app template, with Space
Grotesk for display type and Inter for body/UI text.

Import and call inject_css() once near the top of every page (after
st.set_page_config). Use badge_html() / render_incident_card() to keep
incident displays visually consistent everywhere.
"""

import streamlit as st

# ---- Design tokens ----
INK = "#0E2438"        # near-black navy — headers, sidebar
NAVY = "#123A5C"       # primary surfaces
TEAL = "#128C87"       # primary action / brand accent
TEAL_DARK = "#0D6B67"
AMBER = "#F2A93B"      # pending / in-progress accent
CORAL = "#E4572E"      # high priority / danger
GREEN = "#2E9E64"      # resolved / success
PAPER = "#F4F7FA"      # app background
CARD = "#FFFFFF"
INK_SOFT = "#5B7185"   # secondary text

STATUS_STYLE = {
    "Pending":     {"bg": "#FDEDEA", "fg": "#C1401D", "dot": CORAL},
    "In Progress": {"bg": "#FEF3E1", "fg": "#A6690C", "dot": AMBER},
    "Resolved":    {"bg": "#E7F6EC", "fg": "#1C7A45", "dot": GREEN},
}

PRIORITY_STYLE = {
    "High":   {"bg": "#FDEDEA", "fg": "#C1401D"},
    "Medium": {"bg": "#FEF3E1", "fg": "#A6690C"},
    "Low":    {"bg": "#EAF3FB", "fg": "#1A5C8C"},
}


def inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        h1, h2, h3, h4, .cs-display {{
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.01em;
        }}

        .stApp {{
            background: {PAPER};
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {INK} 0%, {NAVY} 100%);
        }}
        section[data-testid="stSidebar"] * {{
            color: #E7EEF3 !important;
        }}
        section[data-testid="stSidebar"] .stButton button {{
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.18);
        }}
        section[data-testid="stSidebar"] a {{
            border-radius: 8px !important;
        }}
        section[data-testid="stSidebarNav"] li div a {{
            border-radius: 8px;
        }}
        section[data-testid="stSidebarNav"] li div a:hover {{
            background: rgba(18,140,135,0.35) !important;
        }}

        /* ---- Buttons ---- */
        .stButton > button, .stFormSubmitButton > button {{
            background: linear-gradient(135deg, {TEAL} 0%, {TEAL_DARK} 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.55em 1.2em;
            transition: transform 0.08s ease, box-shadow 0.15s ease;
            box-shadow: 0 2px 6px rgba(18,140,135,0.25);
        }}
        .stButton > button:hover, .stFormSubmitButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(18,140,135,0.35);
            color: white;
        }}

        /* ---- Metrics as cards ---- */
        div[data-testid="stMetric"] {{
            background: {CARD};
            border: 1px solid #E4EAEF;
            border-left: 5px solid {TEAL};
            border-radius: 12px;
            padding: 14px 18px 10px 18px;
            box-shadow: 0 2px 10px rgba(14,36,56,0.05);
        }}
        div[data-testid="stMetricLabel"] {{
            color: {INK_SOFT};
        }}

        /* ---- Tabs ---- */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 6px;
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px 10px 0 0;
            padding: 8px 18px;
            font-weight: 600;
            color: {INK_SOFT};
        }}
        .stTabs [aria-selected="true"] {{
            background: {CARD};
            color: {TEAL_DARK} !important;
            border-bottom: 3px solid {TEAL};
        }}

        /* ---- Inputs ---- */
        .stTextInput input, .stTextArea textarea, .stNumberInput input,
        div[data-baseweb="select"] > div {{
            border-radius: 8px !important;
            border: 1px solid #D6DEE5 !important;
        }}

        /* ---- Expander (used for admin incident cards) ---- */
        details {{
            background: {CARD};
            border: 1px solid #E4EAEF !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(14,36,56,0.04);
            margin-bottom: 10px;
        }}

        /* ---- Custom classes ---- */
        .cs-hero {{
            background: linear-gradient(135deg, {INK} 0%, {NAVY} 55%, {TEAL_DARK} 100%);
            border-radius: 20px;
            padding: 40px 36px;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 10px 30px rgba(14,36,56,0.25);
        }}
        .cs-hero h1 {{
            color: white !important;
            font-size: 2.4rem;
            margin-bottom: 6px;
        }}
        .cs-hero p {{
            color: #C9DCE4;
            font-size: 1.05rem;
            margin: 0;
        }}
        .cs-eyebrow {{
            display: inline-block;
            background: rgba(242,169,59,0.18);
            color: {AMBER};
            font-weight: 600;
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 14px;
        }}

        .cs-feature-card {{
            background: {CARD};
            border: 1px solid #E4EAEF;
            border-radius: 14px;
            padding: 18px 16px;
            height: 100%;
            box-shadow: 0 2px 10px rgba(14,36,56,0.05);
        }}
        .cs-feature-card .cs-icon {{
            font-size: 1.6rem;
        }}
        .cs-feature-card h4 {{
            margin: 8px 0 4px 0;
            color: {INK};
        }}
        .cs-feature-card p {{
            color: {INK_SOFT};
            font-size: 0.88rem;
            margin: 0;
        }}

        .cs-card {{
            background: {CARD};
            border: 1px solid #E4EAEF;
            border-left: 5px solid {TEAL};
            border-radius: 12px;
            padding: 14px 18px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(14,36,56,0.05);
        }}
        .cs-card-title {{
            font-weight: 700;
            color: {INK};
            font-size: 1.02rem;
            margin-bottom: 4px;
        }}
        .cs-card-meta {{
            color: {INK_SOFT};
            font-size: 0.82rem;
            margin-bottom: 8px;
        }}
        .cs-card-desc {{
            color: #2C3E4A;
            font-size: 0.92rem;
        }}

        .cs-badge {{
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 999px;
            margin-right: 6px;
            letter-spacing: 0.02em;
        }}
        .cs-dot {{
            display: inline-block;
            width: 7px; height: 7px;
            border-radius: 50%;
            margin-right: 5px;
        }}

        .cs-legend-item {{
            display: inline-flex;
            align-items: center;
            margin-right: 18px;
            font-size: 0.85rem;
            color: {INK_SOFT};
        }}

        /* ---- Force dark, readable text on every light/white surface,      ---- */
        /* ---- regardless of the visitor's OS/browser dark-mode preference ---- */
        .stApp, .stApp p, .stApp span, .stApp li, .stApp label,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5,
        .stMarkdown, .stMarkdown p {{
            color: {INK};
        }}
        details, details *,
        div[data-testid="stMetricValue"], div[data-testid="stMetricDelta"],
        div[data-testid="stMetricLabel"],
        .stDataFrame, .stDataFrame * ,
        .stChatMessage, .stChatMessage p,
        .stTextInput label, .stTextArea label, .stSelectbox label,
        .stNumberInput label, .stFileUploader label,
        div[data-baseweb="select"] * ,
        .cs-card, .cs-card *:not(.cs-badge):not(.cs-dot),
        .cs-feature-card, .cs-feature-card p, .cs-feature-card h4 {{
            color: {INK} !important;
        }}
        /* Sidebar keeps light text on its dark background — re-override after the block above */
        section[data-testid="stSidebar"], section[data-testid="stSidebar"] * {{
            color: #E7EEF3 !important;
        }}
        /* Hero banner keeps light text on its dark gradient background */
        .cs-hero, .cs-hero h1, .cs-hero p {{
            color: white !important;
        }}
        .cs-hero p {{
            color: #C9DCE4 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def status_badge(status: str) -> str:
    s = STATUS_STYLE.get(status, {"bg": "#EEE", "fg": "#555", "dot": "#999"})
    return (f'<span class="cs-badge" style="background:{s["bg"]};color:{s["fg"]};">'
            f'<span class="cs-dot" style="background:{s["dot"]};"></span>{status}</span>')


def priority_badge(priority: str) -> str:
    p = PRIORITY_STYLE.get(priority, {"bg": "#EEE", "fg": "#555"})
    return f'<span class="cs-badge" style="background:{p["bg"]};color:{p["fg"]};">{priority} priority</span>'


def category_badge(category: str) -> str:
    return f'<span class="cs-badge" style="background:#EAF3FB;color:{NAVY};">{category}</span>'


def render_incident_card(row) -> str:
    """Build an HTML card for a single incident row (dict-like with the usual fields)."""
    return f"""
    <div class="cs-card">
        <div class="cs-card-title">#{row['id']} — {row['category']}</div>
        <div class="cs-card-meta">📍 {row.get('location_text', '—')} &nbsp;•&nbsp; 🕒 {str(row.get('created_at',''))[:16]}
        &nbsp;•&nbsp; 👤 {row.get('username','—')}</div>
        {status_badge(row['status'])}{priority_badge(row['priority'])}
        <div class="cs-card-desc" style="margin-top:8px;">{row.get('description','')}</div>
    </div>
    """


def hero(title: str, subtitle: str, eyebrow: str = None):
    eyebrow_html = f'<span class="cs-eyebrow">{eyebrow}</span><br/>' if eyebrow else ""
    st.markdown(
        f"""
        <div class="cs-hero">
            {eyebrow_html}
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
