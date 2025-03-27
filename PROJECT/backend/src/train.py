import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Define file paths
data_path = "../data/processed_data.csv"
model_path = "../models/disaster_classifier_model.pkl"
vectorizer_path = "../models/tfidf_vectorizer.pkl"

# Load the processed data
df = pd.read_csv(data_path)

# Ensure necessary columns exist
if "cleaned_text" not in df.columns or "target" not in df.columns:
    raise ValueError("Error: 'cleaned_text' or 'target' column is missing!")

# Splitting the dataset
X_train, X_test, y_train, y_test = train_test_split(df['cleaned_text'], df["target"], test_size=0.2, random_state=42)

# Vectorizing the text data
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Evaluate model
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.4f}")

# Ensure models folder exists
os.makedirs("../models", exist_ok=True)

# Save model and vectorizer
joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)
print(f"✅ Model and vectorizer saved successfully in {model_path} and {vectorizer_path}!")

