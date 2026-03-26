import json
import numpy as np
import faiss

from sentence_transformers  import SentenceTransformer
def load_faiss():
    print("Loading IPC sections...")
    with open("ipc_structured.json", "r", encoding="utf-8") as f:
        ipc_sections = json.load(f  )
    print(f"Total sections loaded: {len(ipc_sections)}")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded successfully!") 
    section_texts = [
    f"""
    IPC Section {sec['section']}
    Chapter: {sec['chapter']}
    Crime law punishment offense:
    {sec['text']}
    """
    for sec in ipc_sections
]
    print("Generating embeddings...")
    embeddings = model.encode(section_texts, show_progress_bar=True,convert_to_numpy=True)
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)  
    
    return model,index,ipc_sections


        
