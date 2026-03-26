import pdfplumber
import re
import json


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def preprocess_ipc(text):

    # --------------------------------------------------
    # 1️⃣ Cut everything before ACT NO.
    # --------------------------------------------------
    act_match = re.search(
        r'ACT\s+NO\.\s*\d+\s+OF\s+\d{4}',
        text,
        re.IGNORECASE
    )

    if act_match:
        text = text[act_match.start():]

    # --------------------------------------------------
    # 2️⃣ Remove ARRANGEMENT OF SECTIONS block
    # --------------------------------------------------
    text = re.sub(
        r'ARRANGEMENT OF SECTIONS.*?CHAPTER I',
        'CHAPTER I',
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    # --------------------------------------------------
    # 3️⃣ Clean footnote-style section markers like 8[14.
    # --------------------------------------------------
    text = re.sub(r'\d+\[(\d+[A-Z]?\.)', r'\1', text)

    structured_sections = []
    current_chapter = "Unknown"

    # --------------------------------------------------
    # 4️⃣ Split by chapters
    # --------------------------------------------------
    chapter_pattern = r'(?m)^(CHAPTER\s+[IVXLC]+)'
    chapter_parts = re.split(chapter_pattern, text)

    for part in chapter_parts:

        if part.strip().upper().startswith("CHAPTER"):
            current_chapter = part.strip()
        else:

            # --------------------------------------------------
            # 5️⃣ Split by potential section numbers
            # --------------------------------------------------
            section_pattern = r'(?m)^\s*(\d+[A-Z]?\.)\s'
            section_parts = re.split(section_pattern, part)

            for i in range(1, len(section_parts), 2):

                section_number_raw = section_parts[i]
                section_content = section_parts[i + 1] if i + 1 < len(section_parts) else ""

                section_number = section_number_raw.replace(".", "").strip()
                full_text = (section_number_raw + " " + section_content).strip()

                # --------------------------------------------------
                # 6️⃣ Accept only real IPC sections
                # Must contain ".—" (dot + em dash)
                # --------------------------------------------------
                if not re.search(r'\d+[A-Z]?\.\s.*?—', full_text):
                    continue

                structured_sections.append({
                    "chapter": current_chapter,
                    "section": section_number,
                    "text": full_text
                })

    return structured_sections


def main():
    pdf_path = "data/ipc.pdf"
    print("Extracting text...")
    print("Loading model...")
    raw_text = extract_text_from_pdf(pdf_path)

    print("Processing IPC structure...")
    structured_data = preprocess_ipc(raw_text)

    print(f"Total sections extracted: {len(structured_data)}")

    with open("ipc_structured.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)

    print("Saved to ipc_structured.json")


if __name__ == "__main__":
    main()
