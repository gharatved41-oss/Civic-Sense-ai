# 🏙️ Civic Sense AI

A Streamlit application for citizens to report civic issues (potholes, garbage,
water logging, streetlights, etc.), view them on a live map, and get help from
an AI assistant. Admins get a dashboard to manage and resolve reports.

## Features

- **Login / Registration** — session-based auth backed by SQLite, with a
  pre-seeded admin and citizen demo account.
- **Report Incident** — citizens submit issues; an AI layer auto-suggests the
  category and priority from the free-text description. An interactive map
  lets them click to pin the exact incident location (or search a place
  name), with manual latitude/longitude fields as a fallback.
- **Incident Map** — all reports plotted on an interactive map, color-coded
  by status (Pending / In Progress / Resolved), with filters.
- **Admin Dashboard** — KPI overview, category/priority charts, and controls
  to update status or delete reports (admin-only).
- **AI Assistant** — a chat interface that answers civic questions and
  guides users through the app. Works fully offline out of the box; if you
  set an `ANTHROPIC_API_KEY`, it automatically upgrades to a Claude-powered
  assistant.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app will create a local `civic_sense.db` SQLite file on first run.

### Demo credentials

| Role    | Username | Password    |
|---------|----------|-------------|
| Admin   | admin    | admin123    |
| Citizen | citizen  | citizen123  |

### (Optional) Enable the Claude-powered AI Assistant

Set your Anthropic API key as an environment variable before launching:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
streamlit run app.py
```

Or add it to `.streamlit/secrets.toml`:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Without a key, the assistant automatically falls back to a built-in
rule-based responder — no functionality is lost, responses are just simpler.

## Project structure

```
civic_sense_ai/
├── app.py                            # Login / registration entry point
├── database.py                       # SQLite persistence layer
├── auth.py                           # Session-based auth helpers
├── ai_assistant.py                   # Classification + chatbot logic
├── style.py                          # Shared design system (CSS + badges/cards)
├── requirements.txt
├── .streamlit/config.toml            # Forces a consistent light theme
└── pages/
    ├── 1_📝_Report_Incident.py       # includes the click-to-pin location map
    ├── 2_🗺️_Incident_Map.py
    ├── 3_📊_Admin_Dashboard.py
    └── 4_🤖_AI_Assistant.py
```

### Note on the location picker map

The Report Incident page's click-to-pin map uses `folium` +
`streamlit-folium` (already in `requirements.txt`). If those packages
aren't installed, the page automatically falls back to manual
latitude/longitude number inputs — nothing breaks, you just lose the
visual picker. The "Search for a place" box uses the free OpenStreetMap
Nominatim API and requires the app server to have internet access.
