# Project Conclusion: Fake News Detection with NLP

## 1. Project Overview
**Objective:** To develop a machine learning model capable of performing binary classification to distinguish between **FAKE** and **REAL** news articles.
**Dataset:** Utilized the "Fake or Real News" dataset, containing approximately 6,335 labeled records.

## 2. Data Preprocessing Pipeline
To prepare raw text for modeling, a standard NLP pipeline was implemented:
* **Text Cleaning:** Removal of URLs, punctuation, and non-alphanumeric characters using Regex.
* **Normalization:** Converted text to lowercase and removed English stopwords via NLTK.
* **Lemmatization:** Reduced words to their base roots (e.g., "running" $\rightarrow$ "run") using `WordNetLemmatizer`.
* **Feature Extraction:** Converted text into numerical vectors using **TF-IDF** (Term Frequency-Inverse Document Frequency). The vectorizer included both unigrams and bigrams (`ngram_range=(1,2)`) to capture contextual word pairings.

## 3. Model Performance Comparison
Three supervised learning algorithms were trained and evaluated on a 30% test set.

| Model | Accuracy | Key Observation |
| :--- | :--- | :--- |
| **Multinomial Naive Bayes** | 82.80% | Baseline performance. High recall for "FAKE" news but lower precision compared to other models. |
| **Logistic Regression** | 91.43% | Significant improvement with balanced Precision and Recall scores (~0.91) for both classes. |
| **Linear SVC** | **94.16%** | **Best Performer.** Achieved the highest accuracy and a balanced F1-score of 0.94. |

## 4. Final Outcome
* **Winning Model:** The **Linear Support Vector Classifier (LinearSVC)** was selected as the final model due to its ability to handle high-dimensional sparse data efficiently.
* **Deployment:** The model was serialized and saved as `Fake_news_classification.pkl`.
* **Inference:** The model was tested on a complex, unseen news snippet regarding court proceedings and political figures; it successfully predicted the label as **'REAL'**, demonstrating good generalization.

## 5. Recommendations for Future Work
* **Deep Learning:** Experiment with Transformer models (like BERT or RoBERTa) to capture deeper semantic meaning.
* **Explainability:** Integrate tools like LIME or SHAP to visualize which specific words contribute most to a "Fake" or "Real" classification.
