# 🧠 Student Mental Health State Prediction  

This project focuses on predicting the **mental health state of students** using deep learning techniques based on behavioral and lifestyle parameters. It leverages data-driven insights to identify mental health indicators, supporting awareness and early intervention in student well-being.  

---

## 🚀 Project Overview  

The goal of this project is to build a deep learning model that can predict the **mental health state** (e.g., healthy, stressed, at risk) of a student based on features such as:  

- Age & Gender  
- Platform usage type  
- Daily screen time (minutes)  
- Social media activity (minutes)  
- Negative and positive interactions  
- Sleep hours & physical activity time  
- Self-reported stress, mood, and anxiety levels  

The process includes **data preprocessing, model training, and prediction** through three main Python scripts.  

---

## 🔍 Project Structure  
Student-Mental-Health/
│
├── data_preprocessing.ipynb # Data cleaning, visualization, and tensor preparation
├── model_training.ipynb # Model creation and training pipeline
├── prediction.ipynb # Takes user input and predicts mental health state
└── README.md # Project documentation


---

## 🧩 Project Phases  

### Phase 1: Data Preprocessing  
- Loaded and explored the dataset using **Pandas**, **NumPy**, and **Seaborn**.  
- Visualized key relationships between parameters  
- Encoded categorical variables using **OrdinalEncoder**.  
- Normalized/selectively scaled numerical features for model readiness.  
- Split data into **training**, **validation**, and **test** sets.  
- Saved datasets in **Tensor** format for deep learning workflows.  

### Phase 2: Deep Learning Model  
- Implemented a **4-layer neural network** using **TensorFlow** and **Keras**.  
- Used **ReLU** activations for hidden layers and **Softmax** for output classification.  
- Applied **Adam optimizer** with categorical cross-entropy loss.  
- Trained the model and monitored accuracy and loss metrics on validation data.  
- Saved the trained model for use in downstream prediction.  

### Phase 3: Prediction System  
- Created an interactive prediction interface using Python input prompts.  
- User enters student parameters (age, sleep hours, stress level, etc.).  
- Model outputs one of the three possible mental health states (e.g., *Healthy*, *Stressed*, *At Risk*).  
- Useful for analyzing real-time data or conducting hypothetical scenario testing.  

---

## 🧠 Libraries and Dependencies  

Below are all the Python libraries and modules used throughout the project:  

`import pandas as pd`
`import numpy as np`
`import matplotlib.pyplot as plt`
`import seaborn as sns`
`from sklearn.preprocessing import OrdinalEncoder, scale`
`import warnings`
`import tensorflow as tf`
`from sklearn import preprocessing`
`from IPython.display import clear_output`


**Additional details:**  
- **Pandas & NumPy:** Data manipulation and numerical computing.  
- **Matplotlib & Seaborn:** Data visualization and insights.  
- **scikit-learn:** Encoding and scaling transformations.  
- **TensorFlow:** Deep learning model design, training, and inference.  
- **IPython.display:** Used for clearing outputs during iterative model training.  


---

## 💡 Key Insights  

- Balanced screen time, social interactions, and physical activity strongly correlate with positive mental health outcomes.  
- Excessive screen time and higher stress levels are significant indicators of adverse mental states.  
- The model demonstrates how **AI can contribute to well-being analysis** in educational contexts.  

---

## 🤝 Contributing  

Contributions, suggestions, and improvements are welcome!  
If you’d like to enhance the model or visualization pipeline, feel free to submit a pull request or open an issue.  

---

## 📫 Contact  

For questions or collaborations, connect on [LinkedIn]([https://linkedin.com](https://www.linkedin.com/in/abhishek-biswas-developer/)) or check out more of the projects on [GitHub]([https://github.com/yourusername](https://github.com/AbhishekBiswas-github)).  
