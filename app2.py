import streamlit as st
import requests
import random
import re

st.set_page_config(page_title="Text to MCQ Generator", layout="centered")
st.title("📷 Text → MCQ Generator")

# ---------------- OCR FUNCTION ----------------
def ocr_space(image_bytes):
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": "K86421971588957",
        "language": "eng",
        "isOverlayRequired": False,
        "scale": True,
        "OCREngine": 2,
    }
    files = {
        "file": ("image.jpg", image_bytes)
    }

    response = requests.post(url, files=files, data=payload)
    result = response.json()

    # DEBUG INFO
    if result.get("IsErroredOnProcessing"):
        st.error(result.get("ErrorMessage"))
        return ""

    parsed = result.get("ParsedResults")
    if parsed and parsed[0].get("ParsedText"):
        return parsed[0]["ParsedText"].strip()

    st.warning("⚠️ OCR could not detect readable text. Try better lighting or clearer image.")
    return ""

# ---------------- MCQ GENERATOR ----------------
def generate_mcqs(text, num_questions=5):
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.split()) > 6]

    mcqs = []
    random.shuffle(sentences)

    for sentence in sentences[:num_questions]:
        words = sentence.split()
        answer = random.choice(words)

        question = sentence.replace(answer, "______", 1)

        options = random.sample(words, min(3, len(words)))
        if answer not in options:
            options.append(answer)

        options = list(set(options))
        random.shuffle(options)

        mcqs.append({
            "question": question,
            "options": options,
            "answer": answer
        })

    return mcqs

# ---------------- INPUT OPTIONS ----------------
option = st.radio(
    "Choose input type",
    ("Camera", "Upload Image", "Text Area")
)

st.subheader("📄 Extracted / Input Text")

input_text = st.text_area(
    "Editable text",
    value=input_text if input_text else "",
    height=220
)

# Image Upload
elif option == "Upload Image":
    image = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])
    if image:
        st.image(image, use_column_width=True)
        input_text = ocr_space(image.getvalue())

# Text Area
elif option == "Text Area":
    input_text = st.text_area("Enter text", height=200)

# ---------------- OUTPUT ----------------
st.subheader("📄 Extracted / Input Text")
input_text = st.text_area("Editable text", input_text, height=200)

if st.button("🎯 Generate MCQs"):
    if input_text.strip() == "":
        st.warning("Please enter text or capture an image first")
    else:
        mcqs = generate_mcqs(input_text)

        st.subheader("📝 Generated Questions")
        for i, mcq in enumerate(mcqs, 1):
            st.markdown(f"**Q{i}. {mcq['question']}**")
            for opt in mcq["options"]:
                st.markdown(f"- {opt}")
            st.markdown(f"✅ **Answer:** {mcq['answer']}")
            st.divider()
            st.markdown(f"✅ **Answer:** {mcq['answer']}")
            st.divider()


