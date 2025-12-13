# House Price Prediction

This repository contains a machine learning project for predicting residential house prices based on various property features. The project encompasses the full data science workflow—from data exploration and preprocessing to model training, evaluation, and deployment-ready prediction functions.

---

## Project Overview

Predicting house prices is a key challenge in real estate analytics, helping buyers, sellers, and professionals make informed decisions. This project uses a dataset with several housing attributes such as area, number of bedrooms and bathrooms, amenities, and furnishing status to build regression models that accurately estimate house prices.

---

## Dataset Description

The dataset includes the following features:

| Feature Name         | Description                                                                        | Type        |
|----------------------|------------------------------------------------------------------------------------|-------------|
| Price                | The target variable—the price of the house                                        | Numeric     |
| Area                 | Total area of the house in square feet                                            | Numeric     |
| Bedrooms             | Number of bedrooms                                                                 | Integer     |
| Bathrooms            | Number of bathrooms                                                                | Integer     |
| Stories              | Number of stories                                                                 | Integer     |
| Mainroad             | Whether house is connected to the main road (Yes/No)                              | Categorical |
| Guestroom            | Presence of guest room (Yes/No)                                                    | Categorical |
| Basement             | Presence of basement (Yes/No)                                                      | Categorical |
| Hot water heating    | Hot water heating system presence (Yes/No)                                        | Categorical |
| Airconditioning      | Air conditioning system presence (Yes/No)                                         | Categorical |
| Parking              | Number of parking spaces                                                          | Integer     |
| Prefarea             | Location in preferred area (Yes/No)                                               | Categorical |
| Furnishing status    | Furnishing status (Fully Furnished, Semi-Furnished, Unfurnished)                   | Categorical |

---

## Project Structure

- **1. Exploratory Data Analysis (EDA):** Understand data structure, detect missing values, and summarize statistics.
- **2. Data Preprocessing:** Encode categorical variables into numerical values and scale features.
- **3. Data Visualization:** Visualize relationships between features and price using distribution plots and correlation heatmaps.
- **4. Model Building:** Train and evaluate regression models including Linear Regression (final model) and Random Forest Regression.
- **5. Prediction Interface:** Functions to encode inputs, scale features, and predict house prices based on user input.

---

## Installation and Usage

### Prerequisites

- Python 3.6+
- Jupyter Notebook (optional for exploration)
- Required Python libraries:
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - seaborn
  - joblib (for model serialization)
