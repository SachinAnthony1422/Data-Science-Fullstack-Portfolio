from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# 1. Load Data & Model
model_pipeline = joblib.load('models/segmentation_pipeline.pkl')
df = pd.read_csv("data/bank_customers_labeled.csv")

# 2. Helper function to get distribution data
def get_distribution(column_name):
    return df[column_name].value_counts().to_dict()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/dashboard-data')
def get_dashboard_data():
    # 1. Cluster Summary
    cluster_stats = df.groupby('Cluster').agg({
        'Age': 'mean',
        'Balance': 'mean',
        'Customer ID': 'count'
    }).reset_index().to_dict(orient='records')
    
    # 2. Demographics
    gender_dist = get_distribution('Gender')
    region_dist = get_distribution('Province')
    job_dist = get_distribution('Job Classification')
    
    # 3. Total Stats
    total_customers = len(df)
    avg_balance = df['Balance'].mean()
    
    return jsonify({
        'clusters': cluster_stats,
        'gender': gender_dist,
        'region': region_dist,
        'jobs': job_dist,
        'kpi': {
            'total_customers': total_customers,
            'avg_balance': round(avg_balance, 2)
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([{
            'Age': float(data['Age']),
            'Balance': float(data['Balance'])
        }])
        
        cluster = int(model_pipeline.predict(input_df)[0])
        
        # Personas based on the analysis
        personas = {
            0: "Sensible Saver (Mid-Balance)",
            1: "Wealthy Elite (High-Balance)",
            2: "Young Starter (Low-Balance)",
            3: "Mid-Life Spender (Average)"
        }
        
        return jsonify({
            'cluster': cluster,
            'persona': personas.get(cluster, "Unknown Segment")
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5002)