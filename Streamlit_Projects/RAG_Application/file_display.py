import streamlit as st
import base64
from PyPDF2 import PdfReader

def display_pdf():
    # Read PDF file as bytes
    uploaded_file = st.session_state['file_details']['details']['file']
    pdf_bytes = uploaded_file.read()

    # Convert to base64
    base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    # Display PDF inside Streamlit
    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%"
        height="700"
        type="application/pdf">
    </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)

    # Extract text from all pages
    pdf_reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text() + "\n"

    # Display extracted text
    st.subheader("Extracted Text")
    st.text_area(
        "PDF Content",
        extracted_text,
        height=400
    )

    # st.write(uploaded_file)