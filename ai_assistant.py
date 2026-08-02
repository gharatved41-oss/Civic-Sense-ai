"""
ai_assistant.py
A lightweight "civic sense" AI layer.

- classify_incident(): keyword-based auto-categorization + priority suggestion
  for incident reports (works fully offline, no API key required).
- get_ai_response(): a rule-based civic assistant chatbot. If an
  ANTHROPIC_API_KEY is available (env var or st.secrets), it will
  automatically upgrade to a real Claude-powered assistant; otherwise it
  falls back to the built-in rule-based responder so the app always works
  out of the box.
"""

import os
import re

CATEGORY_KEYWORDS = {
    "Pothole": ["pothole", "road damage", "broken road", "crater", "road crack"],
    "Garbage": ["garbage", "trash", "waste", "litter", "dump", "rubbish"],
    "Streetlight": ["streetlight", "street light", "lamp post", "no light", "dark street"],
    "Water Logging": ["water logging", "flooding", "flood", "drain overflow", "stagnant water"],
    "Sewage": ["sewage", "drainage", "manhole", "gutter", "sewer"],
    "Electricity": ["power cut", "electricity", "wire", "transformer", "short circuit"],
    "Stray Animals": ["stray dog", "stray cattle", "stray animal", "animal menace"],
    "Illegal Construction": ["illegal construction", "encroachment", "unauthorized building"],
    "Tree/Vegetation": ["fallen tree", "tree branch", "overgrown", "tree fall"],
    "Traffic": ["traffic signal", "traffic jam", "signal not working", "encroached footpath"],
}

HIGH_PRIORITY_WORDS = ["accident", "injury", "fire", "collapse", "danger", "electrocution",
                        "child", "hospital", "emergency", "death", "flood"]
MEDIUM_PRIORITY_WORDS = ["overflow", "broken", "leak", "blocked", "damaged"]


def classify_incident(description: str):
    """Return (category, priority) suggested from free-text description."""
    text = description.lower()

    category = "Other"
    best_hits = 0
    for cat, keywords in CATEGORY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text)
        if hits > best_hits:
            best_hits = hits
            category = cat

    if any(word in text for word in HIGH_PRIORITY_WORDS):
        priority = "High"
    elif any(word in text for word in MEDIUM_PRIORITY_WORDS):
        priority = "Medium"
    else:
        priority = "Low"

    return category, priority


# ---------------- CHATBOT ----------------

FAQ_RESPONSES = {
    r"\b(hi|hello|hey)\b": "Hello! I'm your Civic Sense AI Assistant. Ask me how to report an issue, "
                            "check incident status, or learn about civic responsibilities.",
    r"report.*(pothole|road)": "To report a pothole: go to **Report Incident**, choose category "
                                "'Pothole', describe the location clearly, and attach a photo if possible. "
                                "It will automatically be marked with a priority level.",
    r"report.*(garbage|trash|waste)": "To report a garbage issue: open **Report Incident**, select "
                                       "'Garbage', and mention the exact street/landmark so sanitation "
                                       "teams can locate it quickly.",
    r"(status|track).*(incident|report|complaint)": "You can track your reports from the **Report "
                                                      "Incident** page — your past submissions and their "
                                                      "current status are listed at the bottom.",
    r"(who|what).*(admin|resolve)": "Reported incidents are reviewed by municipal admins through the "
                                     "**Admin Dashboard**, where they update status to In Progress or "
                                     "Resolved.",
    r"(map|near me|nearby)": "Check the **Incident Map** page to see all reported civic issues plotted "
                              "by location, color-coded by status.",
    r"(civic sense|responsibility|clean|litter)": "Civic sense means taking small daily actions — not "
                                                    "littering, reporting hazards, conserving water and "
                                                    "electricity, and respecting public property — that "
                                                    "collectively keep our community safe and clean.",
    r"(thank|thanks)": "You're welcome! Together we can build a cleaner, safer community. 🙂",
}


def _rule_based_response(query: str) -> str:
    q = query.lower().strip()
    for pattern, response in FAQ_RESPONSES.items():
        if re.search(pattern, q):
            return response

    # Try to at least suggest a category if it looks like an incident description
    category, priority = classify_incident(q)
    if category != "Other":
        return (f"That sounds like it could be a **{category}** issue "
                f"(suggested priority: **{priority}**). Head to the Report Incident page to file it, "
                f"or ask me anything else about civic reporting.")

    return ("I can help with reporting civic issues (potholes, garbage, streetlights, water logging, "
            "sewage, and more), tracking complaint status, or explaining how the platform works. "
            "Could you rephrase your question?")


def _get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("ANTHROPIC_API_KEY")
    except Exception:
        return None


def get_ai_response(query: str, history=None) -> str:
    """
    Main entry point used by the AI Assistant page.
    Uses Claude via the Anthropic API if a key is configured, otherwise
    falls back to the offline rule-based assistant.
    """
    api_key = _get_api_key()
    if not api_key:
        return _rule_based_response(query)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        messages = []
        if history:
            for role, content in history[-6:]:
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": query})

        system_prompt = (
            "You are Civic Sense AI, a helpful assistant embedded in a citizen incident-reporting "
            "platform. Help users report civic issues (potholes, garbage, water logging, streetlights, "
            "sewage, illegal construction, stray animals, etc.), understand app features (Report "
            "Incident, Incident Map, Admin Dashboard), and encourage civic responsibility. Keep answers "
            "concise and practical."
        )

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
    except Exception as e:
        # Fail gracefully to the offline assistant rather than breaking the app
        fallback = _rule_based_response(query)
        return f"{fallback}\n\n_(Note: AI API call failed — using offline assistant. {e})_"
