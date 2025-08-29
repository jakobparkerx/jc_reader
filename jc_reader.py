import streamlit as st
import numpy as np
import cv2
import easyocr
import re

st.title("📋 Job Reference Extractor")

@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'])

reader = get_reader()

uploaded_file = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    with st.spinner("Scanning for Job Reference..."):
        result = reader.readtext(gray)
        text = " ".join([r[1] for r in result])
        normalized_text = text.replace('O', '0')
        
        match = re.search(r"(J-[A-Z0-9]{8})", normalized_text)

    if match:
        st.success(f"✅ Job Reference Found: {match.group(1)}")
    else:
        st.error("❌ No job reference found.")


