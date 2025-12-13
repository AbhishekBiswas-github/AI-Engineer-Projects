
# Global Earthquake-Tsunami Risk Assessment using Deep Learning

This project implements an end-to-end deep learning pipeline to predict the risk of a tsunami following an earthquake. The model is built using TensorFlow and Keras and is divided into three main components: data preprocessing, model training, and prediction.

---

## 📋 Table of Contents
* [Project Overview](#project-overview)
* [Dataset](#dataset)
* [Project Structure](#project-structure)
* [Methodology](#methodology)
* [Technologies Used](#technologies-used)
* [How to Use](#how-to-use)
* [Results](#results)

---

## 🚀 Project Overview

The goal of this project is to develop a reliable neural network model that can classify whether an earthquake will generate a tsunami based on various seismic features. The final application allows a user to input data for a new earthquake event and receive a tsunami risk prediction.

---

## 💾 Dataset

The dataset used for this project is sourced from a public CSV file containing global earthquake and tsunami data. The preprocessing script (`Global Earthquake Tsunami Risk - Data Preprocessing.ipynb`) loads this data directly.

**Source:** [earthquake_data_tsunami.csv](https://raw.githubusercontent.com/AbhishekBiswas-github/Python_Data_Science/refs/heads/main/Global%20Earthquake-Tsunami%20Risk%20Assessment/earthquake_data_tsunami.csv)

---

## 📂 Project Structure

The repository is organized into three Jupyter notebooks, each handling a specific part of the machine learning pipeline:

1.  **`Global Earthquake Tsunami Risk - Data Preprocessing.ipynb`**: This notebook is responsible for loading the raw data, cleaning it, balancing the target classes, scaling the features, and splitting the dataset into training, validation, and test sets. The processed data is saved into `.npz` files.
2.  **`Global Earthquake Tsunami Risk - Modelling.ipynb`**: This notebook loads the preprocessed data, defines the neural network architecture, compiles and trains the model, and evaluates its performance. The final trained model is saved as `Earthquake.keras`.
3.  **`Global Earthquake Tsunami Risk - Prediction.ipynb`**: This script loads the saved `.keras` model and provides a simple command-line interface for users to input new earthquake data and get a tsunami risk prediction.

---

## 🛠️ Methodology

### 1. Data Preprocessing
* **Data Loading**: The dataset is loaded from the source URL using **Pandas**.
