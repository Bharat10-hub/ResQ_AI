import pandas as pd
import nltk
import re
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean_text(text):
    if isinstance(text, str):  # Ensure text is a string before processing
        text = text.lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
        tokens = text.split()
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    return ""  # Return empty string if text is NaN

def load_and_preprocess(input_path, output_path):
    df = pd.read_csv(input_path)

    if "text" not in df.columns or "target" not in df.columns:
        print("❌ Error: 'text' or 'target' column is missing!")
        return
    
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    df[['cleaned_text', 'target']].to_csv(output_path, index=False)
    print(f"✅ Processed data saved to {output_path}")

# Run preprocessing
load_and_preprocess("../data/train.csv", "../data/processed_data.csv")