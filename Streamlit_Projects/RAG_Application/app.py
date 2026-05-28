import streamlit as st
from dotenv import load_dotenv, set_key
import os

load_dotenv()

st.set_page_config(
    layout="wide",
    page_title="QuickQuery"
)

if "db_connection" not in st.session_state:
    st.session_state["db_connection"] = "Connected"
if "model_connection" not in st.session_state:
    st.session_state["model_connection"] = "Connected"

with st.sidebar:
    st.header("Welcome to QuickQuery", text_alignment='center')

    @st.dialog("Configuration")
    def config():
        with st.form("my_form"):
            st.header("Database Credentials")
            host = st.text_input("Host", placeholder="Enter your Host", value="localhost")
            username = st.text_input("Username", placeholder="Enter your Username", value="root")
            port = st.text_input("Password", placeholder="Enter your Password", value=3306)
            password = st.text_input("Password", placeholder="Enter your Password", type="password", value=f"AbhiBoss@2508")
            database_name = st.text_input("Database Name", placeholder="Enter Database Name")
            if st.form_submit_button("Submit", type='primary', width="stretch"):
                set_key(".env", "HOST", host)
                set_key(".env", "USERNAME", username)
                set_key(".env", "DATABASE_PASSWORD", password)
                set_key(".env", "PORT", port)
                st.rerun()
    if st.button("⚙️ Configuration", type='primary', width="stretch"):
        config()
    
    st.divider()

    st.header("Connection status")
    st.write(f"Database Connection: {st.session_state["db_connection"]}")
    st.write(f"Model Connection: {st.session_state["model_connection"]}")

    st.divider()
    st.subheader(f"©️ 2026 - All rights reserved")


# Main Section
st.header("Welcome to QuickQuery - Your AI SQL Assistant")
st.text("Ask you question and agent with response with optimized SQL query")
with st.form("model_selection", width="stretch"):
    llm_model = st.selectbox(
        "Select your LLM Model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "whisper-large-v3-turbo"]
    )
    if st.form_submit_button("Choose", type="primary", width="stretch"):
        set_key(".env", "MODEL_NAME", llm_model)
st.chat_input(placeholder="Inter your Question")
with st.chat_message(name="user"):
    st.write("Sales of current year")
with st.chat_message(name="assistant"):
    st.write("Below is your sales")
