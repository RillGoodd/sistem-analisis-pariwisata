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

# Minimal app - just run the basic structure
st.markdown("# 🏖️ Sistem Analisis Pariwisata Indonesia")

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

# Load sample data
@st.cache_data
def load_sample_data():
    try:
        df = pd.read_csv('sample_data_complete.csv')
        return df
    except:
        return None

# Sidebar
st.sidebar.title("📍 Menu")
page = st.sidebar.radio("Pilih Halaman", ["Dashboard", "Upload Data", "Visualisasi", "Peta"])

if page == "Dashboard":
    st.markdown("## 📊 Dashboard")
    sample_df = load_sample_data()
    if sample_df is not None:
        st.session_state.df = sample_df
        st.session_state.data_loaded = True
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📍 Destinasi", len(sample_df))
        with col2:
            if 'kategori' in sample_df.columns:
                st.metric("🏷️ Kategori", sample_df['kategori'].nunique())
        with col3:
            st.metric("✅ Status", "Ready")
        
        st.dataframe(sample_df.head(10), use_container_width=True)
    
elif page == "Upload Data":
    st.markdown("## 📤 Upload File atau Scrape URL")
    
    tab1, tab2 = st.tabs(["Upload File", "Scrape URL"])
    
    with tab1:
        uploaded_file = st.file_uploader("Upload CSV/Excel", type=['csv', 'xlsx', 'xls'])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                scraper = TourismDataScraper()
                df = scraper.map_columns(df)
                df = scraper.extract_coordinates(df)
                
                st.session_state.df = df
                st.session_state.data_loaded = True
                st.success(f"✅ {len(df)} records loaded!")
                st.dataframe(df.head(10), use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
    
    with tab2:
        st.markdown("### Scrape dari URL")
        url = st.text_input("URL")
        if st.button("🚀 Scrape"):
            if url:
                try:
                    scraper = TourismDataScraper()
                    df = scraper.scrape_from_url(url)
                    if df is not None and len(df) > 0:
                        df = scraper.map_columns(df)
                        df = scraper.extract_coordinates(df)
                        st.session_state.df = df
                        st.session_state.data_loaded = True
                        st.success(f"✅ {len(df)} records scraped!")
                        st.dataframe(df.head(10), use_container_width=True)
                    else:
                        st.error("No data found")
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "Visualisasi":
    st.markdown("## 📊 Visualisasi Data")
    if st.session_state.df is not None:
        df = st.session_state.df
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'kategori' in df.columns:
                fig = px.pie(values=df['kategori'].value_counts().values, names=df['kategori'].value_counts().index, title='Per Kategori')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'rating' in df.columns:
                df_num = df.copy()
                df_num['rating'] = pd.to_numeric(df_num['rating'], errors='coerce')
                df_num = df_num.dropna(subset=['rating'])
                fig = px.histogram(df_num, x='rating', nbins=20, title='Rating Distribution')
                st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True, height=300)
    else:
        st.warning("Load data dulu")

elif page == "Peta":
    st.markdown("## 🗺️ GIS Mapping")
    if st.session_state.df is not None:
        df = st.session_state.df
        scraper = TourismDataScraper()
        
        if 'latitude' not in df.columns:
            df = scraper.extract_coordinates(df)
            st.session_state.df = df
        
        valid_mask = (df['latitude'].notna()) & (df['longitude'].notna())
        df_map = df[valid_mask]
        
        if len(df_map) > 0:
            center_lat = df_map['latitude'].mean()
            center_lon = df_map['longitude'].mean()
            m = folium.Map(location=[center_lat, center_lon], zoom_start=5)
            
            for idx, row in df_map.iterrows():
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=8,
                    popup=str(row.get('nama', 'N/A')),
                    color='blue'
                ).add_to(m)
            
            st_folium(m, width=1200, height=600)
        else:
            st.error("No valid coordinates")
    else:
        st.warning("Load data dulu")
