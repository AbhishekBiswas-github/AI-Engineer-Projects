import streamlit as st
import google.generativeai as genai

def display_key():
    st.write(st.session_state)

    # # Configure API Key
    # genai.configure(api_key=st.session_state['api_key'])

    # # Load Gemini model
    # model = genai.GenerativeModel("gemini-1.3")

    # # Generate response
    # response = model.generate_content("Explain RAG in simple terms")

    # print(response.text)