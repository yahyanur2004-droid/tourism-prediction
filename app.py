from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model dan data
with open('kmeans_model.pkl', 'rb') as f:
    kmeans_model = pickle.load(f)

# Load data untuk referensi
df = pd.read_csv('tourism_cleaned.csv')

# Cluster descriptions
cluster_descriptions = {
    0: "Wisata Premium - Harga tinggi dengan rating sangat baik",
    1: "Wisata Menengah - Harga moderate dengan rating baik", 
    2: "Wisata Ekonomis - Harga terjangkau dengan rating baik",
    3: "Wisata Gratis/Murah - Harga rendah dengan rating bervariasi"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from form
        price = float(request.form.get('price', 0))
        rating = float(request.form.get('rating', 4.5))
        time_minutes = float(request.form.get('time_minutes', 60))
        lat = float(request.form.get('lat', -6.9))
        long = float(request.form.get('long', 110.4))
        
        # Normalize input (same as training)
        price_norm = price / 900000  # max price
        rating_norm = (rating - 3.4) / (5.0 - 3.4)  # min-max
        time_norm = (time_minutes - 10) / (360 - 10)  # min-max
        lat_norm = (lat - (-8.197894)) / (1.078880 - (-8.197894))
        long_norm = (long - 103.931398) / (112.821662 - 103.931398)
        
        # Predict cluster
        features = np.array([[price_norm, rating_norm, time_norm, lat_norm, long_norm]])
        cluster = kmeans_model.predict(features)[0]
        
        # Get similar places from same cluster
        similar_places = df[df['Cluster'] == cluster][['Place_Name', 'Category', 'City', 'Price', 'Rating']].head(5).to_dict('records')
        
        result = {
            'cluster': int(cluster),
            'description': cluster_descriptions.get(cluster, "Unknown cluster"),
            'similar_places': similar_places
        }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/places')
def get_places():
    """Get all tourism places"""
    places = df[['Place_Name', 'Category', 'City', 'Price', 'Rating', 'Cluster']].to_dict('records')
    return jsonify(places)

@app.route('/api/clusters')
def get_clusters():
    """Get cluster statistics"""
    cluster_stats = df.groupby('Cluster').agg({
        'Place_Name': 'count',
        'Price': 'mean',
        'Rating': 'mean'
    }).reset_index()
    cluster_stats.columns = ['Cluster', 'Count', 'Avg_Price', 'Avg_Rating']
    return jsonify(cluster_stats.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)
