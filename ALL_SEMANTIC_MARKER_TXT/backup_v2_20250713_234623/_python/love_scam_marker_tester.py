
import streamlit as st
import json
import difflib

# Load marker knowledge
with open("marker_knowledge_compact.json", "r", encoding="utf-8") as f:
    markers = json.load(f)

st.title("Love Scam Marker Tester")

user_text = st.text_area("Gib hier einen Test-Chat oder Text ein:", height=200)

threshold = st.slider("Ähnlichkeitsschwelle (0.0 = sehr locker, 1.0 = sehr streng)", 0.0, 1.0, 0.75, step=0.01)

if st.button("Scannen"):
    matched = []
    for marker in markers:
        example = marker["beispiel"]
        similarity = difflib.SequenceMatcher(None, example.lower(), user_text.lower()).ratio()
        if similarity >= threshold:
            matched.append({
                "beispiel": example,
                "kategorie": marker["kategorie"],
                "score": marker["score"],
                "similarity": round(similarity, 2)
            })

    if matched:
        total_score = sum(m["score"] for m in matched)
        st.success(f"⚠️ {len(matched)} Marker erkannt – Gesamtrisiko-Score: {total_score}")
        for m in matched:
            st.markdown(
                f"""**Beispiel:** {m['beispiel']}  
**Kategorie:** {m['kategorie']}  
**Score:** {m['score']}  
**Ähnlichkeit:** {m['similarity']}"""
            )
    else:
        st.info("✅ Keine passenden Marker gefunden.")
