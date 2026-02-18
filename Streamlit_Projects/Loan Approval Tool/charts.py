import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.DataFrame()

def show_insights():
    global df 
    df = st.session_state.dataset
    show_dataset()
    show_dataset_insights()
    show_charts()
    show_histogram()
    st.toast("😄 Insights Generated successfully")
    

def show_dataset():
    st.header("Dataset", divider="violet")
    st.dataframe(df, hide_index=True)

def show_dataset_insights():
    st.header("Understanding the data", divider="violet")
    st.subheader("Datatset Information", divider="rainbow")
    st.info(f"""Dataset Shape: {df.shape}""")
    st.subheader("Describe Numerical Columns", divider="rainbow")
    st.dataframe(df.describe(include=[np.number]))


def show_charts():
    st.header("Charts", divider="violet")

    st.subheader("Categorical Feature Analysis", divider="rainbow")

    df = st.session_state.dataset
    df.columns = df.columns.str.strip()
    
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x='education', hue='loan_status', palette='rainbow', ax=ax1)
    for p in ax1.patches:
        height = p.get_height()
        if height > 0:  # Only annotate bars with non-zero height
            ax1.text(
                p.get_x() + p.get_width() / 2,
                height + 0.5,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )
    # ax.legend_.remove()
    plt.xlabel('Education', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    plt.title('Loan Status Distribution based on Education', fontsize=16)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x='no_of_dependents', hue='loan_status', palette='magma', ax=ax2)
    for p in ax2.patches:
        height = p.get_height()
        if height > 0:  # Only annotate bars with non-zero height
            ax2.text(
                p.get_x() + p.get_width() / 2,
                height + 0.5,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )
    # ax.legend_.remove()
    plt.xlabel('Number of Dependents', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    plt.title('Loan Status Distribution based on Number of Dependents', fontsize=16)

    
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x='self_employed', hue='loan_status', palette='Set1', ax=ax3)
    for p in ax3.patches:
        height = p.get_height()
        if height > 0:  # Only annotate bars with non-zero height
            ax3.text(
                p.get_x() + p.get_width() / 2,
                height + 0.5,
                f'{int(height)}',
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )
    # ax.legend_.remove()
    plt.xlabel('Self Employed', fontsize=16)
    plt.ylabel('Frequency', fontsize=16)
    plt.title('Loan Status Distribution based on Self Employed', fontsize=16)
    
    col1, col2, col3 = st.columns([1, 1, 1])  # adjust ratio
    with col1:
        st.pyplot(fig1)

    with col2:
        st.pyplot(fig3)

    with col3: 
        st.pyplot(fig2)


def show_histogram():
    st.subheader("Histogram and KDE Plots", divider="rainbow")
    # 1️⃣ Income Distribution
    fig_h1, ax1 = plt.subplots(figsize=(6, 4))
    sns.histplot(df['income_annum'], kde=True, color='skyblue', ax=ax1)
    ax1.set_xlabel('Annual Income (INR)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Income Distribution')

    # 2️⃣ Loan Amount Distribution
    fig_h2, ax2 = plt.subplots(figsize=(6, 4))
    sns.histplot(df['loan_amount'], kde=True, color='lightgreen', ax=ax2)
    ax2.set_xlabel('Loan Amount (INR)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Loan Amount Distribution')

    # 3️⃣ CIBIL Score Distribution
    fig_h3, ax3 = plt.subplots(figsize=(6, 4))
    sns.histplot(df['cibil_score'], kde=True, color='salmon', ax=ax3)
    ax3.set_xlabel('CIBIL Score')
    ax3.set_ylabel('Frequency')
    ax3.set_title('CIBIL Score Distribution')

    # 4️⃣ Residential Assets Distribution
    fig_h4, ax4 = plt.subplots(figsize=(6, 4))
    sns.histplot(df['residential_assets_value'], kde=True, color='purple', ax=ax4)
    ax4.set_xlabel('Residential Assets Value (INR)')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Residential Assets Value Distribution')

    # 5️⃣ Commercial Assets Distribution
    fig_h5, ax5 = plt.subplots(figsize=(6, 4))
    sns.histplot(df['commercial_assets_value'], kde=True, color='orange', ax=ax5)
    ax5.set_xlabel('Commercial Assets Value (INR)')
    ax5.set_ylabel('Frequency')
    ax5.set_title('Commercial Assets Value Distribution')

    # 6️⃣ Luxury Assets Distribution
    fig_h6, ax6 = plt.subplots(figsize=(6, 4))
    sns.histplot(df['luxury_assets_value'], kde=True, color='blue', ax=ax6)
    ax6.set_xlabel('Luxury Assets Value (INR)')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Luxury Assets Value Distribution')

    
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.pyplot(fig_h1)
        st.pyplot(fig_h3)
    
    with col2:
        st.pyplot(fig_h5)
        st.pyplot(fig_h2)

    with col3:
        st.pyplot(fig_h4)
        st.pyplot(fig_h6)


    fig_lt, ax_lt = plt.subplots(figsize=(10, 5))
    ax = sns.barplot(data=df.sort_values('loan_term'), x='loan_term', y='loan_amount', estimator=np.mean, errorbar=None, hue='loan_term', palette='rainbow', ax=ax_lt)
    for p in ax_lt.patches:
        height = p.get_height()
        if height > 0:
            label = f"{height/1e6:.2f}M"
            ax_lt.text(
                p.get_x() + p.get_width() / 2,
                height + 2e5,
                label,
                va='bottom',
                ha='center',
                fontsize=10,
                color='black'     
            )
    ax.legend_.remove()
    plt.xlabel("Loan Tenure (in years)")
    plt.ylabel("Average Loan Amount (in INR)")
    plt.title("Total Loan Amount based on Loan Tenure")
    plt.tight_layout(h_pad=30)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Loan Tenure Trend", divider="rainbow")
        st.pyplot(fig_lt)

    st.session_state.insights_shown = True