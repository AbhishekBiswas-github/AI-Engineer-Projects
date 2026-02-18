import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.metrics import (
                            accuracy_score, 
                            confusion_matrix, 
                            classification_report,
                            precision_score,
                            recall_score,
                            f1_score,
                            roc_auc_score,
                            )

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

if 'model' not in st.session_state:
    st.session_state.model = ''

model = {
    'encoded': '',
    'x_train': '',
    'x_test': '',
    'y_train': '',
    'y_test': '',
    'model_name': '',
    'model':'',
    'model_accuracy': 0,
    'model_precision': 0,
    'model_recall': 0
}



def create_model():
    # Encode Categorical Variable
    df = st.session_state.dataset

    oe = OrdinalEncoder(categories=[[' Not Graduate', ' Graduate']])
    df['education'] = oe.fit_transform(df[['education']])

    oe = OrdinalEncoder(categories=[[' No', ' Yes']])
    df['self_employed'] = oe.fit_transform(df[['self_employed']])

    oe = OrdinalEncoder(categories=[[' Rejected', ' Approved']])
    df['loan_status'] = oe.fit_transform(df[['loan_status']])

    model['encoded'] = df

    # Splitting the dataset
    df = df.drop(columns='loan_id', axis=1)  # dropping the id columns
    model['X'] = df.drop(columns='loan_status', axis=1)
    y = df['loan_status']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(model['X'])
    X_scaled
    model['x_train'], model['x_test'], model['y_train'], model['y_test'] = train_test_split(X_scaled, y, test_size=0.2, random_state=25)

    log_model = LogisticRegression(max_iter=10000)
    log_model.fit(model['x_train'], model['y_train'])
    pred_log = log_model.predict(model['x_test'])
    if model['model_accuracy'] < round(accuracy_score(model['y_test'], pred_log)*100,2):
        model['model_accuracy'] = round(accuracy_score(model['y_test'], pred_log)*100,2)
        model['model_precision'] = round(precision_score(model['y_test'], pred_log)*100,2)
        model['model_recall'] = round(recall_score(model['y_test'], pred_log)*100,2)
        model['model_name'] = 'Logistic Regresstion'
        model['model'] = log_model

    dt_model = DecisionTreeClassifier()
    dt_model.fit(model['x_train'], model['y_train'])
    pred_dt = dt_model.predict(model['x_test'])
    if model['model_accuracy'] < round(accuracy_score(model['y_test'], pred_dt)*100,2):
        model['model_accuracy'] = round(accuracy_score(model['y_test'], pred_dt)*100,2)
        model['model_precision'] = round(precision_score(model['y_test'], pred_dt)*100,2)
        model['model_recall'] = round(recall_score(model['y_test'], pred_dt)*100,2)
        model['model_name'] = 'Decision Tree Classifier'
        model['model'] = dt_model

    rf_model = RandomForestClassifier()
    rf_model.fit(model['x_train'], model['y_train'])
    pred_rf = rf_model.predict(model['x_test'])
    if model['model_accuracy'] < round(accuracy_score(model['y_test'], pred_rf)*100,2):
        model['model_accuracy'] = round(accuracy_score(model['y_test'], pred_rf)*100,2)
        model['model_precision'] = round(precision_score(model['y_test'], pred_rf)*100,2)
        model['model_recall'] = round(recall_score(model['y_test'], pred_rf)*100,2)
        model['model_name'] = 'Random Forest Classifier'
        model['model'] = rf_model


    st.session_state.model = model
    pred = st.session_state.model['model'].fit(model['x_train'], model['y_train'])
    st.info(f"""
    Model Selected: {model['model_name']} \n
    Model Accuracy: {model['model_accuracy']}% \n
    Model Precision: {model['model_precision']}% \n
    Model Recall: {model['model_recall']}%
    """)

    
    cv_scores = cross_val_score(rf_model, model['X'], y, cv=20)
    n_iter = np.arange(1, 21)

    # Create figure and axis
    fig_cv, ax_cv = plt.subplots(figsize=(8, 5))

    # Plot CV scores
    ax_cv.plot(n_iter, cv_scores * 100, marker='o', label="CV Score")

    # Plot average line
    ax_cv.plot(
        n_iter,
        np.full(shape=20, fill_value=np.mean(cv_scores) * 100),
        linestyle='--',
        label='Average CV Score'
    )

    # Labels and title
    ax_cv.set_xlabel('Iterations')
    ax_cv.set_ylabel('Cross Validation Scores (%)')
    ax_cv.set_title('Cross Validation Scores Plot')
    ax_cv.legend()

    fig_hm, ax_hm = plt.subplots(figsize=(10, 5))
    sns.heatmap(model['encoded'].corr(), annot=True, cmap='magma', ax=ax_hm)
    plt.xlabel('Features', fontsize=18)
    plt.ylabel('Features', fontsize=18)
    plt.title("Correlation Heatmap between numerical fields", fontsize=18)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.pyplot(fig_cv)

    with col2:
        st.pyplot(fig_hm)


    st.toast("😄 Model Created successfully")

