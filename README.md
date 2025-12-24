# Tourism Prediction - Indonesia

Sistem Prediksi Cluster Wisata Indonesia menggunakan Machine Learning (K-Means Clustering)

## 📁 Struktur Project

```
├── templates/
│   └── index.html
├── app.py
├── kmeans_model.pkl
├── Procfile
├── README.md
└── requirements.txt
```

## 🚀 Cara Deploy ke Heroku

1. Login Heroku CLI
```bash
heroku login
```

2. Buat app baru
```bash
heroku create nama-app
```

3. Set remote heroku
```bash
heroku git:remote -a nama-app
```

4. Deploy
```bash
git add .
git commit -m "deployment"
git push heroku master
```

## 🛠️ Tech Stack
- Python Flask
- Scikit-learn (K-Means)
- Pandas, Numpy
- Gunicorn

## 📊 Dataset
- 437 Destinasi Wisata Indonesia
- 5 Kota: Jakarta, Yogyakarta, Bandung, Semarang, Surabaya
- 6 Kategori: Budaya, Taman Hiburan, Bahari, Cagar Alam, Pusat Perbelanjaan, Tempat Ibadah

## 👨‍💻 Author
EAS Penambangan Data - Semester 5
