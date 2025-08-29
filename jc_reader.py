import streamlit as st
import easyocr

st.title("OCR Test")

@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'])

reader = get_reader()

st.write("Reader loaded successfully!")



