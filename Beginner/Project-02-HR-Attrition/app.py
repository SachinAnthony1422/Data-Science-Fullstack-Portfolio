from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# 1. Load the Senior Pipeline
print("Loading HR Model Pipeline...")
pipeline = joblib.load('models/attrition_pipeline.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from frontend
        data = request.get_json()
        
        # Convert to DataFrame (The pipeline expects named columns)
        input_df = pd.DataFrame([data])
        
        # Ensure numeric types where necessary
        numeric_cols = ['Age', 'DailyRate', 'DistanceFromHome', 'HourlyRate', 
                        'MonthlyIncome', 'MonthlyRate', 'NumCompaniesWorked', 
                        'PercentSalaryHike', 'TotalWorkingYears', 
                        'TrainingTimesLastYear', 'YearsAtCompany', 
                        'YearsInCurrentRole', 'YearsSinceLastPromotion', 
                        'YearsWithCurrManager']
        
        for col in numeric_cols:
            if col in input_df.columns:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')

        # Predict
        prediction = pipeline.predict(input_df)[0] # 0 or 1
        probability = pipeline.predict_proba(input_df)[0][1] # Probability of Class 1 (Yes)
        
        result = "Yes" if prediction == 1 else "No"
        
        return jsonify({
            'prediction': result,
            'probability': round(probability * 100, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Running on port 5001 to avoid conflict with Project 1