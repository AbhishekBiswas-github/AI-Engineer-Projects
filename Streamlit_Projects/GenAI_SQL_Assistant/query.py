import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
import json


def get_query():
    st.session_state.business_query = st.text_input("Business Question Input", value=None, placeholder="Enter business query")
    if st.button("Show Intent", type='primary'):
        prompt = f"""
        Extract the business intent, metrics and filter from the below user quesion:

        Question:
        {st.session_state.business_query}

        return in below JSON format
        {{
            "business_intent": "...."
            "metrics": [.....]
            "filters": "...."
        }}
        """
        chat_message = st.session_state.chat_model.invoke([
            SystemMessage(content="You are a business analytics expert"),
            HumanMessage(content=prompt)
        ])
        response_json = json.loads(chat_message.content)
        st.session_state.intent = response_json
        st.toast("✅ Intent Generated Successfully.")