from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# 1. Load the Full Pipeline (Includes Preprocessing + Model)
print("Loading production pipeline...")
pipeline = joblib.load('models/churn_pipeline.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from frontend
        data = request.get_json()
        
        # Convert to DataFrame
        # The pipeline expects a DataFrame with the original column names
        input_df = pd.DataFrame([data])
        
        # Ensure numeric types for specific columns (API receives strings mostly)
        # The pipeline handles scaling/missing values, but basic type conversion helps
        for col in ['tenure', 'MonthlyCharges', 'TotalCharges']:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce')

        # Predict
        prediction = pipeline.predict(input_df)[0]
        probability = pipeline.predict_proba(input_df)[0][1]
        
        result = "Yes" if prediction == 1 else "No"
        
        return jsonify({
            'prediction': result,
            'probability': round(probability * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)