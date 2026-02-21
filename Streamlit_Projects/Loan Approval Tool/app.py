import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time

import charts as ct
import model as ml
import prediction as pred

if 'dataset' not in st.session_state:
    st.session_state.dataset = pd.DataFrame()
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'insights_shown' not in st.session_state:
    st.session_state.insights_shown = False
if 'model_created' not in st.session_state:
    st.session_state.model_created = False
if 'predicted' not in st.session_state:
    st.session_state.predicted = False


def file_uploaded():
    st.session_state.file_uploaded = True

def insight_shown():
    st.session_state.insights_shown = True

def model_created():
    st.session_state.model_created = True

def start_prediction():
    st.session_state.predicted = True

st.set_page_config(page_title="Loan Approval Tool", layout='wide')

st.title("Loan Approval Tool")

# File upload page
if not st.session_state.file_uploaded:
    st.subheader('Upload your file', divider='rainbow')

    if st.button("Load Dataset", type='primary'):
        my_bar = st.progress(0, "Reading the Dataset")
        
        for percentage_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percentage_complete+1, "Reading the Dataset")   

        time.sleep(1)
        my_bar.empty()

        url = "https://raw.githubusercontent.com/AbhishekBiswas-github/AI-Engineer-Projects/refs/heads/main/Machine-Learning/Loan-Approval-Prediction/loan_approval_dataset.csv"

        df = pd.read_csv(url)
        st.toast("😄 File uploaded successfully")
        st.session_state.dataset = df

        st.info("Dataset Loaded Successfully")
        if st.button(label="Show Insights", on_click=file_uploaded, type='primary'):
            st.write("File uploaded, show Dataset....")
                # st.rerun()

# Show insights page
elif st.session_state.file_uploaded and not st.session_state.model_created:
    ct.show_insights()

    if st.button(label="Create Model", on_click=model_created, type='primary'):
        st.write("Insights Shown....")
        

# model creation page
if st.session_state.model_created and not st.session_state.predicted:
    st.header("Model Creation and Prediction", divider="violet")
    ml.create_model()

    if st.button(label="Start Prediction", on_click=start_prediction, type='primary'):
        st.write("Start Prediction....")

elif st.session_state.predicted:
    st.header('Fill the Form to check the status of your loan', divider='rainbow')
    pred.start_prediction()
