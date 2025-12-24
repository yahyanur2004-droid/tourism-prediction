import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page config
st.set_page_config(
    page_title="Sistem Prediksi Wisata Indonesia",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS untuk tampilan seperti index.html
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f64f59 100%);
        padding: 60px 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .hero-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    
    /* Stats Cards in Hero */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 25px;
    }
    
    .stat-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 20px 30px;
        border-radius: 15px;
        text-align: center;
        min-width: 120px;
    }
    
    .stat-number {
        display: block;
        font-size: 2rem;
        font-weight: 700;
        color: white;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.85rem;
    }
    
    /* Team Section */
    .team-section {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 20px 30px;
        border-radius: 15px;
        max-width: 500px;
        margin: 0 auto;
    }
    
    .team-title {
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .team-list {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        text-align: left;
        padding-left: 20px;
    }
    
    /* Section Title */
    .section-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin: 30px 0 20px;
    }
    
    /* Form Card */
    .form-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* Result Cards */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    
    .result-title {
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 10px;
        opacity: 0.9;
    }
    
    .result-value {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    /* Recommendation Card */
    .rec-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .rec-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    .rec-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 5px;
    }
    
    .rec-category {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        display: inline-block;
        margin-right: 8px;
    }
    
    .rec-city {
        background: #f0f0f0;
        color: #666;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        display: inline-block;
    }
    
    .rec-details {
        display: flex;
        justify-content: space-between;
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid #eee;
    }
    
    .rec-price {
        color: #667eea;
        font-weight: 600;
    }
    
    .rec-rating {
        color: #f5a623;
        font-weight: 600;
    }
    
    /* Analysis Card */
    .analysis-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #e0e0e0;
    }
    
    .analysis-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }
    
    /* Custom Button */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Custom Select/Input */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }
    
    /* Cluster Badge */
    .cluster-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .cluster-0 { background: #ff6b6b; color: white; }
    .cluster-1 { background: #ffd93d; color: #333; }
    .cluster-2 { background: #6bcb77; color: white; }
    .cluster-3 { background: #4d96ff; color: white; }
</style>
""", unsafe_allow_html=True)

# Load model dan data
@st.cache_resource
def load_model():
    with open('kmeans_model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def load_data():
    return pd.read_csv('tourism_cleaned.csv')

@st.cache_data  
def load_original_data():
    return pd.read_csv('tourism_with_id.csv')

kmeans_model = load_model()
df = load_data()
df_original = load_original_data()

# Hitung min/max dari data asli untuk normalisasi
PRICE_MAX = df_original['Price'].max()
RATING_MIN = df_original['Rating'].min()
RATING_MAX = df_original['Rating'].max()
TIME_MIN = df_original['Time_Minutes'].min()
TIME_MAX = df_original['Time_Minutes'].max()
LAT_MIN = df_original['Lat'].min()
LAT_MAX = df_original['Lat'].max()
LONG_MIN = df_original['Long'].min()
LONG_MAX = df_original['Long'].max()

# Cluster descriptions
cluster_info = {
    0: {"name": "Wisata Premium", "desc": "Harga tinggi dengan rating sangat baik", "color": "#ff6b6b"},
    1: {"name": "Wisata Menengah", "desc": "Harga moderate dengan rating baik", "color": "#ffd93d"}, 
    2: {"name": "Wisata Ekonomis", "desc": "Harga terjangkau dengan rating baik", "color": "#6bcb77"},
    3: {"name": "Wisata Gratis/Murah", "desc": "Harga rendah dengan rating bervariasi", "color": "#4d96ff"}
}

# ===== HERO SECTION =====
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">🔮 Sistem Prediksi Wisata Indonesia</div>
    <div class="hero-subtitle">Prediksi Cluster & Rekomendasi Destinasi menggunakan Machine Learning (K-Means Clustering)</div>
    
    <div class="stats-container">
        <div class="stat-card">
            <span class="stat-number">{len(df)}</span>
            <span class="stat-label">Data Wisata</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">4</span>
            <span class="stat-label">Cluster</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">{df['City'].nunique()}</span>
            <span class="stat-label">Kota</span>
        </div>
        <div class="stat-card">
            <span class="stat-number">{df['Category'].nunique()}</span>
            <span class="stat-label">Kategori</span>
        </div>
    </div>
    
    <div class="team-section">
        <div class="team-title">👨‍💻 Oleh : Kelompok 4</div>
        <ol class="team-list">
            <li>Alfian Dimas Maulana (1462300019)</li>
            <li>Zidan Alfarizan Nugraha (1462300029)</li>
            <li>Raniah Aurellia Putri (1462300040)</li>
            <li>Yahya Nur Nasywa H (1462300067)</li>
            <li>Fajar Rizky Fathoni (1462300099)</li>
        </ol>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== PREDICTION SECTION =====
st.markdown('<div class="section-title">🎯 Silahkan Masukkan Data Anda</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    city = st.selectbox("🏙️ Kota Tujuan Wisata:", ["Jakarta", "Yogyakarta", "Bandung", "Semarang", "Surabaya"])
    
    category = st.selectbox("🎭 Kategori Wisata yang Diminati:", 
                           df['Category'].unique().tolist())
    
    budget_options = {
        "Gratis (Rp 0)": 0,
        "Dibawah Rp 10.000": 10000,
        "Dibawah Rp 25.000": 25000,
        "Dibawah Rp 50.000": 50000,
        "Dibawah Rp 100.000": 100000,
        "Dibawah Rp 200.000": 200000,
        "Dibawah Rp 500.000": 500000,
        "Semua Harga": int(PRICE_MAX)
    }
    budget_choice = st.selectbox("💰 Budget Maksimal:", list(budget_options.keys()), index=4)
    price = budget_options[budget_choice]
    
    rating_options = {
        "≥ 4.0 (Baik)": 4.0,
        "≥ 4.3 (Bagus)": 4.3,
        "≥ 4.5 (Sangat Bagus)": 4.5,
        "≥ 4.7 (Excellent)": 4.7
    }
    rating_choice = st.selectbox("⭐ Ekspektasi Rating Minimal:", list(rating_options.keys()), index=2)
    rating = rating_options[rating_choice]
    
    time_options = {
        "Tidak Ada Preferensi": 180,
        "≤ 1 jam": 60,
        "≤ 2 jam": 120,
        "≤ 3 jam": 180,
        "≤ 6 jam": 360
    }
    time_choice = st.selectbox("⏱️ Waktu Kunjungan yang Diinginkan:", list(time_options.keys()))
    time_minutes = time_options[time_choice]
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    predict_btn = st.button("🔮 Jalankan Prediksi & Rekomendasi", use_container_width=True)

# City coordinates
city_coords = {
    "Jakarta": (-6.2, 106.8),
    "Yogyakarta": (-7.8, 110.4),
    "Bandung": (-6.9, 107.6),
    "Semarang": (-7.0, 110.4),
    "Surabaya": (-7.25, 112.75)
}
lat, long = city_coords[city]

with col2:
    if predict_btn:
        # Normalisasi
        price_norm = price / PRICE_MAX if PRICE_MAX > 0 else 0
        rating_norm = (rating - RATING_MIN) / (RATING_MAX - RATING_MIN) if (RATING_MAX - RATING_MIN) > 0 else 0
        time_norm = (time_minutes - TIME_MIN) / (TIME_MAX - TIME_MIN) if (TIME_MAX - TIME_MIN) > 0 else 0
        lat_norm = (lat - LAT_MIN) / (LAT_MAX - LAT_MIN) if (LAT_MAX - LAT_MIN) > 0 else 0
        long_norm = (long - LONG_MIN) / (LONG_MAX - LONG_MIN) if (LONG_MAX - LONG_MIN) > 0 else 0
        
        # Predict
        features = np.array([[price_norm, rating_norm, time_norm, lat_norm, long_norm]])
        cluster = kmeans_model.predict(features)[0]
        
        cluster_data = cluster_info.get(cluster, {"name": "Unknown", "desc": "", "color": "#999"})
        
        # Results
        st.markdown('<div class="section-title">📊 Hasil Prediksi & Analisis</div>', unsafe_allow_html=True)
        
        # Result cards
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">🎯 Cluster Prediksi</div>
                <div class="result-value">Cluster {cluster}</div>
                <div style="margin-top: 10px; font-size: 0.9rem;">{cluster_data['name']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with r2:
            # Hitung rata-rata rating cluster
            cluster_avg_rating = df[df['Cluster'] == cluster]['Rating'].mean()
            display_rating = cluster_avg_rating * (RATING_MAX - RATING_MIN) + RATING_MIN
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">⭐ Rata-rata Rating Cluster</div>
                <div class="result-value">{display_rating:.2f}</div>
                <div style="margin-top: 10px; font-size: 0.9rem;">{cluster_data['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recommendations
        st.markdown('<div class="section-title">🎁 Rekomendasi Destinasi Wisata</div>', unsafe_allow_html=True)
        
        # Filter by cluster, city, category, and budget
        recommendations = df[
            (df['Cluster'] == cluster) & 
            (df['City'] == city) &
            (df['Category'] == category)
        ].head(5)
        
        # If no match with all filters, relax filters
        if len(recommendations) == 0:
            recommendations = df[
                (df['Cluster'] == cluster) & 
                (df['City'] == city)
            ].head(5)
        
        if len(recommendations) == 0:
            recommendations = df[df['Cluster'] == cluster].head(5)
        
        for _, place in recommendations.iterrows():
            original_price = place['Price'] * PRICE_MAX
            original_rating = place['Rating'] * (RATING_MAX - RATING_MIN) + RATING_MIN
            
            st.markdown(f"""
            <div class="rec-card">
                <div class="rec-name">{place['Place_Name']}</div>
                <div>
                    <span class="rec-category">{place['Category']}</span>
                    <span class="rec-city">📍 {place['City']}</span>
                </div>
                <div class="rec-details">
                    <span class="rec-price">💰 Rp {original_price:,.0f}</span>
                    <span class="rec-rating">⭐ {original_rating:.1f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="form-card" style="text-align: center; padding: 60px;">
            <div style="font-size: 4rem; margin-bottom: 20px;">🔮</div>
            <div style="font-size: 1.2rem; color: #667eea; font-weight: 600;">Hasil Prediksi akan muncul di sini</div>
            <div style="color: #888; margin-top: 10px;">Silahkan isi form di sebelah kiri dan klik tombol Prediksi</div>
        </div>
        """, unsafe_allow_html=True)

# ===== ANALYSIS SECTION =====
st.markdown('<div class="section-title">📊 Analisis Dataset</div>', unsafe_allow_html=True)

a1, a2 = st.columns(2)

with a1:
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.markdown('<div class="analysis-title">📈 Statistik per Kategori</div>', unsafe_allow_html=True)
    
    cat_stats = df_original.groupby('Category').agg({
        'Place_Name': 'count',
        'Rating': 'mean',
        'Price': 'mean'
    }).reset_index()
    cat_stats.columns = ['Kategori', 'Jumlah', 'Avg Rating', 'Avg Harga']
    cat_stats['Avg Harga'] = cat_stats['Avg Harga'].apply(lambda x: f"Rp {x:,.0f}")
    cat_stats['Avg Rating'] = cat_stats['Avg Rating'].apply(lambda x: f"{x:.2f}")
    st.dataframe(cat_stats, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

with a2:
    st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
    st.markdown('<div class="analysis-title">🏙️ Statistik per Kota</div>', unsafe_allow_html=True)
    
    city_stats = df_original.groupby('City').agg({
        'Place_Name': 'count',
        'Rating': 'mean',
        'Price': 'mean'
    }).reset_index()
    city_stats.columns = ['Kota', 'Jumlah', 'Avg Rating', 'Avg Harga']
    city_stats['Avg Harga'] = city_stats['Avg Harga'].apply(lambda x: f"Rp {x:,.0f}")
    city_stats['Avg Rating'] = city_stats['Avg Rating'].apply(lambda x: f"{x:.2f}")
    st.dataframe(city_stats, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Cluster Statistics
st.markdown('<div class="section-title">🎯 Statistik Cluster</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
cluster_cols = [c1, c2, c3, c4]

for i, col in enumerate(cluster_cols):
    cluster_df = df[df['Cluster'] == i]
    count = len(cluster_df)
    avg_price = cluster_df['Price'].mean() * PRICE_MAX
    avg_rating = cluster_df['Rating'].mean() * (RATING_MAX - RATING_MIN) + RATING_MIN
    
    with col:
        st.markdown(f"""
        <div class="result-card" style="background: {cluster_info[i]['color']};">
            <div class="result-title">Cluster {i}</div>
            <div class="result-value">{count}</div>
            <div style="font-size: 0.85rem; margin-top: 10px;">
                {cluster_info[i]['name']}<br>
                Avg: Rp {avg_price:,.0f}<br>
                ⭐ {avg_rating:.2f}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ===== DATA SECTION =====
st.markdown('<div class="section-title">📁 Data Wisata</div>', unsafe_allow_html=True)

st.markdown('<div class="analysis-card">', unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3 = st.columns(3)
with filter_col1:
    filter_city = st.selectbox("Filter Kota:", ["Semua"] + df_original['City'].unique().tolist(), key="filter_city")
with filter_col2:
    filter_cat = st.selectbox("Filter Kategori:", ["Semua"] + df_original['Category'].unique().tolist(), key="filter_cat")
with filter_col3:
    filter_cluster = st.selectbox("Filter Cluster:", ["Semua", 0, 1, 2, 3], key="filter_cluster")

display_df = df_original.copy()
if filter_city != "Semua":
    display_df = display_df[display_df['City'] == filter_city]
if filter_cat != "Semua":
    display_df = display_df[display_df['Category'] == filter_cat]

# Add cluster info from cleaned df
display_df = display_df.merge(df[['Place_Id', 'Cluster']], on='Place_Id', how='left')

if filter_cluster != "Semua":
    display_df = display_df[display_df['Cluster'] == filter_cluster]

st.dataframe(
    display_df[['Place_Name', 'Category', 'City', 'Price', 'Rating', 'Cluster']].head(50),
    use_container_width=True,
    hide_index=True
)

st.markdown(f"*Menampilkan {min(50, len(display_df))} dari {len(display_df)} data*", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 40px; color: #888; margin-top: 40px;">
    <p>🔮 Tourism Prediction System - Kelompok 4</p>
    <p style="font-size: 0.8rem;">Powered by Machine Learning (K-Means Clustering) & Streamlit</p>
</div>
""", unsafe_allow_html=True)
