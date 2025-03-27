import joblib

class DisasterClassifier:
    def __init__(self, model_path, vectorizer_path):
        try:
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            print("✅ Model Loaded Successfully!")
        except Exception as e:
            print(f"❌ Error Loading Model: {str(e)}")

    def predict(self, text_list):
        text_vectors = self.vectorizer.transform(text_list)
        return self.model.predict(text_vectors)
