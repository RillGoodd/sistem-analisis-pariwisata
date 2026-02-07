import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
import os
from scraper import TourismDataScraper

# Page config
st.set_page_config(
    page_title="Sistem Analisis Pariwisata Indonesia",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced Styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        padding: 1rem 2rem;
    }
    
    /* Typography */
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #ff7f0e;
        border-bottom: 3px solid #ff7f0e;
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    h3 {
        color: #2ca02c;
    }
    
    /* Metrics Cards */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        border-left: 5px solid #fff;
    }
    
    /* Data Table */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Cards for Dashboard */
    .dashboard-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        border-left: 5px solid white;
    }
    
    .dashboard-card-2 {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        border-left: 5px solid white;
    }
    
    .dashboard-card-3 {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(67, 233, 123, 0.3);
        border-left: 5px solid white;
    }
    
    /* Alerts & Info Boxes */
    .stAlert {
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #ff7f0e;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border-color: #e0e0e0;
    }
    
    /* Sidebar styles */
    .stSidebar {
        background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Custom Upload Section */
    .upload-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        margin: 20px 0;
        border: 2px dashed rgba(255, 255, 255, 0.3);
    }
    
    .upload-title {
        color: white;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    .upload-description {
        color: rgba(255, 255, 255, 0.9);
        font-size: 14px;
        margin-bottom: 20px;
    }
    
    .row-selector {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

def load_data_from_file(filepath):
    """Load data from CSV/Excel"""
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(filepath)
        else:
            return None
        
        st.session_state.df = df
        st.session_state.data_loaded = True
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Sidebar Navigation
st.sidebar.title("Menu Navigasi")
page = st.sidebar.radio(
    "Pilih Halaman",
    ["Dashboard", "Web Scraping", "Visualisasi Data", "GIS Mapping"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Informasi")
st.sidebar.info("""
**Sistem Analisis & Pemetaan Data Pariwisata**
🌍 **Support Worldwide Data!**

✅ Web Scraping dari URL (mana saja)
✅ Upload file CSV/Excel  
✅ Visualisasi interaktif
✅ GIS Mapping dengan Folium
✅ Support data worldwide dengan koordinat

📍 **Tips:** Jika data sudah punya kolom
lat/lon, GIS mapping berfungsi di
manapun di dunia!
""")

st.sidebar.markdown("---")
try:
    if st.session_state.get('data_loaded', False):
        st.sidebar.success(f"✅ Data loaded: {len(st.session_state.df)} records")
    else:
        st.sidebar.warning("⚠️ Belum ada data")
except Exception as e:
    st.sidebar.warning("⚠️ Belum ada data")

# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":
    st.markdown("# 📊 Dashboard Sistem Analisis Pariwisata")
    
    if not st.session_state.get('data_loaded', False) or st.session_state.df is None:
        # Welcome Section
        st.markdown("---")
        
        # Deskripsi Sistem
        st.markdown("""
        ## 🌍 Tentang Sistem Analisis & Pemetaan Data Pariwisata
        
        **Sistem Analisis Pariwisata Indonesia** adalah aplikasi web modern yang dirancang untuk:
        - 🕷️ **Web Scraping:** Mengekstrak data pariwisata dari berbagai sumber online
        - 📊 **Data Analysis:** Analisis mendalam dengan visualisasi interaktif
        - 🗺️ **GIS Mapping:** Pemetaan geografis destinasi wisata dengan Folium
        - 🌐 **Worldwide Support:** Mendukung data pariwisata dari seluruh dunia
        
        Aplikasi ini dibangun menggunakan **Streamlit**, **Plotly**, **Folium**, dan **Pandas** untuk memberikan
        pengalaman analisis data yang responsif dan user-friendly.
        """)
        
        st.markdown("---")
        
        # Feature Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="dashboard-card">
                <h3>🕷️ Web Scraping</h3>
                <p>Otomatis extract data dari URL terstruktur dengan strategi parsing multi-layer</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="dashboard-card-2">
                <h3>📈 Visualisasi Data</h3>
                <p>5 jenis analisis berbeda: Overview, Demographics, Geographic, Detailed, Correlation</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="dashboard-card-3">
                <h3>🗺️ GIS Mapping</h3>
                <p>Peta interaktif dengan 5 style berbeda dan insights tentang destinasi populer</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Getting Started
        st.info("""
        ✨ **Selamat datang! Mulai gunakan sistem ini dalam 4 langkah:**
        
        **1️⃣ Load Data (Web Scraping)**
        - Buka tab **Web Scraping**
        - Pilih scrape dari URL atau upload file CSV/Excel
        - Data akan tersimpan dalam session
        
        **2️⃣ Dashboard Overview**
        - Kembali ke **Dashboard** atau refresh
        - Lihat ringkasan data, metrics, dan statistik
        
        **3️⃣ Analisis Mendalam (Visualisasi Data)**
        - Buka tab **Visualisasi Data**
        - Pilih 5 jenis analisis: Overview, Demographics, Geographic, Detailed Analysis, Correlation
        - Eksplorasi data dengan chart interaktif
        
        **4️⃣ Pemetaan Geografis (GIS Mapping)**
        - Buka tab **GIS Mapping**
        - Visualisasi destinasi di peta interaktif
        - Lihat insights tentang destinasi populer
        
        💡 **Tips:** Data tersimpan selama session aktif. Upload ulang jika refresh halaman.
        """)
        
        st.markdown("---")
        
        # Fitur Lengkap
        st.markdown("### 🎯 Fitur Lengkap Sistem")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🕷️ Web Scraping & Data Loading
            - ✅ Scrape dari URL dengan tabel HTML
            - ✅ Support CSV dan Excel files
            - ✅ Auto-detect dan mapping kolom
            - ✅ Smart data cleaning
            - ✅ Support 3 retry strategies
            - ✅ Worldwide data support
            
            #### 📊 Data Analysis & Visualization
            - ✅ 5 Tabs visualisasi berbeda
            - ✅ Interactive charts dengan Plotly
            - ✅ Multiple analysis types
            - ✅ Distribution analysis
            - ✅ Trend detection
            - ✅ Correlation matrix heatmap
            """)
        
        with col2:
            st.markdown("""
            #### 🗺️ GIS Mapping & Insights
            - ✅ Interactive Folium maps
            - ✅ 5 map style options
            - ✅ 34 Indonesian provinces
            - ✅ Color-coded markers
            - ✅ Multi-filter support
            - ✅ Insights destinasi populer
            
            #### 💾 Data Management
            - ✅ CSV/Excel import & export
            - ✅ Coordinate validation
            - ✅ UTF-8 encoding support
            - ✅ Max 3000 rows processing
            - ✅ Real-time data mapping
            - ✅ Session-based storage
            """)
        
        st.markdown("---")
        
        # Teknologi yang Digunakan
        st.markdown("### 🛠️ Teknologi & Framework")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Frontend & UI:**")
            st.write("- Streamlit")
            st.write("- Plotly Express")
            st.write("- Folium")
        
        with col2:
            st.write("**Data Processing:**")
            st.write("- Pandas")
            st.write("- NumPy")
            st.write("- BeautifulSoup4")
        
        with col3:
            st.write("**Web & Integration:**")
            st.write("- Requests")
            st.write("- Streamlit-Folium")
            st.write("- OpenPyXL (Excel)")
        
        st.markdown("---")
        
        # Contoh Use Cases
        st.markdown("### 📋 Contoh Use Cases")
        
        st.write("""
        - **🏨 Tourism Industry:** Analisis destinasi wisata populer dan trend kunjungan
        - **📈 Market Research:** Riset pasar pariwisata dan kompetitor destinasi
        - **🎓 Academic Research:** Studi tentang pola distribusi dan karakteristik destinasi
        - **📱 Developer Tools:** Backend system untuk aplikasi pariwisata
        - **📊 Business Intelligence:** Dashboard analytics untuk stakeholder pariwisata
        """)
    
    else:
        df = st.session_state.df
        
        st.markdown("---")
        
        # Key Metrics Row 1 - Only show valid metrics without misleading N/A
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📍 Total Destinasi", len(df), delta=f"+{len(df)} records")
        
        with col2:
            if 'kategori' in df.columns and not df['kategori'].isna().all():
                unique_cat = df['kategori'].nunique()
                st.metric("🏷️ Kategori Unik", unique_cat, delta=f"{unique_cat} types")
        
        with col3:
            if 'provinsi' in df.columns and not df['provinsi'].isna().all():
                unique_prov = df['provinsi'].nunique()
                st.metric("🏛️ Provinsi/Lokasi", unique_prov, delta=f"{unique_prov} areas")
        
        with col4:
            if 'rating' in df.columns and not df['rating'].isna().all():
                try:
                    valid_ratings = pd.to_numeric(df['rating'], errors='coerce')
                    avg_rating = valid_ratings[valid_ratings.notna()].mean()
                    if pd.notna(avg_rating):
                        st.metric("⭐ Rata-rata Rating", f"{avg_rating:.2f}", delta="⭐⭐⭐⭐")
                except:
                    pass

# ==================== WEB SCRAPING PAGE ====================
elif page == "Web Scraping":
    st.markdown("# 🕷️ Web Scraping Data Pariwisata")
    
    tab1, tab2 = st.tabs(["🌐 Scrape dari URL", "📤 Upload File"])
    
    with tab1:
        st.markdown("## 🌐 Scrape dari URL")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            url = st.text_input(
                "🔗 Masukkan URL (Tabel HTML, CSV, atau JSON)",
                "",
                placeholder="https://example.com/data",
                key="scrape_url"
            )
        
        with col2:
            scrape_btn = st.button("🚀 Scrape", type="primary", use_container_width=True)
        
        # Row selection for scraping
        st.markdown("---")
        st.markdown("### 🔢 Pengaturan Data")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            scrape_max_rows = st.slider(
                "Pilih jumlah data yang ingin discrape",
                min_value=10,
                max_value=3000,
                value=100,
                step=10,
                key="scrape_row_slider",
                help="Maksimal 3000 baris. Semakin banyak data = loading lebih lama"
            )
        
        with col2:
            st.metric("Max Baris", "3000", delta="Limit")
        
        with col3:
            st.metric("Pilihan Anda", f"{scrape_max_rows:,}", delta="rows")
        
        st.markdown("---")
        
        with st.expander("💡 TIPS SCRAPING DATA"):
            st.info("""
            **Gunakan URL dengan data terstruktur yang mudah di-parse:**
            
            📍 Contoh URL yang bisa dicoba:
            - Halaman HTML dengan tabel (`<table>` tags)
            - API public yang mengembalikan HTML/JSON
            - Website yang tidak strict dengan robots.txt
            - Data publik dari institutional websites
            
            ✅ **Best Practice:**
            - Cari halaman dengan tabel terstruktur
            - Mulai scrape dengan row limit kecil (50-100) dulu
            - Jika berhasil, increase ke 500+ rows
            - Simpan hasil scraping untuk backup
            
            ❌ **Hindari:**
            - Website yang explicit melarang scraping (robots.txt)
            - JavaScript-heavy pages (React, Vue, Angular)
            - Halaman yang memerlukan login/authentication
            - Content yang di-render dinamis client-side
            
            💡 **Tips Mencari URL:**
            1. Cari website dengan topik yang Anda ingin
            2. Inspect element → cari `<table>` tags
            3. Copy URL, paste ke field ini, set row limit
            4. Klik Scrape dan lihat hasilnya
            5. Jika berhasil, adjust row limit untuk lebih banyak data
            
            Sistem akan otomatis:
            - Detect & extract tabel HTML
            - Map column names ke format standar (nama, kategori, rating, dll)
            - Auto-generate koordinat dari nama lokasi/provinsi
            - Validasi data sebelum visualisasi
            """)
        
        if scrape_btn:
            if url and url.startswith(('http://', 'https://')):
                with st.spinner("⏳ Sedang scraping data..."):
                    try:
                        scraper = TourismDataScraper()
                        df = scraper.scrape_from_url(url)
                        
                        # Check if scraping returned valid data
                        if df is None or len(df) == 0:
                            st.error("❌ Tidak berhasil extract data dari URL - DataFrame kosong atau None")
                            st.info("💡 Solusi:\n- Gunakan salah satu URL dari REKOMENDASI yang disediakan\n- Pastikan URL bukan halaman dinamis/JavaScript")
                        else:
                            # Apply row limit
                            if len(df) > scrape_max_rows:
                                st.warning(f"⚠️ Data di-trim dari {len(df)} menjadi {scrape_max_rows} baris")
                                df = df.head(scrape_max_rows)
                            
                            st.session_state.df = df
                            st.session_state.data_loaded = True
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.success(f"✅ Berhasil scrape {len(df)} records!")
                            with col2:
                                st.info(f"📊 {len(df.columns)} kolom ditemukan")
                            with col3:
                                st.info(f"✨ Data siap untuk dianalisis")
                            
                            st.balloons()
                            
                            # Data preview - Before Mapping
                            st.markdown("### 📋 Data Hasil Scraping (Before Mapping)")
                            st.write(f"**Kolom:** {list(df.columns)}")
                            st.dataframe(df.head(10), use_container_width=True, height=300)
                            
                            # Column Mapping
                            st.markdown("---")
                            st.markdown("### 🔧 Column Mapping Otomatis")
                            
                            st.info("""
                            **Apa itu Column Mapping?**
                            Sistem otomatis mendeteksi dan menstandarkan nama kolom hasil scraping agar kompatibel dengan visualisasi.
                            """)
                            
                            scraper = TourismDataScraper()
                            df_mapped = scraper.map_columns(df)
                            df_mapped = scraper.extract_coordinates(df_mapped)
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**SEBELUM Mapping:**")
                                st.write(f"Kolom: {list(df.columns)}")
                                st.dataframe(df.head(5), use_container_width=True, height=200)
                            
                            with col2:
                                st.write("**SESUDAH Mapping + AUTO GEOCODING:**")
                                st.write(f"Kolom: {list(df_mapped.columns)}")
                                st.info("✅ Koordinat (latitude/longitude) otomatis di-generate dari nama lokasi/provinsi!")
                                st.dataframe(df_mapped.head(5), use_container_width=True, height=200)
                            
                            st.session_state.df = df_mapped
                            
                            # Data Quality Check
                            st.markdown("---")
                            st.markdown("### ✅ Data Quality & Accuracy Report")
                            
                            # Get detailed accuracy report
                            scraper = TourismDataScraper()
                            accuracy_report = scraper.get_data_accuracy_report(df_mapped)
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                quality_score = accuracy_report.get('data_quality_score', 0)
                                if quality_score >= 80:
                                    st.success(f"✅ Kualitas Data: {quality_score:.1f}%")
                                elif quality_score >= 60:
                                    st.warning(f"⚠️ Kualitas Data: {quality_score:.1f}%")
                                else:
                                    st.error(f"❌ Kualitas Data: {quality_score:.1f}%")
                            
                            with col2:
                                st.info(f"📊 Dataset Overview:\n- Total Baris: {len(df_mapped):,}\n- Total Kolom: {len(df_mapped.columns)}")
                            
                            with col3:
                                st.info(f"💾 Ukuran: {df_mapped.memory_usage(deep=True).sum() / 1024:.2f} KB")
                            
                            # Completeness by column
                            st.markdown("### 📋 Data Completeness per Kolom")
                            
                            completeness_data = []
                            for col, details in accuracy_report['completeness_by_column'].items():
                                completeness_data.append({
                                    'Kolom': col,
                                    'Completeness': f"{details['completeness_percent']:.1f}%",
                                    'Filled': details['filled'],
                                    'Missing': details['missing'],
                                })
                            
                            completeness_df = pd.DataFrame(completeness_data)
                            
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                fig = px.bar(
                                    completeness_df,
                                    x='Completeness',
                                    y='Kolom',
                                    orientation='h',
                                    title='📊 Data Completeness per Kolom (%)',
                                    color='Completeness',
                                    color_continuous_scale=['#ff4444', '#ffaa00', '#00cc00'],
                                    text='Completeness'
                                )
                                fig.update_traces(textposition='outside')
                                fig.update_layout(height=300)
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with col2:
                                st.markdown("**Penjelasan Completeness:**")
                                st.info("""
                                - **100%**: Semua baris terisi
                                - **80-99%**: Sebagian kecil kosong
                                - **50-79%**: Cukup data kosong
                                - **<50%**: Data banyak kosong
                                """)
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown("**WAJIB ADA:**")
                                required_cols = ['nama', 'provinsi', 'latitude', 'longitude']
                                for col in required_cols:
                                    if col in df_mapped.columns:
                                        st.write(f"✅ `{col}`")
                                    else:
                                        st.write(f"❌ `{col}`")
                            
                            with col2:
                                st.markdown("**DISARANKAN:**")
                                recommended_cols = ['kategori', 'rating', 'kota']
                                for col in recommended_cols:
                                    if col in df_mapped.columns:
                                        non_null = df_mapped[col].notna().sum()
                                        pct = (non_null / len(df_mapped) * 100)
                                        st.write(f"✅ `{col}` ({pct:.0f}%)")
                                    else:
                                        st.write(f"⚠️ `{col}`")
                            
                            with col3:
                                st.markdown("**OPSIONAL:**")
                                optional_cols = ['deskripsi', 'harga']
                                for col in optional_cols:
                                    if col in df_mapped.columns:
                                        non_null = df_mapped[col].notna().sum()
                                        pct = (non_null / len(df_mapped) * 100)
                                        st.write(f"✅ `{col}` ({pct:.0f}%)")
                                    else:
                                        st.write(f"⚠️ `{col}`")
                            
                            # Statistics
                            st.markdown("---")
                            st.markdown("### 📊 Informasi Dataset")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Jumlah Baris", len(df_mapped))
                            with col2:
                                st.metric("Jumlah Kolom", len(df_mapped.columns))
                            with col3:
                                st.metric("Memory", f"{df_mapped.memory_usage(deep=True).sum() / 1024:.2f} KB")
                            
                            # Download option
                            st.markdown("---")
                            st.markdown("### 💾 Download Data")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                csv = df_mapped.to_csv(index=False, encoding='utf-8-sig')
                                st.download_button(
                                    "📥 Download CSV",
                                    csv,
                                    "data_scraping.csv",
                                    "text/csv",
                                    use_container_width=True
                                )
                            
                            with col2:
                                try:
                                    from openpyxl import Workbook
                                    from openpyxl.utils.dataframe import dataframe_to_rows
                                    from io import BytesIO
                                    
                                    def to_excel_bytes(df):
                                        wb = Workbook()
                                        ws = wb.active
                                        for r in dataframe_to_rows(df, index=False, header=True):
                                            ws.append(r)
                                        stream = BytesIO()
                                        wb.save(stream)
                                        return stream.getvalue()
                                    
                                    excel_bytes = to_excel_bytes(df)
                                    st.download_button(
                                        "📥 Download Excel",
                                        excel_bytes,
                                        "data_scraping.xlsx",
                                        "application/vnd.ms-excel",
                                        use_container_width=True
                                    )
                                except:
                                    pass
                    
                    except Exception as e:
                        st.error(f"❌ Gagal scraping: {str(e)}")
                        st.info("💡 Solusi:\n- Periksa kembali URL\n- Pastikan situs dapat diakses\n- Coba URL lain dari rekomendasi")
            else:
                st.error("❌ Masukkan URL yang valid (mulai dengan http:// atau https://)")
    
    with tab2:
        st.markdown("## 📤 Upload File")
        
        uploaded_file = st.file_uploader(
            "Pilih file CSV atau Excel",
            type=['csv', 'xlsx', 'xls'],
            key="scrape_upload"
        )
        
        if uploaded_file:
            # Row selection for upload
            st.markdown("---")
            st.markdown("### 🔢 Pengaturan Data")
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                upload_max_rows = st.slider(
                    "Pilih jumlah data yang ingin diproses",
                    min_value=10,
                    max_value=3000,
                    value=100,
                    step=10,
                    key="upload_row_slider",
                    help="Maksimal 3000 baris. Semakin banyak data = loading lebih lama"
                )
            
            with col2:
                st.metric("Max Baris", "3000", delta="Limit")
            
            with col3:
                st.metric("Pilihan Anda", f"{upload_max_rows:,}", delta="rows")
            
            st.markdown("---")
            
            try:
                with st.spinner("⏳ Memproses file..."):
                    if uploaded_file.name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    # Apply row limit
                    if len(df) > upload_max_rows:
                        df = df.head(upload_max_rows)
                    
                    st.session_state.df = df
                    st.session_state.data_loaded = True
                    
                    st.success(f"✅ File berhasil diupload! ({len(df)} records)")
                    st.balloons()
                    
                    # Show original data
                    st.markdown("### 📋 Data Original (Sebelum Processing)")
                    st.dataframe(df.head(10), use_container_width=True, height=300)
                    
                    # Show data type mapping
                    st.markdown("---")
                    st.markdown("### 🔧 Column Mapping Otomatis")
                    
                    st.info("""
                    **Apa itu Column Mapping?**
                    
                    Sistem otomatis mendeteksi dan menstandarkan nama kolom Anda agar kompatibel dengan visualisasi.
                    
                    **Contoh:**
                    - "destination" → diubah menjadi "nama"
                    - "location" → diubah menjadi "provinsi"  
                    - "category" → diubah menjadi "kategori"
                    - "stars" → diubah menjadi "rating"
                    """)
                    
                    scraper = TourismDataScraper()
                    df_mapped = scraper.map_columns(df)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**SEBELUM Mapping:**")
                        st.write(f"Kolom: {list(df.columns)}")
                        st.dataframe(df.head(5), use_container_width=True, height=200)
                    
                    with col2:
                        st.write("**SESUDAH Mapping + AUTO GEOCODING:**")
                        st.write(f"Kolom: {list(df_mapped.columns)}")
                        st.info("✅ Koordinat (latitude/longitude) otomatis di-generate dari nama lokasi/provinsi untuk Indonesia maupun worldwide data!")
                        st.dataframe(df_mapped.head(5), use_container_width=True, height=200)
                    
                    # Update session state
                    st.session_state.df = df_mapped
                    
                    # Data Quality Check
                    st.markdown("---")
                    st.markdown("### ✅ Data Quality & Accuracy Report")
                    
                    # Get detailed accuracy report
                    scraper = TourismDataScraper()
                    accuracy_report = scraper.get_data_accuracy_report(df_mapped)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        quality_score = accuracy_report.get('data_quality_score', 0)
                        if quality_score >= 80:
                            st.success(f"✅ Kualitas Data: {quality_score:.1f}%")
                        elif quality_score >= 60:
                            st.warning(f"⚠️ Kualitas Data: {quality_score:.1f}%")
                        else:
                            st.error(f"❌ Kualitas Data: {quality_score:.1f}%")
                    
                    with col2:
                        st.info(f"📊 Dataset:\n- Total Baris: {len(df_mapped):,}\n- Total Kolom: {len(df_mapped.columns)}")
                    
                    with col3:
                        st.info(f"💾 Ukuran: {df_mapped.memory_usage(deep=True).sum() / 1024:.2f} KB")
                    
                    # Completeness chart
                    st.markdown("### 📋 Data Completeness per Kolom")
                    
                    completeness_data = []
                    for col, details in accuracy_report['completeness_by_column'].items():
                        completeness_data.append({
                            'Kolom': col,
                            'Completeness': f"{details['completeness_percent']:.1f}%",
                            'Filled': details['filled'],
                            'Missing': details['missing'],
                        })
                    
                    completeness_df = pd.DataFrame(completeness_data)
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        fig = px.bar(
                            completeness_df,
                            x='Completeness',
                            y='Kolom',
                            orientation='h',
                            title='📊 Data Completeness per Kolom (%)',
                            color='Completeness',
                            color_continuous_scale=['#ff4444', '#ffaa00', '#00cc00'],
                            text='Completeness'
                        )
                        fig.update_traces(textposition='outside')
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown("**Interpretasi Completeness:**")
                        st.info("""
                        - **100%**: Semua terisi
                        - **80-99%**: Sedikit kosong
                        - **50-79%**: Cukup kosong
                        - **<50%**: Banyak kosong
                        """)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**WAJIB ADA (Untuk Peta):**")
                        
                        required_cols = ['nama', 'provinsi', 'latitude', 'longitude']
                        for col in required_cols:
                            if col in df_mapped.columns:
                                st.write(f"✅ `{col}` - OK")
                            else:
                                st.write(f"❌ `{col}` - MISSING")
                    
                    with col2:
                        st.markdown("**SANGAT DISARANKAN:**")
                        
                        recommended_cols = ['kategori', 'rating', 'kota']
                        for col in recommended_cols:
                            if col in df_mapped.columns:
                                non_null = df_mapped[col].notna().sum()
                                pct = (non_null / len(df_mapped) * 100)
                                st.write(f"✅ `{col}` - {pct:.0f}% filled")
                            else:
                                st.write(f"⚠️ `{col}` - MISSING")
                    
                    with col3:
                        st.markdown("**OPSIONAL (Bonus):**")
                        
                        optional_cols = ['deskripsi', 'harga']
                        for col in optional_cols:
                            if col in df_mapped.columns:
                                non_null = df_mapped[col].notna().sum()
                                pct = (non_null / len(df_mapped) * 100)
                                st.write(f"✅ `{col}` - {pct:.0f}% filled")
                            else:
                                st.write(f"⚠️ `{col}` - MISSING")
                    
                    # Coordinate Validation
                    if 'latitude' in df_mapped.columns and 'longitude' in df_mapped.columns:
                        st.markdown("---")
                        st.markdown("### 📍 Validasi Koordinat")
                        
                        valid_coords = (
                            (df_mapped['latitude'].notna()) &
                            (df_mapped['longitude'].notna()) &
                            (df_mapped['latitude'] >= -90) &
                            (df_mapped['latitude'] <= 90) &
                            (df_mapped['longitude'] >= -180) &
                            (df_mapped['longitude'] <= 180)
                        )
                        
                        valid_count = valid_coords.sum()
                        total_count = len(df_mapped)
                        valid_pct = (valid_count / total_count * 100)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if valid_pct >= 90:
                                st.success(f"✅ Valid Coordinates: {valid_count}/{total_count} ({valid_pct:.1f}%)")
                            elif valid_pct >= 70:
                                st.warning(f"⚠️ Valid Coordinates: {valid_count}/{total_count} ({valid_pct:.1f}%)")
                            else:
                                st.error(f"❌ Valid Coordinates: {valid_count}/{total_count} ({valid_pct:.1f}%)")
                        
                        with col2:
                            if valid_pct >= 90:
                                st.write("**Status:** Siap untuk GIS Mapping ✅")
                            else:
                                st.write("**Status:** Perlu Data Cleansing ⚠️")
                        
                        with col3:
                            st.write(f"**Lat Range:** {df_mapped['latitude'].min():.2f} to {df_mapped['latitude'].max():.2f}")
                            st.write(f"**Lon Range:** {df_mapped['longitude'].min():.2f} to {df_mapped['longitude'].max():.2f}")
                    
                    # Statistics
                    st.markdown("---")
                    st.markdown("### 📊 Dataset Statistics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Jumlah Baris", len(df_mapped))
                    with col2:
                        st.metric("Jumlah Kolom", len(df_mapped.columns))
                    with col3:
                        missing = df_mapped.isnull().sum().sum()
                        st.metric("Missing Values", missing)
                    with col4:
                        st.metric("Memory", f"{df_mapped.memory_usage(deep=True).sum() / 1024:.2f} KB")
                    
                    # Download option
                    st.markdown("---")
                    st.markdown("### 💾 Download Data Hasil Mapping")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        csv = df_mapped.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            "📥 Download CSV",
                            csv,
                            "data_mapped.csv",
                            "text/csv",
                            use_container_width=True
                        )
                    
                    with col2:
                        st.success("""
                        ✅ Data Processing Complete!
                        
                        Silakan buka **Dashboard** atau **Visualisasi Data** untuk analisis lebih lanjut.
                        """)
                    
                    # Tips untuk data yang lebih baik
                    with st.expander("💡 Tips untuk Data yang Lebih Baik", expanded=False):
                        st.markdown("""
                        **Untuk Visualisasi LENGKAP, pastikan data Anda memiliki:**
                        
                        1. **Nama Destinasi** (`nama`)
                           - ✅ Harus unik untuk setiap destinasi
                           - ✅ Jangan kosong
                        
                        2. **Lokasi** (`provinsi` atau `kota`)
                           - ✅ Nama benar sesuai geografis
                           - ✅ Format standar
                        
                        3. **Kategori** (`kategori`)
                           - ✅ Konsisten (Pantai, Gunung, Museum, Candi, dll)
                           - ✅ Jangan terlalu banyak variasi
                        
                        4. **Rating** (`rating`)
                           - ✅ Dalam format numerik (0-5)
                           - ✅ Jangan ada rating > 5 atau < 0
                        
                        5. **Koordinat** (`latitude`, `longitude`)
                           - ✅ Untuk Indonesia: auto-generated dari provinsi
                           - ✅ Untuk Worldwide: harus ada data koordinat
                           - ✅ Format desimal (-7.6079, 110.2038)
                        """)
                    
            except Exception as e:
                st.error(f"❌ Gagal upload file: {e}")
                st.info("💡 Tips:\n- Pastikan file adalah CSV atau Excel yang valid\n- Cek format dan encoding file")

# ==================== VISUALISASI DATA PAGE ====================
elif page == "Visualisasi Data":
    st.markdown("# 📊 Visualisasi Data Pariwisata")
    
    if not st.session_state.get('data_loaded', False) or st.session_state.df is None:
        st.warning("⚠️ Belum ada data. Silakan load data di halaman Web Scraping")
        st.info("💡 **Cara menggunakan:**\n1. Buka Web Scraping\n2. Scrape dari URL atau Upload file Anda\n3. Kembali ke halaman ini untuk analisis data")
    else:
        df = st.session_state.df
        
        st.markdown("---")
        
        # Show available columns info
        st.markdown("### 📋 Kolom yang Tersedia dalam Dataset")
        
        available_cols = list(df.columns)
        required_cols = ['nama', 'provinsi', 'latitude', 'longitude']
        optional_cols = ['kategori', 'rating', 'kota', 'deskripsi', 'harga']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**WAJIB:**")
            for col in required_cols:
                if col in available_cols:
                    st.write(f"✅ `{col}`")
                else:
                    st.write(f"❌ `{col}` (MISSING)")
        
        with col2:
            st.markdown("**DISARANKAN:**")
            for col in optional_cols[:2]:
                if col in available_cols:
                    st.write(f"✅ `{col}`")
                else:
                    st.write(f"⚠️ `{col}` (MISSING)")
        
        with col3:
            st.markdown("**LAINNYA:**")
            other_cols = [c for c in available_cols if c not in required_cols + optional_cols]
            if other_cols:
                for col in other_cols[:3]:
                    st.write(f"📊 `{col}`")
            else:
                st.write("_(tidak ada kolom tambahan)_")
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview",
            "👥 Demographics",
            "🌍 Geographic",
            "📊 Detailed Analysis",
            "📋 Correlation"
        ])
        
        # TAB 1: OVERVIEW
        with tab1:
            st.markdown("## 📈 Overview Data Pariwisata")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📍 Total Destinasi", len(df))
            with col2:
                if 'kategori' in df.columns:
                    st.metric("🏷️ Kategori Unik", df['kategori'].nunique())
                else:
                    st.metric("🏷️ Kategori Unik", "N/A")
            with col3:
                if 'rating' in df.columns:
                    try:
                        avg = pd.to_numeric(df['rating'], errors='coerce').mean()
                        st.metric("⭐ Rata-rata Rating", f"{avg:.2f}")
                    except:
                        st.metric("⭐ Rata-rata Rating", "N/A")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            # Kategori Distribution
            if 'kategori' in df.columns and not df['kategori'].isna().all():
                with col1:
                    kategori_counts = df['kategori'].value_counts()
                    fig = px.pie(
                        values=kategori_counts.values,
                        names=kategori_counts.index,
                        title='📊 Distribusi Destinasi per Kategori',
                        hole=0.3,
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                with col1:
                    st.warning("Kolom 'kategori' tidak ditemukan")
            
            # Rating Distribution
            if 'rating' in df.columns and not df['rating'].isna().all():
                with col2:
                    df_numeric = df.copy()
                    df_numeric['rating'] = pd.to_numeric(df_numeric['rating'], errors='coerce')
                    df_numeric = df_numeric.dropna(subset=['rating'])
                    
                    if len(df_numeric) > 0:
                        fig = px.histogram(
                            df_numeric,
                            x='rating',
                            nbins=20,
                            title='⭐ Distribusi Rating Destinasi',
                            labels={'rating': 'Rating'},
                            color_discrete_sequence=['#1f77b4'],
                            marginal='box'
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                with col2:
                    st.warning("Kolom 'rating' tidak ditemukan")
        
        # TAB 2: DEMOGRAPHICS
        with tab2:
            st.markdown("## 👥 Analisis Demographics")
            
            col1, col2 = st.columns(2)
            
            # Kategori
            if 'kategori' in df.columns and not df['kategori'].isna().all():
                with col1:
                    kategori_data = df['kategori'].value_counts().reset_index()
                    kategori_data.columns = ['kategori', 'count']
                    
                    fig = px.bar(
                        kategori_data,
                        x='count',
                        y='kategori',
                        orientation='h',
                        title='📌 Destinasi per Kategori',
                        labels={'count': 'Jumlah', 'kategori': 'Kategori'},
                        color='count',
                        color_continuous_scale='Blues',
                        text='count'
                    )
                    fig.update_traces(textposition='outside')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                with col1:
                    st.info("📌 Kategori: Gunakan fitur Detailed Analysis untuk eksplorasi lebih lanjut")
            
            # Provinsi / Location
            if 'provinsi' in df.columns and not df['provinsi'].isna().all():
                with col2:
                    provinsi_data = df['provinsi'].value_counts().reset_index()
                    provinsi_data.columns = ['provinsi', 'count']
                    
                    fig = px.bar(
                        provinsi_data,
                        x='count',
                        y='provinsi',
                        orientation='h',
                        title='🏛️ Destinasi per Lokasi',
                        labels={'count': 'Jumlah', 'provinsi': 'Lokasi'},
                        color='count',
                        color_continuous_scale='Greens',
                        text='count'
                    )
                    fig.update_traces(textposition='outside')
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                with col2:
                    st.info("🏛️ Lokasi: Data dimuat dari koordinat atau nama lokasi yang terdeteksi")

        
        # TAB 3: GEOGRAPHIC
        with tab3:
            st.markdown("## 🌍 Analisis Geographic")
            
            col1, col2 = st.columns(2)
            
            # Provinsi Distribution
            if 'provinsi' in df.columns and not df['provinsi'].isna().all():
                with col1:
                    prov_stats = df['provinsi'].value_counts()
                    fig = px.sunburst(
                        df[['provinsi']],
                        path=['provinsi'],
                        title='🗺️ Persebaran Destinasi per Lokasi',
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    fig.update_layout(height=450)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                with col1:
                    st.info("🗺️ Geographic: Buka GIS Mapping untuk visualisasi peta interaktif")
            
            # Kategori by Provinsi
            if 'kategori' in df.columns and 'provinsi' in df.columns:
                if not df['kategori'].isna().all() and not df['provinsi'].isna().all():
                    with col2:
                        cross_tab = pd.crosstab(df['provinsi'], df['kategori'])
                        fig = px.bar(
                            cross_tab.reset_index().melt(id_vars='provinsi'),
                            x='provinsi',
                            y='value',
                            color='kategori',
                            barmode='stack',
                            title='📊 Distribusi Kategori per Lokasi',
                            labels={'value': 'Jumlah', 'provinsi': 'Lokasi', 'kategori': 'Kategori'},
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        fig.update_layout(height=450, xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    with col2:
                        st.info("📊 Data kategori atau lokasi tidak lengkap. Gunakan Detailed Analysis untuk eksplorasi.")
            else:
                with col2:
                    st.info("📊 Kategori dan lokasi data tidak tersedia. Coba tab lainnya untuk analisis yang berbeda.")
        
        # TAB 4: DETAILED ANALYSIS
        with tab4:
            st.markdown("## 📊 Detailed Analysis")
            
            analysis_type = st.selectbox(
                "🔍 Pilih Tipe Analisis",
                ["Distribution", "Scatter Plot", "Percentage", "Trend", "Box Plot"],
                key="analysis_select"
            )
            
            if analysis_type == "Distribution":
                object_cols = df.select_dtypes(include=['object']).columns.tolist()
                if object_cols:
                    col = st.selectbox("Pilih Kolom", object_cols, key="dist_col")
                    if col and not df[col].isna().all():
                        value_counts = df[col].value_counts()
                        fig = px.bar(
                            x=value_counts.values,
                            y=value_counts.index,
                            orientation='h',
                            title=f'📊 Distribusi {col}',
                            labels={'x': 'Jumlah', 'y': col},
                            color=value_counts.values,
                            color_continuous_scale='Blues',
                            text=value_counts.values
                        )
                        fig.update_traces(textposition='outside')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning(f"Kolom '{col}' kosong atau belum dipilih")
                else:
                    st.warning("Tidak ada kolom object yang ditemukan")
            
            elif analysis_type == "Scatter Plot":
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if len(numeric_cols) >= 2:
                    col1, col2 = st.columns(2)
                    with col1:
                        x_col = st.selectbox("Sumbu X", numeric_cols, key="scatter_x")
                    with col2:
                        y_col = st.selectbox("Sumbu Y", numeric_cols, index=min(1, len(numeric_cols)-1), key="scatter_y")
                    
                    if x_col and y_col and x_col != y_col:
                        try:
                            fig = px.scatter(
                                df,
                                x=x_col,
                                y=y_col,
                                title=f'📍 {x_col} vs {y_col}',
                                color_discrete_sequence=['#ff7f0e'],
                                labels={x_col: x_col, y_col: y_col}
                            )
                            fig.update_traces(marker=dict(size=10, opacity=0.6))
                            st.plotly_chart(fig, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error membuat scatter plot: {e}")
                    else:
                        st.warning("Pilih kolom yang berbeda untuk X dan Y")
                else:
                    st.warning("Minimal 2 kolom numerik diperlukan")
            
            elif analysis_type == "Percentage":
                object_cols = df.select_dtypes(include=['object']).columns.tolist()
                if object_cols:
                    col = st.selectbox("Pilih Kolom", object_cols, key="pct_col")
                    if col and not df[col].isna().all():
                        dist = df[col].value_counts()
                        pct_data = pd.DataFrame({
                            'kategori': dist.index,
                            'nilai': dist.values,
                            'persentase': (dist.values / dist.sum() * 100).round(2)
                        })
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            fig = px.pie(
                                pct_data,
                                values='nilai',
                                names='kategori',
                                title=f'📈 Persentase {col}',
                                labels='kategori'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            st.write("**Tabel Persentase:**")
                            st.dataframe(pct_data, use_container_width=True)
                else:
                    st.warning("Tidak ada kolom untuk analisis persentase")
            
            elif analysis_type == "Trend":
                # Check for time-series or sequential data
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if numeric_cols:
                    selected_col = st.selectbox("Pilih Kolom Numerik", numeric_cols, key="trend_col")
                    if selected_col:
                        df_sorted = df.reset_index(drop=True).copy()
                        df_sorted['index'] = range(len(df_sorted))
                        
                        fig = px.line(
                            df_sorted,
                            x='index',
                            y=selected_col,
                            title=f'📉 Trend {selected_col}',
                            labels={'index': 'Index', selected_col: selected_col},
                            markers=True,
                            color_discrete_sequence=['#2ca02c']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Tidak ada kolom numerik untuk analisis trend")
            
            elif analysis_type == "Box Plot":
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                object_cols = df.select_dtypes(include=['object']).columns.tolist()
                
                if numeric_cols:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        numeric_col = st.selectbox("Pilih Kolom Numerik", numeric_cols, key="box_numeric")
                    
                    with col2:
                        group_col = st.selectbox("Group By (Optional)", [None] + object_cols, key="box_group")
                    
                    try:
                        if group_col:
                            fig = px.box(
                                df,
                                x=group_col,
                                y=numeric_col,
                                title=f'📦 Box Plot {numeric_col} by {group_col}',
                                labels={numeric_col: numeric_col, group_col: group_col},
                                color_discrete_sequence=['#9467bd']
                            )
                        else:
                            fig = px.box(
                                df,
                                y=numeric_col,
                                title=f'📦 Box Plot {numeric_col}',
                                color_discrete_sequence=['#9467bd']
                            )
                        
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error membuat box plot: {e}")
                else:
                    st.warning("Tidak ada kolom numerik untuk box plot")
        
        # TAB 5: CORRELATION
        with tab5:
            st.markdown("## 📋 Correlation Analysis")
            
            numeric_df = df.select_dtypes(include=['number']).copy()
            
            if len(numeric_df.columns) >= 2:
                corr = numeric_df.corr()
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.imshow(
                        corr,
                        labels=dict(color="Korelasi"),
                        title="🔗 Correlation Matrix",
                        color_continuous_scale="RdBu",
                        zmin=-1,
                        zmax=1,
                        text_auto='.2f',
                        aspect='auto'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.write("**Interpretasi:**")
                    st.info("""
                    **Nilai Korelasi:**
                    - (+1.0 hingga +0.7): Sangat kuat positif
                    - (+0.7 hingga +0.4): Kuat positif
                    - (+0.4 hingga 0): Lemah positif
                    - (-0 hingga -0.4): Lemah negatif
                    - (-0.4 hingga -0.7): Kuat negatif
                    - (-0.7 hingga -1.0): Sangat kuat negatif
                    """)
                
                with st.expander("📊 Tabel Korelasi Detail"):
                    st.dataframe(corr, use_container_width=True)
            else:
                st.warning("⚠️ Minimal 2 kolom numerik diperlukan untuk correlation analysis")

# ==================== GIS MAPPING PAGE ====================
elif page == "GIS Mapping":
    st.markdown("# 🗺️ GIS Mapping - Pariwisata Worldwide 🌍")
    
    if not st.session_state.get('data_loaded', False) or st.session_state.df is None:
        st.warning("⚠️ Belum ada data. Silakan load data di halaman Web Scraping")
        st.info("""
        💡 **Cara Menggunakan GIS Mapping:**
        
        **Untuk Data Indonesia:**
        - Sistem otomatis generate koordinat dari nama lokasi
        
        **Untuk Data Worldwide:**
        - Pastikan file punya kolom 'latitude' dan 'longitude'
        - Koordinat otomatis generate dari nama lokasi jika ada
        - Atau upload file dengan koordinat sudah ada
        
        **Langkah:**
        1. Buka Web Scraping
        2. Upload/Scrape file dengan data + koordinat
        3. Kembali ke GIS Mapping untuk visualisasi peta
        """)
    else:
        df = st.session_state.df
        
        # Validate coordinates
        scraper = TourismDataScraper()
        
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            st.info("🔄 Generating coordinates from location data...")
            df = scraper.extract_coordinates(df)
            st.session_state.df = df
        else:
            st.success("✅ Kolom latitude & longitude sudah ada - Ready untuk worldwide mapping!")
        
        # Check jika ada valid coordinates
        valid_mask = TourismDataScraper.validate_coordinates(df)
        valid_records = valid_mask.sum()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Data Valid", f"{valid_records}/{len(df)}")
        with col2:
            if valid_records > 0:
                st.metric("📍 Koordinat Valid", f"{valid_records}")
            else:
                st.metric("📍 Koordinat Valid", "0")
        with col3:
            if valid_records > 0:
                pct = (valid_records / len(df) * 100)
                st.metric("📊 Validitas", f"{pct:.1f}%")
        
        st.markdown("---")
        
        if valid_records == 0:
            st.error("❌ Tidak ada koordinat yang valid dalam data")
            st.info("""
            💡 **Solusi untuk Worldwide Data:**
            
            **Untuk data Indonesia:**
            - Sistem otomatis generate dari nama provinsi/kota
            
            **Untuk data Worldwide:**
            1. Pastikan file punya kolom 'latitude' dan 'longitude'
            2. Format koordinat harus angka desimal:
               - Latitude: -90 hingga +90
               - Longitude: -180 hingga +180
            
            **Contoh format yang bekerja:**
            | Nama | Negara | Latitude | Longitude |
            |------|--------|----------|-----------|
            | Bangkok | Thailand | 13.7563 | 100.5018 |
            | Paris | France | 48.8566 | 2.3522 |
            | Tokyo | Japan | 35.6762 | 139.6503 |
            """)
        else:
            # Sidebar controls
            col1, col2 = st.columns(2)
            
            with col1:
                map_style = st.selectbox(
                    "🎨 Pilih Map Style",
                    ["OpenStreetMap", "Satellite", "Dark", "Topo", "Positron"],
                    index=0
                )
            
            with col2:
                zoom = st.slider("🔍 Zoom Level", 2, 15, 5)
            
            st.markdown("---")
            
            # Filter options
            st.markdown("### 🔍 Filter Data")
            col1, col2 = st.columns(2)
            
            # Normalize kategori upfront for consistency
            if 'kategori' in df.columns:
                df['kategori'] = df['kategori'].astype(str).str.strip().str.title()
            
            if 'provinsi' in df.columns and not df['provinsi'].isna().all():
                with col1:
                    selected_provinsi = st.multiselect(
                        "Pilih Provinsi",
                        sorted(df['provinsi'].unique()),
                        default=list(sorted(df['provinsi'].unique())[:5]),
                        key="gis_provinsi"
                    )
                    if selected_provinsi:
                        df_filtered = df[df['provinsi'].isin(selected_provinsi)]
                    else:
                        df_filtered = df
            else:
                df_filtered = df
            
            if 'kategori' in df.columns and not df_filtered['kategori'].isna().all():
                with col2:
                    selected_kategori = st.multiselect(
                        "Pilih Kategori",
                        sorted(df_filtered['kategori'].unique()),
                        default=list(sorted(df_filtered['kategori'].unique())),
                        key="gis_kategori"
                    )
                    if selected_kategori:
                        df_filtered = df_filtered[df_filtered['kategori'].isin(selected_kategori)]
            
            st.markdown("---")
            
            # Build map
            valid_mask = TourismDataScraper.validate_coordinates(df_filtered)
            df_map = df_filtered[valid_mask].copy()
            
            if len(df_map) > 0:
                # Calculate map center
                center_lat = df_map['latitude'].mean()
                center_lon = df_map['longitude'].mean()
                
                # Map style configurations
                tiles_config = {
                    'OpenStreetMap': {'tiles': 'OpenStreetMap', 'attr': None},
                    'Satellite': {
                        'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                        'attr': 'Tiles &copy; Esri'
                    },
                    'Dark': {
                        'url': 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png',
                        'attr': '&copy; OpenStreetMap contributors, &copy; CartoDB'
                    },
                    'Topo': {
                        'url': 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
                        'attr': 'Map data: &copy; OpenStreetMap contributors, SRTM | Map style: &copy; OpenTopoMap'
                    },
                    'Positron': {
                        'url': 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png',
                        'attr': '&copy; OpenStreetMap contributors, &copy; CartoDB'
                    }
                }
                
                # Create map with selected style
                config = tiles_config.get(map_style, tiles_config['OpenStreetMap'])
                
                if 'tiles' in config:
                    m = folium.Map(
                        location=[center_lat, center_lon],
                        zoom_start=zoom,
                        tiles=config['tiles'],
                        prefer_canvas=True
                    )
                else:
                    m = folium.Map(
                        location=[center_lat, center_lon],
                        zoom_start=zoom,
                        prefer_canvas=True
                    )
                    # Add custom tile layer with attribution (required for all custom tiles)
                    folium.TileLayer(
                        tiles=config['url'],
                        attr=config.get('attr', 'Map data'),
                        overlay=False,
                        control=True,
                        name=map_style
                    ).add_to(m)
                
                # Validate and normalize kategori before mapping
                if 'kategori' in df_map.columns:
                    df_map['kategori'] = df_map['kategori'].astype(str).str.strip().str.title()
                
                # Add markers with better styling - Extended color map
                color_map = {
                    'Pantai': '#0066CC',
                    'Gunung': '#CC1111',
                    'Danau': '#00CCFF',
                    'Candi': '#FF6600',
                    'Desa Wisata': '#00CC00',
                    'Taman Laut': '#0033CC',
                    'Taman Hiburan': '#FF9900',
                    'Air Panas': '#FF3333',
                    'Museum': '#9933CC',
                    'Goa': '#996633',
                    'Pulau': '#FFCC00',
                    'Taman Nasional': '#CC00CC',
                    'Air Terjun': '#00FF99',
                    'Attraction': '#FF6666',
                    'Temple': '#FF8800',
                    'Beach': '#0066CC',
                    'Mountain': '#CC1111',
                    'Lake': '#00CCFF',
                    'National Park': '#CC00CC',
                    'Waterfall': '#00FF99',
                }
                
                for idx, row in df_map.iterrows():
                    kategori = str(row.get('kategori', 'N/A')).strip().title()
                    color = color_map.get(kategori, color_map.get(str(row.get('kategori', 'N/A')).lower(), '#808080'))
                    
                    # Enhanced popup with rich formatting and complete information
                    rating_val = row.get('rating', 'N/A')
                    rating_str = f"⭐ {rating_val}" if (rating_val != 'N/A' and str(rating_val) != 'nan') else "Rating: -"
                    
                    price_val = row.get('harga', 'N/A')
                    if price_val != 'N/A' and str(price_val) != 'nan':
                        try:
                            price_str = f"Rp {int(float(price_val)):,}"
                        except:
                            price_str = "Harga: -"
                    else:
                        price_str = "Gratis"
                    
                    desc = row.get('deskripsi', '')
                    if desc and str(desc) != 'nan':
                        desc_str = str(desc)[:100] + "..." if len(str(desc)) > 100 else str(desc)
                    else:
                        desc_str = "Deskripsi tidak tersedia"
                    
                    # Rich HTML popup
                    popup_html = f"""
                    <div style="font-family: Arial; width: 300px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; padding: 15px; color: white;">
                        <h3 style="margin: 0 0 10px 0; color: #ffffff; border-bottom: 2px solid #ffd700; padding-bottom: 8px;">
                            📍 {row.get('nama', 'N/A')}
                        </h3>
                        <table style="width: 100%; font-size: 13px; line-height: 1.8;">
                            <tr>
                                <td style="width: 40%; padding: 4px; font-weight: bold;">🏛️ Lokasi:</td>
                                <td style="padding: 4px;">{row.get('provinsi', 'N/A')}</td>
                            </tr>
                            <tr style="background: rgba(255,255,255,0.1);">
                                <td style="width: 40%; padding: 4px; font-weight: bold;">🏙️ Kota:</td>
                                <td style="padding: 4px;">{row.get('kota', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td style="width: 40%; padding: 4px; font-weight: bold;">🏷️ Kategori:</td>
                                <td style="padding: 4px;">{kategori}</td>
                            </tr>
                            <tr style="background: rgba(255,255,255,0.1);">
                                <td style="width: 40%; padding: 4px; font-weight: bold;">⭐ Rating:</td>
                                <td style="padding: 4px;">{rating_str}</td>
                            </tr>
                            <tr>
                                <td style="width: 40%; padding: 4px; font-weight: bold;">💰 Tiket:</td>
                                <td style="padding: 4px;">{price_str}</td>
                            </tr>
                            <tr style="background: rgba(255,255,255,0.1);">
                                <td style="width: 40%; padding: 4px; font-weight: bold;">📍 Koordinat:</td>
                                <td style="padding: 4px; font-size: 11px;">{row['latitude']:.4f}, {row['longitude']:.4f}</td>
                            </tr>
                            <tr>
                                <td colspan="2" style="padding: 8px 4px; border-top: 1px solid rgba(255,255,255,0.3); font-size: 12px; font-style: italic;">
                                    📝 {desc_str}
                                </td>
                            </tr>
                        </table>
                    </div>
                    """
                    
                    # Rich tooltip that appears on hover with destination info
                    tooltip_text = f"""<b>{row.get('nama', 'N/A')}</b><br/>
                    📍 {row.get('provinsi', 'N/A')}<br/>
                    🏷️ {kategori}<br/>
                    ⭐ {rating_str}<br/>
                    💰 {price_str}<br/>
                    🌐 Lat: {row['latitude']:.4f}, Lon: {row['longitude']:.4f}"""
                    
                    folium.CircleMarker(
                        location=[row['latitude'], row['longitude']],
                        radius=10,
                        popup=folium.Popup(popup_html, max_width=350),
                        tooltip=folium.Tooltip(tooltip_text, sticky=False),
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.8,
                        weight=3
                    ).add_to(m)
                
                # Display map
                st.markdown("### 📍 Peta Interaktif")
                st_folium(m, width=1200, height=600)
                
                st.markdown("---")
                
                # Statistics
                st.markdown("### 📊 Statistik Geographic")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📍 Destinasi Pemetakan", len(df_map))
                
                with col2:
                    lat_range = f"{df_map['latitude'].min():.2f} - {df_map['latitude'].max():.2f}"
                    st.metric("📐 Latitude Range", lat_range)
                
                with col3:
                    lon_range = f"{df_map['longitude'].min():.2f} - {df_map['longitude'].max():.2f}"
                    st.metric("📐 Longitude Range", lon_range)
                
                with col4:
                    if 'rating' in df_map.columns:
                        try:
                            avg_rating = pd.to_numeric(df_map['rating'], errors='coerce').mean()
                            st.metric("⭐ Avg Rating", f"{avg_rating:.2f}")
                        except:
                            st.metric("⭐ Avg Rating", "N/A")
                
                st.markdown("---")
                
                # Category distribution with consistent color mapping
                if 'kategori' in df_map.columns:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Normalize kategori for consistency
                        df_map_normalized = df_map.copy()
                        df_map_normalized['kategori'] = df_map_normalized['kategori'].astype(str).str.strip().str.title()
                        
                        kategori_counts = df_map_normalized['kategori'].value_counts()
                        
                        # Create color mapping for pie chart consistent with map markers
                        color_map_extended = {
                            'Pantai': '#0066CC',
                            'Gunung': '#CC1111',
                            'Danau': '#00CCFF',
                            'Candi': '#FF6600',
                            'Desa Wisata': '#00CC00',
                            'Taman Laut': '#0033CC',
                            'Taman Hiburan': '#FF9900',
                            'Air Panas': '#FF3333',
                            'Museum': '#9933CC',
                            'Goa': '#996633',
                            'Pulau': '#FFCC00',
                            'Taman Nasional': '#CC00CC',
                            'Air Terjun': '#00FF99',
                        }
                        
                        # Map colors to categories
                        colors = [color_map_extended.get(cat, '#808080') for cat in kategori_counts.index]
                        
                        fig = px.pie(
                            values=kategori_counts.values,
                            names=kategori_counts.index,
                            title='📊 Distribusi Kategori pada Peta',
                            color_discrete_sequence=colors
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.write("**Daftar Destinasi pada Peta:**")
                        # Select only columns that exist
                        cols_to_show = ['nama', 'kategori', 'provinsi', 'rating']
                        available_cols = [col for col in cols_to_show if col in df_map.columns]
                        if not available_cols:
                            available_cols = ['nama', 'provinsi']  # fallback
                        
                        # Normalize kategori for display consistency
                        st_data = df_map[available_cols].copy().reset_index(drop=True)
                        if 'kategori' in st_data.columns:
                            st_data['kategori'] = st_data['kategori'].astype(str).str.strip().str.title()
                        st.dataframe(st_data, use_container_width=True, height=300)
                
                st.markdown("---")
                
                # Insights about Popular Destinations
                st.markdown("## 🎯 Insights: Destinasi Populer & Layak Dikunjungi")
                
                # Top Rated Destinations
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'rating' in df_map.columns:
                        st.markdown("### ⭐ Top Destinasi Berdasarkan Rating")
                        
                        df_with_rating = df_map.copy()
                        df_with_rating['rating'] = pd.to_numeric(df_with_rating['rating'], errors='coerce')
                        df_with_rating = df_with_rating.dropna(subset=['rating'])
                        
                        if len(df_with_rating) > 0:
                            # Select only columns that exist
                            cols_to_show = ['nama', 'kategori', 'provinsi', 'rating']
                            available_cols = [col for col in cols_to_show if col in df_with_rating.columns]
                            if not available_cols:
                                available_cols = ['nama', 'rating']
                            
                            top_rated = df_with_rating.nlargest(5, 'rating')[available_cols]
                            
                            for idx, row in top_rated.iterrows():
                                rating_val = float(row['rating'])
                                stars = '⭐' * int(rating_val) if rating_val > 0 else '🤔'
                                st.write(f"**{idx+1}. {row['nama']}**")
                                if 'provinsi' in row.index:
                                    provinsi_str = f" | 📍 {row['provinsi']}" if 'provinsi' in row.index else ""
                                else:
                                    provinsi_str = ""
                                if 'kategori' in row.index:
                                    kategori_str = f" | 🏷️ {row['kategori']}" if 'kategori' in row.index else ""
                                else:
                                    kategori_str = ""
                                if provinsi_str or kategori_str:
                                    st.write(f"   {provinsi_str}{kategori_str}")
                                st.write(f"   ⭐ Rating: {rating_val:.1f}/5 {stars}")
                                st.write("")
                        else:
                            st.info("Tidak ada data rating yang tersedia")
                
                with col2:
                    st.markdown("### 🏆 Destinasi Paling Banyak Dikunjungi")
                    
                    if 'kategori' in df_map.columns:
                        # Normalize kategori for consistency
                        df_for_count = df_map.copy()
                        df_for_count['kategori'] = df_for_count['kategori'].astype(str).str.strip().str.title()
                        kategori_counts = df_for_count['kategori'].value_counts()
                        top_kategori = kategori_counts.head(5)
                        
                        st.write("**Berdasarkan Jumlah Lokasi:**")
                        for idx, (kat, count) in enumerate(top_kategori.items(), 1):
                            st.write(f"**{idx}. {kat}**")
                            st.write(f"   📊 {count} destinasi")
                            st.write("")
                
                st.markdown("---")
                
                # Province-based insights
                st.markdown("### 🗺️ Insights Berdasarkan Lokasi")
                
                if 'provinsi' in df_map.columns:
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        top_prov = df_map['provinsi'].value_counts().head(1)
                        if len(top_prov) > 0:
                            top_prov_name = top_prov.index[0]
                            top_prov_count = top_prov.values[0]
                            st.metric("🥇 Lokasi Terbanyak", top_prov_name.split()[0], delta=f"{top_prov_count} destinasi")
                    
                    with col2:
                        # Highest rating by province
                        if 'rating' in df_map.columns:
                            df_temp = df_map.copy()
                            df_temp['rating'] = pd.to_numeric(df_temp['rating'], errors='coerce')
                            df_temp_valid = df_temp.dropna(subset=['rating'])
                            if len(df_temp_valid) > 0:
                                best_prov = df_temp_valid.loc[df_temp_valid['rating'].idxmax()]
                                if 'provinsi' in best_prov.index:
                                    prov_name = best_prov['provinsi'].split()[0]
                                    st.metric("🏆 Lokasi Tertinggi Rating", prov_name, delta=f"⭐ {best_prov['rating']:.1f}")
                                else:
                                    st.metric("🏆 Rating Tertinggi", f"⭐ {best_prov['rating']:.1f}")
                    
                    with col3:
                        total_prov = df_map['provinsi'].nunique()
                        st.metric("🌍 Total Lokasi Unik", total_prov, delta=f"{total_prov} areas")
                
                st.markdown("---")
                
                # Recommendations
                st.markdown("### 💡 Rekomendasi Destinasi Wisata")
                
                rec_col1, rec_col2 = st.columns(2)
                
                with rec_col1:
                    st.markdown("""
                    **Destinasi Berkualitas Tinggi (Rating > 3.5):**
                    """)
                    
                    if 'rating' in df_map.columns:
                        df_high_rating = df_map.copy()
                        df_high_rating['rating'] = pd.to_numeric(df_high_rating['rating'], errors='coerce')
                        df_high_rating = df_high_rating[df_high_rating['rating'] >= 3.5]
                        df_high_rating = df_high_rating.sort_values('rating', ascending=False)
                        
                        if len(df_high_rating) > 0:
                            for idx, row in df_high_rating.head(5).iterrows():
                                st.write(f"✅ **{row['nama']}** - Rating {row['rating']:.1f}/5")
                        else:
                            st.write("Tidak ada destinasi dengan rating > 3.5")
                
                with rec_col2:
                    st.markdown("""
                    **Destinasi Populer (Paling Banyak Dikunjungi):**
                    """)
                    
                    if 'kategori' in df_map.columns:
                        # Normalize kategori and count
                        df_for_recommend = df_map.copy()
                        df_for_recommend['kategori'] = df_for_recommend['kategori'].astype(str).str.strip().str.title()
                        top_destinations = df_for_recommend['kategori'].value_counts().head(5)
                        
                        for idx, (kat, count) in enumerate(top_destinations.items(), 1):
                            if count > 0:
                                st.write(f"📍 **{kat}** - {count} destinasi")
            else:
                st.error("❌ Tidak ada data yang valid untuk ditampilkan dengan filter yang dipilih")
