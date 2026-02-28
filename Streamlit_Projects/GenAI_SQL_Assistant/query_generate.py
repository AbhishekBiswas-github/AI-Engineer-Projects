import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
import json
import sqlparse

def generate_query():
    st.write("")
    prompt = f"""You are a SQL Expert.

    Schema:
    Name of the table\n{st.session_state.table_name}\n\nBelow is the Column Schema\n{st.session_state.column_details}

    Business Intent: 
    {st.session_state.intent['business_intent']}
    
    Metrics:
    {st.session_state.intent['metrics']}
    
    Filters: 
    {st.session_state.intent['filters']}

    Optimization Instruction:
    {st.session_state.optimize}

    Rules:
    - Use SELECT only
    - No DELETE / UPDATE / DROP
    - Use explicit column names

"""
    systemPrompt = """
Generate an optimised SQL query.
        Return the output STRICTLY in this JSON format ONLY:

        {
            "code": "<SQL QUERY HERE>",
            "explanation": "<DETAILED EXPLANATION>"
        }

        DO NOT return any text outside of the JSON.
        DO NOT include markdown.
        DO NOT include backticks.

"""

    if not st.session_state.generate_status:
        with st.spinner("Generating Query...."):
            query_generated = st.session_state.chat_model.invoke([
                SystemMessage(content=systemPrompt),
                HumanMessage(content=prompt)
            ])

            # st.write(query_generated)
            response = json.loads(query_generated.content)
            formatted_query = sqlparse.format(
                response["code"],
                reindent=True,
                keyword_case="upper"
            )
            st.subheader("Generated SQL Statement")
            st.code(formatted_query, language="SQL")
            st.subheader("Query Explanation")
            st.info(f"""{response['explanation']}""")
            st.toast("✅ SQL Query Generated Successfully.")
            st.session_state.generate_status = True
            st.link_button("Link to Github Repo", url="https://github.com/AbhishekBiswas-github/GenAI_SQL_Assistant", type='primary')

    keys_to_clear = [
        "schema_status",
        "schema_validated",
        "query_status",
        "intent",
        "table_name",
        "column_details",
        "generate_status",
    ]

    if st.button("Reset Everything....", type='secondary'):
        for key in keys_to_clear:
            del st.session_state[key]
        st.rerun()