import os

import requests
import streamlit as st

st.set_page_config(page_title="Study Studio", page_icon="books", layout="centered")
st.title("Study Studio")
st.caption("One topic, a clearer explanation, and a quick self-check.")
topic = st.text_input("What are you learning?", placeholder="e.g. gradient descent")
level = st.selectbox("Explain it for", ["beginner", "high school", "undergraduate"])

if st.button("Build my study guide", type="primary", disabled=not topic):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        st.error("Set GEMINI_API_KEY in your environment, then restart the app.")
    else:
        prompt = f"For a {level} student studying {topic}, provide: a plain-language explanation, 5 concise revision bullets, and 3 multiple-choice questions with answers at the end. Be accurate and flag uncertainty."
        with st.spinner("Preparing your guide..."):
            try:
                response = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                    params={"key": key},
                    json={"contents": [{"parts": [{"text": prompt}]}]},
                    timeout=45,
                )
                response.raise_for_status()
                text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(text)
            except (requests.RequestException, KeyError, IndexError) as exc:
                st.error(f"The study guide could not be generated: {exc}")
