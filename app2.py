import streamlit as st
import random
from PIL import Image
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ELCOT\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="Objective Question Generator")

st.title("📝 Objective Question Generator")
st.write("Use text input, camera input, or both")

# -------- TEXT INPUT --------
typed_text = st.text_area("✍️ Enter text manually", height=150)

# -------- CAMERA INPUT --------
image = st.camera_input("📷 Capture text using camera")

ocr_text = ""

if image is not None:
    try:
        img = Image.open(image)
        ocr_text = pytesseract.image_to_string(img)
    except Exception as e:
        st.warning("OCR temporarily unavailable.")

# -------- COMBINE TEXT --------
final_text = typed_text + " " + ocr_text

# -------- QUESTION GENERATOR --------
def generate_mcqs(text):
    sentences = [s.strip() for s in text.split(".") if len(s.split()) > 6]
    questions = []

    for sent in sentences:
        words = sent.split()
        answer = random.choice(words)
        question = sent.replace(answer, "______", 1)

        options = random.sample(words, min(4, len(words)))
        if answer not in options:
            options[0] = answer

        questions.append((question, options, answer))

    return questions

# -------- BUTTON --------
if st.button("Generate Objective Questions"):
    if not final_text.strip():
        st.warning("Please enter text or use the camera.")
    else:
        mcqs = generate_mcqs(final_text)

        if not mcqs:
            st.error("Not enough content to generate questions.")
        else:
            for i, (q, options, ans) in enumerate(mcqs, 1):
                st.subheader(f"Q{i}. {q}")
                st.radio("Choose an option:", options, key=i)
                st.caption(f"✅ Correct Answer: {ans}")
                st.divider()

