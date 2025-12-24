import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page config
st.set_page_config(
    page_title="Tourism Prediction - Indonesia",
    page_icon="🏝️",
    layout="wide"
)

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

# Hitung min/max dari data asli untuk normalisasi yang benar
PRICE_MAX = df_original['Price'].max()  # ~900000
RATING_MIN = df_original['Rating'].min()  # ~3.4
RATING_MAX = df_original['Rating'].max()  # ~5.0
TIME_MIN = df_original['Time_Minutes'].min()  # ~10
TIME_MAX = df_original['Time_Minutes'].max()  # ~360
LAT_MIN = df_original['Lat'].min()
LAT_MAX = df_original['Lat'].max()
LONG_MIN = df_original['Long'].min()
LONG_MAX = df_original['Long'].max()

# Cluster descriptions
cluster_descriptions = {
    0: "🔴 Wisata Premium - Harga tinggi dengan rating sangat baik",
    1: "🟡 Wisata Menengah - Harga moderate dengan rating baik", 
    2: "🟢 Wisata Ekonomis - Harga terjangkau dengan rating baik",
    3: "🔵 Wisata Gratis/Murah - Harga rendah dengan rating bervariasi"
}

# Header
st.title("🏝️ Tourism Prediction System")
st.markdown("### Prediksi Cluster Wisata Indonesia dengan Machine Learning")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Dataset Info")
    st.metric("Total Data", len(df))
    st.metric("Jumlah Cluster", 4)
    st.metric("Jumlah Kota", df['City'].nunique())
    st.metric("Jumlah Kategori", df['Category'].nunique())

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🎯 Input Data Wisata")
    
    price = st.number_input("💰 Harga Tiket (Rp)", min_value=0, max_value=int(PRICE_MAX), value=25000, step=5000)
    rating = st.slider("⭐ Rating", min_value=float(RATING_MIN), max_value=float(RATING_MAX), value=4.5, step=0.1)
    time_minutes = st.slider("⏱️ Waktu Kunjungan (menit)", min_value=int(TIME_MIN), max_value=int(TIME_MAX), value=60)
    
    city = st.selectbox("🏙️ Kota", ["Jakarta", "Yogyakarta", "Bandung", "Semarang", "Surabaya"])
    
    # City coordinates
    city_coords = {
        "Jakarta": (-6.2, 106.8),
        "Yogyakarta": (-7.8, 110.4),
        "Bandung": (-6.9, 107.6),
        "Semarang": (-7.0, 110.4),
        "Surabaya": (-7.25, 112.75)
    }
    lat, long = city_coords[city]
    
    st.info(f"📍 Koordinat: Lat {lat}, Long {long}")
    
    predict_btn = st.button("🔮 Prediksi Cluster", type="primary", use_container_width=True)

with col2:
    st.header("📊 Hasil Prediksi")
    
    if predict_btn:
        # Normalisasi sesuai dengan cara training model (MinMaxScaler)
        price_norm = price / PRICE_MAX if PRICE_MAX > 0 else 0
        rating_norm = (rating - RATING_MIN) / (RATING_MAX - RATING_MIN) if (RATING_MAX - RATING_MIN) > 0 else 0
        time_norm = (time_minutes - TIME_MIN) / (TIME_MAX - TIME_MIN) if (TIME_MAX - TIME_MIN) > 0 else 0
        lat_norm = (lat - LAT_MIN) / (LAT_MAX - LAT_MIN) if (LAT_MAX - LAT_MIN) > 0 else 0
        long_norm = (long - LONG_MIN) / (LONG_MAX - LONG_MIN) if (LONG_MAX - LONG_MIN) > 0 else 0
        
        # Predict
        features = np.array([[price_norm, rating_norm, time_norm, lat_norm, long_norm]])
        cluster = kmeans_model.predict(features)[0]
        
        # Display debug info
        with st.expander("🔍 Debug - Nilai Normalisasi"):
            st.write(f"Price: {price} → {price_norm:.4f}")
            st.write(f"Rating: {rating} → {rating_norm:.4f}")
            st.write(f"Time: {time_minutes} → {time_norm:.4f}")
            st.write(f"Lat: {lat} → {lat_norm:.4f}")
            st.write(f"Long: {long} → {long_norm:.4f}")
        
        # Display result
        st.success(f"### Cluster: {cluster}")
        st.info(cluster_descriptions.get(cluster, "Unknown"))
        
        # Similar places
        st.subheader("🎁 Rekomendasi Wisata Serupa:")
        similar = df[df['Cluster'] == cluster][['Place_Name', 'Category', 'City', 'Price', 'Rating']].head(5)
        
        for _, place in similar.iterrows():
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{place['Place_Name']}**")
                    # Denormalisasi price untuk tampilan
                    original_price = place['Price'] * PRICE_MAX
                    st.caption(f"{place['Category']} • {place['City']} • Rp {original_price:,.0f}")
                with c2:
                    original_rating = place['Rating'] * (RATING_MAX - RATING_MIN) + RATING_MIN
                    st.markdown(f"⭐ **{original_rating:.1f}**")
                st.divider()
    else:
        st.info("👆 Masukkan data dan klik tombol **Prediksi Cluster**")

# Data Explorer
st.markdown("---")
st.header("📁 Eksplorasi Data")

tab1, tab2, tab3 = st.tabs(["📊 Statistik Cluster", "🗺️ Data Wisata", "📈 Visualisasi"])

with tab1:
    cluster_stats = df.groupby('Cluster').agg({
        'Place_Name': 'count',
        'Price': 'mean',
        'Rating': 'mean'
    }).reset_index()
    cluster_stats.columns = ['Cluster', 'Jumlah', 'Rata-rata Harga', 'Rata-rata Rating']
    st.dataframe(cluster_stats, use_container_width=True)

with tab2:
    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_city = st.selectbox("Filter Kota", ["Semua"] + df['City'].unique().tolist())
    with col_f2:
        filter_cat = st.selectbox("Filter Kategori", ["Semua"] + df['Category'].unique().tolist())
    
    filtered_df = df.copy()
    if filter_city != "Semua":
        filtered_df = filtered_df[filtered_df['City'] == filter_city]
    if filter_cat != "Semua":
        filtered_df = filtered_df[filtered_df['Category'] == filter_cat]
    
    st.dataframe(
        filtered_df[['Place_Name', 'Category', 'City', 'Price', 'Rating', 'Cluster']],
        use_container_width=True
    )

with tab3:
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Rating distribution
    df['Rating'].hist(ax=axes[0], bins=15, color='skyblue', edgecolor='black')
    axes[0].set_title('Distribusi Rating')
    axes[0].set_xlabel('Rating')
    
    # Cluster distribution
    df['Cluster'].value_counts().plot(kind='bar', ax=axes[1], color=['#e74c3c', '#f39c12', '#27ae60', '#3498db'])
    axes[1].set_title('Jumlah per Cluster')
    axes[1].set_xlabel('Cluster')
    
    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("🎓 **Penambangan Data - EAS Semester 5** | Model: K-Means Clustering")
