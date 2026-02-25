import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="OCR + Text Input App", layout="centered")

st.title("📷 OCR + Text Input Web App")

# -------- OCR FUNCTION --------
def ocr_space(image_bytes):
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": "K86421971588957",  # 👈 PUT YOUR KEY HERE
        "language": "eng",
    }
    files = {
        "file": ("image.png", image_bytes)
    }
    response = requests.post(url, files=files, data=payload)
    result = response.json()

    if "ParsedResults" in result:
        return result["ParsedResults"][0]["ParsedText"]
    else:
        return "No text detected"

# -------- INPUT OPTIONS --------
option = st.radio(
    "Choose input type",
    ("Camera", "Upload Image", "Text Area")
)

extracted_text = ""

# -------- CAMERA INPUT --------
if option == "Camera":
    image = st.camera_input("Take a photo")

    if image:
        st.image(image, caption="Captured Image", use_column_width=True)
        extracted_text = ocr_space(image.getvalue())

# -------- IMAGE UPLOAD --------
elif option == "Upload Image":
    image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if image:
        st.image(image, caption="Uploaded Image", use_column_width=True)
        extracted_text = ocr_space(image.getvalue())

# -------- TEXT AREA --------
elif option == "Text Area":
    extracted_text = st.text_area("Enter text manually", height=200)

# -------- OUTPUT --------
st.subheader("📝 Final Text")
st.text_area("Editable text", extracted_text, height=250)

st.success("✅ Works on web & mobile!")
