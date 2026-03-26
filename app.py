import streamlit as st
from rag import get_response
from embedcheck import load_faiss

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="centered")

# 🔥 Load backend once
@st.cache_resource
def load_backend():
    return load_faiss()

model, index, ipc_sections = load_backend()

# 🔥 Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: #ffffff;
}

.title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #b0b3b8;
    margin-bottom: 30px;
}

.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-top: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.3);
    line-height: 1.6;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 8px;
}

.small-text {
    color: #9aa0a6;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# 🔥 Header
st.markdown('<div class="title">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Understand IPC laws in simple language</div>', unsafe_allow_html=True)

# 🔥 Input box
query = st.text_area("Describe your situation:", height=120)

# 🔥 Analyze button
if st.button("Analyze"):

    if not query.strip():
        st.warning("Please enter a valid situation.")
    else:
        with st.spinner("Analyzing your situation..."):
            result = get_response(query, model, index, ipc_sections)

        # 🔥 Sections
        st.markdown("### 📜 Relevant IPC Sections")

        if result.get("sections"):
            for sec in result["sections"]:
                st.markdown(f"""
                <div class="card">
                    <div class="section-title">Section {sec['section']}</div>
                    <div class="small-text">{sec['chapter']}</div>
                    <p>{sec['text'][:250]}...</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No relevant IPC sections found.")

        # 🔥 Analysis (UPDATED — no JSON nonsense)
        analysis = result.get("analysis", "No response")

        st.markdown("### 🧠 Simple Explanation")

        st.markdown(f"""
        <div class="card">
        {analysis}
        </div>
        """, unsafe_allow_html=True)

# 🔥 Footer
st.markdown("""
<br><br>
<div class="small-text" style="text-align:center;">
⚠️ This is not legal advice. For educational purposes only.
</div>
""", unsafe_allow_html=True)