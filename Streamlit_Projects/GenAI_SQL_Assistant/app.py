import streamlit as st
import schema as sch
import query as qry
import query_generate as qry_g
from langchain_openai.chat_models import ChatOpenAI



st.set_page_config("GenAI SQL Assistant", layout='wide')
st.title("GenAI SQL Assistant")

if "schema_status" not in st.session_state:
    st.session_state.schema_status = False
if "schema_validated" not in st.session_state:
    st.session_state.schema_validated = False
if "query_status" not in st.session_state:
    st.session_state.query_status = False
if 'intent' not in st.session_state:
    st.session_state.intent = False
if 'generate_status' not in st.session_state:
    st.session_state.generate_status = False


st.session_state.chat_model = ChatOpenAI(model='gpt-4', seed=25, max_completion_tokens=500, temperature=0)


if not st.session_state.schema_status and not st.session_state.query_status:
    st.header("Database Schema Configuration", divider='blue')
    st.caption("Define the structural metadata of your dataset")
    col1, col2 = st.columns([1,1])
    with col1:
        sch.get_schema()
    with col2:
        if st.session_state.schema_validated:
            st.text_area("Schema Validation:",
                    value=f"""Name of the table {st.session_state.table_name}\n\nBelow is the Column Schema\n{st.session_state.column_details}""", 
                    height=330,
                    disabled=True
                )
            if st.button("Proceed", type="primary"):
                st.session_state.schema_status = True
                st.rerun()

elif st.session_state.schema_status and not st.session_state.query_status:
    st.header("Business Requirement Analysis", divider="red")
    st.caption("Translate natural langauge into structured analytical intent")
    col1, col2 = st.columns([1,2])
    with col1:
        qry.get_query()
    with col2:
        if st.session_state.intent:
            st.text_input("Extracted Business Intent", value=st.session_state.intent['business_intent'], disabled=True)
            st.text_input("Metrics Indentification", value=st.session_state.intent['metrics'][0], disabled=True)
            st.text_input("Filters Condition", value=st.session_state.intent['filters'], disabled=True)
            if st.button("Generate", type="primary"):
                st.session_state.query_status = True
                st.rerun()
            # st.write(st.session_state.intent)

elif st.session_state.query_status:
    st.header("SQL Query Generation", divider='yellow')
    st.caption("Generate optimized SQL based schema and extracted intent")
    qry_g.generate_query()
