import streamlit as st
import cv2
import easyocr
import numpy as np
import re

st.title("📋 Job Reference Extractor")

uploaded_file = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # OCR with easyocr
    reader = easyocr.Reader(['en'])
    result = reader.readtext(gray)

    # Combine text
    text = " ".join([r[1] for r in result])

    # Regex for job ref
    match = re.search(r"(J-[A-Z0-9]{8})", text)

    st.subheader("🔎 OCR Result")
    st.text(text)
    if match:
        st.success(f"✅ Job Reference Found: {match.group(1)}")
    else:
        st.error("❌ No job reference found.")

