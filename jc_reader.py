import streamlit as st
import cv2
import pytesseract
import re
import numpy as np

pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.set_page_config(page_title="Job Ref Extractor", page_icon="📋")

st.title("📋 Job Reference Extractor")
st.write("Upload a meter photo and I'll pull out the job reference (e.g. `J-64E1F000`).")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Read file as numpy array
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
    )[1]

    # OCR
    text = pytesseract.image_to_string(gray, config="--psm 6")

    # Find job reference pattern
    match = re.search(r"(J-[A-Z0-9]{8})", text)

    st.subheader("🔎 OCR Result")
    st.text(text)

    if match:
        st.success(f"✅ Job Reference Found: {match.group(1)}")
    else:
        st.error("❌ No job reference found.")
