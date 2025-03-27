from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import DisasterClassifier
from twilio_alert import send_sos
import logging

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load model and vectorizer
model_path = "../models/disaster_classifier_model.pkl"
vectorizer_path = "../models/tfidf_vectorizer.pkl"
classifier = DisasterClassifier(model_path, vectorizer_path)

@app.route("/classify", methods=["POST", "OPTIONS"])
def classify_text():
    if request.method == "OPTIONS":
        logging.debug("CORS preflight request received for /classify")
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.get_json(force=True, silent=True)
    
    if not data or "text" not in data:
        logging.error("Missing 'text' field in request")
        return jsonify({"error": "Missing 'text' field"}), 400

    prediction = classifier.predict([data["text"]])
    logging.info(f"Prediction result: {prediction[0]} for input: {data['text']}")

    return jsonify({"prediction": int(prediction[0])})

@app.route("/send_sos", methods=["POST", "OPTIONS"])
def send_sos_alert():
    if request.method == "OPTIONS":
        logging.debug("CORS preflight request received for /send_sos")
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.get_json(force=True, silent=True)
    
    if not data:
        logging.error("Missing JSON data in request")
        return jsonify({"error": "Missing JSON data"}), 400

    message = data.get("message", "SOS! Emergency alert.")
    recipient = data.get("recipient")

    if not recipient:
        logging.error("Recipient phone number is required")
        return jsonify({"error": "Recipient phone number is required"}), 400

    logging.info(f"Sending SOS alert to {recipient} with message: {message}")
    response = send_sos(message, recipient)
    logging.info(f"SOS response: {response}")

    return jsonify(response)

if __name__ == "__main__":
    logging.info("Starting Flask server...")
    app.run(debug=True)
