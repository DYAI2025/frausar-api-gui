
import streamlit as st
import json
from sentence_transformers import SentenceTransformer, util

# Load semantic model
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# Load marker knowledge
with open("marker_knowledge_compact.json", "r", encoding="utf-8") as f:
    markers = json.load(f)

st.title("Love Scam Marker Tester – Semantisch")

user_text = st.text_area("Gib hier einen Test-Chat oder Text ein:", height=200)

threshold = st.slider("Semantische Ähnlichkeitsschwelle (0.0 = alles matcht, 1.0 = fast identisch)", 0.0, 1.0, 0.7, step=0.01)

if st.button("Scannen"):
    matched = []
    user_embedding = model.encode(user_text, convert_to_tensor=True)

    for marker in markers:
        marker_embedding = model.encode(marker["beispiel"], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(user_embedding, marker_embedding).item()
        if similarity >= threshold:
            matched.append({
                "beispiel": marker["beispiel"],
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
