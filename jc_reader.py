import streamlit as st
import numpy as np
import cv2
import easyocr
import re

st.title("📋 Job Reference Extractor")

uploaded_file = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray)

    text = " ".join([r[1] for r in result])

    # Normalize OCR errors: replace 'O' with '0'
    normalized_text = text.replace('O', '0')

    match = re.search(r"(J-[A-Z0-9]{8})", normalized_text)

    st.subheader("🔎 OCR Result")
    st.text(text)
    st.text(f"Normalized Text: {normalized_text}")

    if match:
        st.success(f"✅ Job Reference Found: {normalized_text}")
")
    else:
        st.error("❌ No job reference found.")


