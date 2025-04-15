# ---- Save this code as model_api.py ----

import numpy as np
from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
# Optional, but good practice for saving/loading trained models:
# import joblib

# --- 1. Model Training (Done once when the script starts) ---

# Load the Iris dataset
iris = load_iris()
X = iris.data  # Features: Sepal length, Sepal width, Petal length, Petal width
y = iris.target  # Target: Species index (0, 1, 2)
target_names = iris.target_names # Species names: ['setosa', 'versicolor', 'virginica']

# Initialize and train a Decision Tree Classifier
# Using a fixed random_state for reproducibility
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

print("--- Iris Decision Tree Model Trained ---")
print(f"Features: {iris.feature_names}")
print(f"Target names: {list(target_names)}")
# Optional: Save the trained model to a file
# joblib.dump(model, 'iris_decision_tree.joblib')
# Optional: Later, load the model instead of training each time
# model = joblib.load('iris_decision_tree.joblib')


# --- 2. Flask API Setup ---

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Simple home page message
    return "<h1>Iris Prediction API</h1><p>Use the /predict endpoint with POST method.</p>"


@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives flower features via JSON POST request and returns prediction.
    Expected JSON format:
    {
        "features": [sepal_length, sepal_width, petal_length, petal_width]
        // Example: "features": [5.1, 3.5, 1.4, 0.2] (should predict setosa)
    }
    """
    # Check if request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    # Get data from JSON payload
    data = request.get_json()

    # Validate input data presence and format
    if 'features' not in data:
        return jsonify({"error": "Missing 'features' key in JSON data"}), 400

    features = data['features']
    if not isinstance(features, list) or len(features) != 4:
        return jsonify({"error": "'features' must be a list of exactly 4 numbers."}), 400

    try:
        # Convert features to numpy array and reshape for single prediction
        # The model expects a 2D array [[feat1, feat2, feat3, feat4]]
        features_array = np.array(features).reshape(1, -1)

        # --- 3. Make Prediction ---
        prediction_index = model.predict(features_array)[0]
        predicted_species = target_names[prediction_index]

        # --- 4. Return Response ---
        return jsonify({
            "input_features": features,
            "predicted_species_index": int(prediction_index), # Convert numpy int to standard int
            "predicted_species_name": predicted_species
        })

    except ValueError as ve:
        # Handle cases where conversion to numpy array fails (e.g., non-numeric input)
        return jsonify({"error": f"Invalid feature data: {ve}. Features must be numbers."}), 400
    except Exception as e:
        # Catch-all for any other unexpected errors during prediction
        # Log the error server-side for debugging
        app.logger.error(f"Prediction error: {e}")
        return jsonify({"error": "An internal error occurred during prediction."}), 500


# --- 5. Run the Flask App ---
if __name__ == '__main__':
    # Use a different port (e.g., 5001) to avoid conflict if Part 1 app is running
    app.run(debug=True, port=5001)