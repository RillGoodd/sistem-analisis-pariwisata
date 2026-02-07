# 🏖️ Sistem Analisis Pariwisata Indonesia

Aplikasi web modern untuk menganalisis, visualisasi, dan pemetaan data destinasi wisata Indonesia menggunakan Streamlit, Folium, dan Plotly.

## ✨ Fitur Utama

### 🏠 Dashboard
- **Data Preview**: Tampilkan 15 baris data pertama
- **Metrics Overview**: Total destinasi, provinsi, kota, rata-rata rating
- **Column Information**: Informasi tipe data dan struktur
- **Missing Values Analysis**: Deteksi data yang hilang
- **Load Sample Data**: Data contoh sudah tersedia siap pakai

### 🕷️ Web Scraping
- **URL Scraping**: Scrape data dari website apapun dengan deteksi otomatis
  - Support HTML tables
  - Support CSV files
  - Support JSON/div structures
- **File Upload**: Unggah file CSV atau Excel
- **Column Auto-Mapping**: Sistem otomatis mapping kolom ke format standar pariwisata
- **Data Cleaning**: Validasi dan pembersihan otomatis
- **CSV Export**: Export hasil dengan encoding Unicode

### 📊 Visualisasi Data (5 Tabs)
1. **📈 Overview**
   - Pie chart kategori destinasi
   - Histogram distribusi rating
   - Quick metrics

2. **👥 Demographics**
   - Bar chart destinasi per kategori
   - Bar chart destinasi per provinsi
   - Sunburst diagram persebaran

3. **🌍 Geographic**
   - Sunburst chart persebaran provinsi
   - Stacked bar kategori per provinsi
   - Cross-tabulation analysis

4. **📊 Detailed Analysis (5 modes)**
   - Distribution: Distribusi kolom categorical
   - Scatter Plot: Relasi 2 variabel numerik
   - Percentage: Pie chart dengan persentase
   - Trend: Analisis tren waktu
   - Box Plot: Visualisasi quartile

5. **📋 Correlation**
   - Correlation matrix heatmap
   - Numeric data analysis
   - Color-coded relationships

### 🗺️ GIS Mapping
- **Interactive Maps**: Peta interaktif dengan Folium
- **5 Map Styles**:
  - OpenStreetMap (default)
  - Satellite
  - Dark
  - Topo
  - Positron
- **Smart Filtering**:
  - Filter by Provinsi
  - Filter by Kategori
  - Real-time update
- **Custom Markers**:
  - Color-coded by kategori
  - Circle markers dengan popup detail
  - Coordinate validation
- **Zoom Control**: 2-15 levels
- **Coordinate Auto-Generation**: Sistem otomatis dari nama lokasi
- **Geographic Statistics**: Latitude/Longitude range, average rating

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone/Download Project**
```bash
cd sistem-analisis-pariwisata-FINAL
```

2. **Create Virtual Environment**
```bash
python -m venv .venv
```

3. **Activate Virtual Environment**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

4. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

Browser akan terbuka otomatis di: **http://localhost:8501**

## 📊 Data Format

### Required Columns (Recommended)
```csv
nama,provinsi,kota,kategori,rating,harga,deskripsi,latitude,longitude
```

### Column Descriptions
| Kolom | Type | Description |
|-------|------|-------------|
| nama | string | Nama destinasi wisata |
| provinsi | string | Provinsi Indonesia |
| kota | string | Kota/Kabupaten |
| kategori | string | Kategori destinasi (Pantai, Gunung, dll) |
| rating | float | Rating destinasi (0-5) |
| harga | int/float | Harga tiket masuk |
| deskripsi | string | Deskripsi destinasi |
| latitude | float | Koordinat latitude (-90 to 90) |
| longitude | float | Koordinat longitude (-180 to 180) |

### Auto-Mapping
Sistem akan otomatis mengenali dan map kolom dengan nama berbeda:
- `nama` → name, destinasi, tempat, lokasi, wisata, objek, attraction
- `provinsi` → province, state, region, daerah
- `kota` → city, kabupaten, kab/kota
- `kategori` → category, tipe, type, jenis
- `rating` → nilai, score, review
- `harga` → price, biaya, cost, tarif
- `deskripsi` → description, keterangan, detail

## 🕷️ Web Scraping Tips

### 🎯 Cara Mencari URL yang Cocok

**Kriteria URL yang cocok untuk scraping:**
1. **HTML Table Structure** - Halaman dengan tabel (`<table>` tags)
2. **Public Data** - Data yang dipublikasikan secara terbuka
3. **Friendly Robots.txt** - Website tidak melarang scraping
4. **Clean Data** - Format konsisten dan terstruktur

### 📌 Tips & Tricks

**Langkah-langkah mencari & test URL:**
1. **Identifikasi topik** - Cari website dengan data yang Anda ingin
2. **Inspect element** - Buka browser DevTools (F12)
3. **Cari `<table>`** - Lihat apakah ada tabel data terstruktur
4. **Copy URL** - Ambil halaman yang memiliki tabel
5. **Test kecil** - Paste URL ke app, set row limit 50, klik Scrape
6. **Jika sukses** - Increase row limit ke 500+ untuk lebih banyak data
7. **Backup** - Simpan hasil ke CSV untuk analisis

### Scraping Strategy (Multi-Layer Approach)
1. **Pandas read_html** - Extract tabel HTML secara langsung (paling efisien)
2. **BeautifulSoup Parsing** - Parse custom HTML structures
3. **Div/List Extraction** - Extract dari div containers jika table gagal
4. **Auto-Retry** - Otomatis retry dengan different strategies

### ✅ System Features
- **Auto Column Mapping** - Otomatis detect & map nama kolom
- **Auto Geocoding** - Generate koordinat dari nama lokasi/provinsi
- **Data Validation** - Validasi data sebelum visualisasi
- **Row Limit Control** - Kontrol jumlah data yang di-scrape

### ❌ HINDARI URLs ini:
- ❌ JavaScript-heavy websites (React, Vue, Angular)
- ❌ Halaman dengan infinite scroll/lazy loading
- ❌ PDF files atau format non-HTML
- ❌ Halaman yang memerlukan authentication/login
- ❌ Content yang di-render dinamis client-side
- ❌ Website yang explicit melarang scraping (robots.txt)

### 💡 Testing Guide
**Sebelum scrape, cek dulu:**
1. Buka halaman di browser
2. Scroll ke bawah → ada tabel?
3. Klik kanan → Inspect → cari `<table>` tag
4. Jika ada, kemungkinan besar scraping akan berhasil

**Row Limit Recommendations:**
- Pertama kali test: 50 rows
- Jika berhasil: coba 200 rows
- Jika masih OK: bisa 500+ rows
- Max processing: 3000 rows (tergantung ukuran file)

## 🗺️ GIS Mapping Features

### Coordinate Auto-Generation
Sistem otomatis generate koordinat dari nama lokasi:
- **City Level**: Jakarta, Bandung, Yogyakarta, Surabaya, dll (19 kota)
- **Province Level**: Semua 34 provinsi Indonesia
- **Worldwide Support**: Latitude/Longitude format untuk data apapun
- **Smart Fallback**: Jika tidak ada, use default koordinat

### Marker Color Coding
Setiap kategori destinasi memiliki warna unik di GIS Map:

```
PANTAI & LAUT:
├── Pantai → Blue (#0066CC)
├── Pulau → Yellow (#FFCC00)
├── Taman Laut → Dark Blue (#0033CC)

GUNUNG & ALAM:
├── Gunung → Red (#CC1111)
├── Taman Nasional → Magenta (#CC00CC)
├── Air Terjun → Cyan (#00FF99)
├── Danau → Light Cyan (#00CCFF)

BUDAYA & HIBURAN:
├── Candi → Orange (#FF6600)
├── Museum → Purple (#9933CC)
├── Desa Wisata → Green (#00CC00)
├── Taman Hiburan → Orange Yellow (#FF9900)

THERMAL & GEOLOGI:
├── Air Panas → Dark Red (#FF3333)
├── Goa → Brown (#996633)
```

### Performance & Features
- ✅ Optimized untuk 1000+ markers tanpa lag
- ✅ Rich popups dengan informasi lengkap (nama, kategori, rating, harga, koordinat)
- ✅ Hover tooltips untuk preview cepat
- ✅ Multi-filter support (provinsi & kategori)
- ✅ Responsive design untuk mobile & desktop
- ✅ Smooth zoom control (level 2-15)

## 📁 File Structure

```
sistem-analisis-pariwisata-FINAL/
├── app.py                      # Main Streamlit application
├── scraper.py                  # Web scraping module dengan auto-geocoding
├── requirements.txt            # Python dependencies
├── sample_data_complete.csv    # Sample tourism data (50 records Indonesia)
├── README.md                   # This file
├── run.bat                     # Quick run untuk Windows
├── run.sh                      # Quick run untuk Linux/Mac
└── __pycache__/                # Python cache files
```

## 🔧 Configuration

### Customize Map Style
Edit di `app.py` untuk mengubah style peta:
```python
map_style = st.selectbox(
    "🎨 Pilih Map Style",
    ["OpenStreetMap", "Satellite", "Dark", "Topo", "Positron"],
    index=0
)
```

### Adjust Zoom Level
Edit default zoom level:
```python
zoom = st.slider("🔍 Zoom Level", 2, 15, 5)  # default 5
```

### Add Custom Marker Colors
Edit color_map di `app.py`:
```python
color_map = {
    'Pantai': 'blue',
    'Gunung': 'red',
    # Add more categories...
}
```

## 📊 Sample Data

File `sample_data.csv` berisi 10 destinasi wisata populer Indonesia:
- Borobudur Temple (Jawa Tengah)
- Prambanan Temple (Yogyakarta)
- Kuta Beach (Bali)
- Ubud (Bali)
- Mount Bromo (Jawa Timur)
- Dan 5 destinasi lainnya

Gunakan untuk quick testing semua fitur.

## 🔄 Typical Workflow

### 1. Quick Test (5 minutes)
```
1. Run: streamlit run app.py
2. Dashboard → Load Sample Data
3. Visualisasi → View all 5 tabs
4. GIS Mapping → Explore map
```

### 2. Upload Own Data (10 minutes)
```
1. Go to Web Scraping → Upload File
2. Select CSV/Excel dengan data pariwisata
3. View column mapping results
4. Explore visualisasi dan GIS mapping
```

### 3. Scrape from Web (15-20 minutes)
```
1. Go to Web Scraping → Scrape dari URL
2. Enter URL dengan data tabel
3. Wait for scraping complete
4. Download CSV hasil
5. Upload ke aplikasi untuk analysis
```

## ⚠️ Troubleshooting

### Error: Module not found
```bash
pip install -r requirements.txt
```

### No coordinates showing on map
- Pastikan kolom 'latitude' dan 'longitude' ada
- Atau pastikan kolom 'provinsi' ada untuk auto-generate
- Check coordinate format: (-90 to 90 for latitude, -180 to 180 for longitude)

### Scraping can't find data
- Check URL is accessible
- View raw HTML to verify table structure
- Try different URL
- Some websites might block scraping

### Map not responding
- Check internet connection
- Clear browser cache
- Reduce number of markers (filter data)
- Try different map style

## 🛠️ Development

### Add New Feature
1. Edit `app.py` atau `scraper.py`
2. Test locally with: `streamlit run app.py`
3. Verify in all 4 pages

### Extend Scraper
Edit method di `scraper.py`:
- `scrape_from_url()` - Main scraping engine
- `map_columns()` - Add new column mappings
- `extract_coordinates()` - Add location databases

### Custom Styling
Edit CSS di `app.py`:
```python
st.markdown("""
<style>
    /* Custom CSS here */
</style>
""", unsafe_allow_html=True)
```

## 📈 Performance Metrics

| Operation | Time | Records |
|-----------|------|---------|
| Load sample data | <1s | 10 |
| Scrape from URL | 5-30s | 50-500 |
| Generate charts | 1-3s | 1000+ |
| GIS mapping | 2-5s | 1000+ |
| Filter & update | <1s | Any |

## 🎓 Learning Resources

### Streamlit
- https://docs.streamlit.io
- https://streamlit.io/gallery

### Folium (GIS)
- https://folium.readthedocs.io
- https://python-visualization.github.io/folium

### Plotly
- https://plotly.com/python
- https://plotly.com/python/basic-charts

### Web Scraping
- https://requests.readthedocs.io
- https://www.crummy.com/software/BeautifulSoup

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💼 Support

### Common Issues
1. **Streamlit not starting**: Clear cache with `streamlit cache clear`
2. **Unicode errors**: Ensure UTF-8 encoding
3. **Missing dependencies**: Run `pip install -r requirements.txt` again

### Tips
- Save frequently scraped data to CSV
- Use sample data for testing features
- Regular backups of important data
- Monitor memory usage for large datasets

## 🎉 Conclusion

Sistem Analisis Pariwisata Indonesia adalah aplikasi web modern yang siap production dengan:
- ✅ Web scraping capability
- ✅ Data visualization
- ✅ GIS mapping
- ✅ Interactive dashboard
- ✅ Export functionality

**Siap untuk digunakan dan dikembangkan lebih lanjut!**

---

Created: February 2026
Version: 1.0
Status: Production Ready
