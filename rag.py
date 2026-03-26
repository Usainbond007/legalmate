import numpy as np
import json

import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def enhance_query(query):
    q = query.lower()
    keywords = []

    if any(w in q for w in ["kill", "murder", "shot", "gun", "dead"]):
        keywords.append("murder attempt IPC 302 307")

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


def get_response(query, model, index, ipc_sections):

    # 🔥 Step 1: Enhance query
    enhanced_query = enhance_query(query)
    print("Enhanced query:", enhanced_query)

    query_embedding = model.encode([enhanced_query]).astype("float32")
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)

    # 🔍 Step 2: FAISS search
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
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    results = results[:3]

    print("\n===== RETRIEVED =====")
    for r in results:
        print(r["section"], r["score"])

    # 📦 Step 3: Context
    context = "\n\n".join([
        f"Section {r['section']} ({r['chapter']}): {r['text']}"
        for r in results
    ])

    # 🤖 Step 4: Gemini prompt
    prompt = f"""
You are a legal assistant.

Explain the IPC sections in simple terms.

User situation:
{query}

Relevant IPC sections:
{context}

Return ONLY valid JSON:
{{
  "simple_explanation": "...",
  "why_it_applies": "...",
  "example": "..."
}}
"""

    # 🚀 Step 5: Gemini API call (NEW SDK STYLE)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw_text = response.text
    print("\n===== GEMINI OUTPUT =====\n", raw_text)

    # 🔥 Step 6: Safe parsing
    try:
        # First level parse
        outer = json.loads(raw_text)

        # If Gemini already returned proper JSON
        if isinstance(outer, dict):
            llm_output = outer
        else:
            raise ValueError("Not dict")

    except:
        try:
            # Try extracting JSON inside text
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            json_str = raw_text[start:end]

            llm_output = json.loads(json_str)

        except:
            llm_output = {
                "simple_explanation": raw_text,
                "why_it_applies": "",
                "example": ""
            }

    return {
        "sections": results,
        "analysis": llm_output
    }