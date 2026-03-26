import numpy as np
import os
import google.generativeai as genai

import streamlit as st
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)


# 🔥 Query Enhancer
def enhance_query(query):
    q = query.lower()
    keywords = []

    if any(w in q for w in ["kill", "murder", "shot", "gun", "dead"]):
        keywords.append("murder IPC 302 307 punishment")

    if any(w in q for w in ["hit", "fight", "attack", "hurt", "beat"]):
        keywords.append("assault IPC 351 352 323")

    if any(w in q for w in ["threat", "threaten"]):
        keywords.append("criminal intimidation IPC 503")

    if any(w in q for w in ["scam", "fraud", "cheat"]):
        keywords.append("cheating IPC 420")

    if any(w in q for w in ["steal", "theft", "rob"]):
        keywords.append("theft robbery IPC 378 390")

    keywords.append("IPC law crime punishment")

    return query + " " + " ".join(keywords)


# 🚀 MAIN FUNCTION
def get_response(query, model, index, ipc_sections):

    # 🔥 Step 1: Enhance query
    enhanced_query = enhance_query(query)
    print("Enhanced query:", enhanced_query)

    # 🔍 Step 2: FAISS search
    query_embedding = model.encode([enhanced_query]).astype("float32")
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)

    D, I = index.search(query_embedding, k=5)

    results = []
    for score, idx in zip(D[0], I[0]):
        results.append({
            "section": ipc_sections[idx]["section"],
            "chapter": ipc_sections[idx]["chapter"],
            "text": ipc_sections[idx]["text"],
            "score": float(score)
        })

    # 🔥 Filter + sort
    results = [r for r in results if r["score"] > 0.25]
    results = sorted(results, key=lambda x: x["score"], reverse=True)[:3]

    print("\n===== RETRIEVED =====")
    for r in results:
        print(r["section"], r["score"])

    # 🚫 Handle no results
    if not results:
        return {
            "sections": [],
            "analysis": "No relevant IPC sections found. Try describing the situation differently."
        }

    # 📦 Step 3: Context
    context = "\n\n".join([
        f"Section {r['section']} ({r['chapter']}): {r['text']}"
        for r in results
    ])

    # 🤖 Step 4: Prompt (NO JSON, just clean text)
    prompt = f"""
You are a legal assistant.

Explain the IPC sections in simple terms.

Structure your answer clearly with:
- Explanation
- Why it applies
- Example

Do NOT use HTML.
Write in clean paragraphs.

User situation:
{query}

Relevant IPC sections:
{context}
"""

    # 🚀 Step 5: Gemini call
    try:
        model_gemini = genai.GenerativeModel("gemini-2.5-flash")

        response = model_gemini.generate_content(
            prompt,
            generation_config={"temperature": 0.4}
        )

        raw_text = response.text or ""

    except Exception as e:
        print("Gemini Error:", e)
        return {
            "sections": results,
            "analysis": "AI service unavailable. Please try again."
        }

    print("\n===== GEMINI OUTPUT =====\n", raw_text)

    return {
        "sections": results,
        "analysis": raw_text.strip()
    }