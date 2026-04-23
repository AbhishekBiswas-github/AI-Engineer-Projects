import streamlit as st
import check_key_config as check_key
import file_display as file_show

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

if 'api_validation' not in st.session_state:
    st.session_state['api_validation'] = False

if 'file_details' not in st.session_state:
    st.session_state['file_details'] = {
        'file_present': False,
        'details': ''
    }

st.set_page_config("RAG BASED APPLICATION", layout="wide")

st.markdown(
    """
    <style>
    .st-emotion-cache-1s8qyds h1 {
        color: red;
        text-align: center;
        font-size: 42px;
    }
    .st-emotion-cache-1permvm{
        display: flex;
        align-items: end;
        justify-content: end;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("RAG BASED APPLICATION")


if not st.session_state['api_validation']:
    col1, col2 = st.columns([6,1])
    with col1:
        api_key = st.text_input("", placeholder="Enter your API KEY", type="password")
    with col2: 
        link = st.button("Link to the LLM model", type='primary')

    if api_key:
        st.session_state['api_key'] = api_key

    if link:
        st.session_state['api_validation'] = True
        check_key.display_key()

if st.session_state['api_validation'] and not st.session_state['file_details']['file_present']:
    st.header("Data Ingestion", divider='rainbow')
    file = st.file_uploader("Upload your file", type=['pdf', 'docx'])
    if file:
        file_details = {
            'file': file,
            'file_id': file.file_id,
            'name': file.name,
            'type': file.type.split('/')[1],
            'size': f"{file.size}mb",
            'upload_url': file._file_urls.upload_url,
            'delete_url': file._file_urls.delete_url
        }
        st.session_state['file_details'] = {
            'file_present': True,
            'details': file_details
        }
    
    if st.session_state['file_details']['file_present']:
        file_show.display_pdf()
        
st.write(st.session_state)