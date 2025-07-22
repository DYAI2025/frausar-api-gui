
import streamlit as st
import json
from difflib import SequenceMatcher

# Load marker data
with open("marker_knowledge_base.json", "r", encoding="utf-8") as f:
    markers = json.load(f)

# Similarity function
def is_similar(a, b, threshold=0.6):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

# Streamlit UI
st.title("Love Scam Marker Tester")

user_input = st.text_area("Gib hier einen Chatverlauf oder Nachricht ein:")

if st.button("Analysieren"):
    if not user_input.strip():
        st.warning("Bitte Text eingeben.")
    else:
        matched = []
        total_score = 0

        for marker in markers:
            example = marker["beispiel"]
            if is_similar(user_input, example):
                matched.append(marker)
                total_score += marker.get("score", 3)

        st.subheader("Erkannte Marker")
        if matched:
            for m in matched:
                st.markdown(f"**Kategorie:** {m['kategorie']}")
                st.markdown(f"- Beispiel: _{m['beispiel']}_")
                st.markdown(f"- Risiko-Score: {m['score']}")
                st.markdown("---")
            st.success(f"📊 Gesamtrisiko-Score: {total_score}")
        else:
            st.info("Keine passenden Marker erkannt.")
