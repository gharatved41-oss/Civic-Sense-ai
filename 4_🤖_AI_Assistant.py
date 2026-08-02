"""
pages/4_🤖_AI_Assistant.py
Chat interface for the Civic Sense AI Assistant.
Works offline (rule-based) out of the box; upgrades automatically to
Claude if an ANTHROPIC_API_KEY is configured.
"""

import streamlit as st
import auth
import style
from ai_assistant import get_ai_response

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
auth.require_login()
style.inject_css()

style.hero("🤖 Civic Sense AI Assistant",
           "Ask about reporting issues, tracking complaints, or general civic responsibility.",
           eyebrow="Always Online")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        ("assistant", "Hi! I'm your Civic Sense AI Assistant. Ask me how to report an issue, "
                      "track a complaint, or anything about civic responsibility.")
    ]

for role, content in st.session_state.chat_history:
    avatar = "🤖" if role == "assistant" else "🧑"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

prompt = st.chat_input("Type your question here...")
if prompt:
    st.session_state.chat_history.append(("user", prompt))
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Map to Anthropic API roles for history context
    api_history = [("user" if r == "user" else "assistant", c) for r, c in st.session_state.chat_history[:-1]]

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt, history=api_history)
        st.markdown(response)

    st.session_state.chat_history.append(("assistant", response))

st.divider()
with st.expander("💡 Try asking..."):
    qcol1, qcol2 = st.columns(2)
    with qcol1:
        st.markdown("- How do I report a pothole?\n- Where can I see nearby incidents?")
    with qcol2:
        st.markdown("- How do I track my complaint?\n- What is civic sense?")
