import streamlit as st
import numpy as np
from sklearn.preprocessing import StandardScaler
from streamlit_js_eval import streamlit_js_eval
import time

def start_prediction():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Section 1")
        number_of_dependencies = st.slider("Number of Dependencies of the Applicant", 0, 100)
        income_annual = st.number_input("Annual Income of the Applicant", placeholder="Annual Income", value=None)
        loan_amount = st.number_input("Loan Amount Requested by the Applicant", placeholder="Loan Amount", value=None, min_value=10000)
        loan_term = st.slider("Loan Term (in years) of the Applicant", 1, 50)
        cibil_score = st.number_input("Cibil Score of the Applicant", placeholder="Cibil Score", value=None)
        bank_asset_value   = st.number_input("Bank Asset Value of the Applicant", placeholder="Bank Asset Value", value=None)

    with col2:
        st.subheader("Section 2")
        education = 0 if st.selectbox("What is your education", options=['Not Graduate', 'Graduate']) == 'Not Graduate' else 1
        self_employed = 1 if st.selectbox("Are you self employed", options=['Yes', 'No']) else 0
        
        residential_assets_value  = st.number_input("Residential Asset Value of the Applicant", placeholder="Residential Asset Value", value=None)
        commercial_assets_value  = st.number_input("Commercial Asset Value of the Applicant", placeholder="Commercial Asset Value", value=None)
        luxury_assets_value  = st.number_input("Luxury Asset Value of the Applicant", placeholder="Luxury Asset Value", value=None)
        
    user_input_value = np.array([[number_of_dependencies, education, self_employed, income_annual, loan_amount, loan_term, cibil_score, residential_assets_value, 
                        commercial_assets_value, luxury_assets_value, bank_asset_value]])
    
    scaler = StandardScaler()
    scaler.fit(st.session_state.model['X'])
    new_input_scaled = scaler.transform(user_input_value)
    pred = st.session_state.model['model'].predict(new_input_scaled)
    
    # st.write(user_input_value)
    # st.write(pred)

    if loan_amount is not None:
        if st.button("Get the Status", type='primary'):
            st.info("😄 You loan got approved") if pred == 1 else st.error("😔 You loan didn't got approved")

            
    if st.button("Reset Everything....", type="secondary", key="reset_btn"):
        with st.spinner("Wait for it...", show_time=True):
            time.sleep(5)
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

    
