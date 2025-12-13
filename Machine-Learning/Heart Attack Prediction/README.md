# ❤️ Heart Attack Prediction using Machine Learning

This project aims to predict the risk of a heart attack in individuals based on various medical parameters using supervised machine learning models. Early detection and prediction can help save lives by allowing timely medical intervention.

---

## 📌 Project Overview

Cardiovascular diseases are one of the leading causes of death globally. Predicting heart disease early can significantly improve treatment outcomes. This machine learning project leverages patient data to build a model that can help predict the presence of heart disease.

---

## 🧠 Problem Statement

Given a dataset of medical attributes, the goal is to build a classification model to predict whether a person is likely to have a heart disease (1) or not (0).

---

## 📁 Dataset Description

The dataset contains 14 attributes related to health and diagnosis:

| Feature      | Description |
|--------------|-------------|
| **Age** | Age of the person (in years) |
| **Sex** | Gender (1 = male, 0 = female) |
| **ChestPain** | Chest pain type (1–typical angina, 2–atypical angina, 3–non-anginal, 4–asymptomatic) |
| **Restbps** | Resting blood pressure (mmHg) |
| **Chol** | Serum cholesterol (mg/dL) |
| **Fbs** | Fasting blood sugar > 120 mg/dL (1 = true, 0 = false) |
| **RestECG** | Resting ECG results (0 = normal, 1 = ST-T abnormality, 2 = left ventricular hypertrophy) |
| **MaxHR** | Maximum heart rate achieved |
| **Exang** | Exercise induced angina (1 = yes, 0 = no) |
| **Oldpeak** | ST depression induced by exercise |
| **Slope** | Slope of peak exercise ST segment (0 = upsloping, 1 = flat, 2 = downsloping) |
| **Ca** | Number of major vessels colored by fluoroscopy (0–3) |
| **Thal** | Thalassemia (0 = normal, 1 = fixed defect, 2 = reversible defect) |
| **Target** | Diagnosis of heart disease (1 = disease, 0 = no disease) |

---

## 🧰 Tools & Libraries Used

- Python
- Pandas
- NumPy
- Matplotlib & Seaborn
- Scikit-learn

---

## 🚀 Project Workflow

### 1️⃣ Exploratory Data Analysis (EDA)
- Inspected data using `.info()`, `.describe()`, and `.isnull()`
- Visualized distributions and relationships
  - Histograms, KDE plots, borplots
  - Correlation heatmap

### 2️⃣ Data Preprocessing
- Feature-target split
- Feature scaling using `StandardScaler`
- Train-test split (80/20)

### 3️⃣ Model Building
Trained and compared the following classifiers:
- **Logistic Regression**
- **Decision Tree Classifier**
- **Random Forest Classifier** *(Final selected model)*

### 4️⃣ Model Evaluation
Evaluated model performance using:
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Classification Report

### 5️⃣ Cross Validation
- Applied K-Fold Cross Validation to validate model stability

### 6️⃣ Prediction on New Data
- Tested the final model with new/unseen input

---

## 📊 Results

The **Random Forest Classifier** provided the best performance with:
- High accuracy (around 80%)
- Strong recall (especially important in health-related predictions)
- Good generalization (via cross-validation)
