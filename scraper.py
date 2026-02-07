import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import re
from urllib.parse import urljoin
from io import StringIO
import random

class TourismDataScraper:
    """
    Web Scraper untuk data pariwisata Indonesia
    NO DUMMY DATA - Hanya scraping dari sumber real
    """
    
    # Data Provinsi Indonesia
    PROVINCES = [
        'Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi',
        'Sumatera Selatan', 'Bengkulu', 'Lampung', 'Kepulauan Bangka Belitung',
        'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah',
        'Daerah Istimewa Yogyakarta', 'Jawa Timur', 'Banten', 'Bali',
        'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Kalimantan Barat',
        'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur',
        'Kalimantan Utara', 'Sulawesi Utara', 'Sulawesi Tengah',
        'Sulawesi Selatan', 'Sulawesi Tenggara', 'Gorontalo',
        'Sulawesi Barat', 'Maluku', 'Maluku Utara', 'Papua', 'Papua Barat'
    ]
    
    def __init__(self):
        self.data = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        self.headers = {
            'User-Agent': self.user_agents[0],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def scrape_from_url(self, url, max_retries=3):
        """
        Scrape data dari URL yang diberikan (Support HTML, CSV, JSON)
        Returns: DataFrame atau None jika gagal
        """
        print(f"[SCRAPE] Starting scrape from URL: {url}")
        
        for attempt in range(max_retries):
            try:
                self.headers['User-Agent'] = self.user_agents[attempt % len(self.user_agents)]
                
                print(f"[ATTEMPT] Attempt {attempt + 1}/{max_retries}...")
                timeout = 60 if attempt > 0 else 30
                response = requests.get(url, headers=self.headers, timeout=timeout)
                response.raise_for_status()
                
                print(f"[OK] Response received (Status: {response.status_code})")
                response.encoding = response.apparent_encoding
                
                df = None
                content_type = response.headers.get('content-type', '').lower()
                url_lower = url.lower()
                
                # Strategy 0: CSV file
                if 'csv' in content_type or url_lower.endswith('.csv'):
                    print("[STRATEGY] Strategy 0: CSV file...")
                    try:
                        df = pd.read_csv(StringIO(response.text))
                        print(f"[CSV] Loaded: {len(df)} rows x {len(df.columns)} cols")
                    except Exception as e:
                        print(f"   [WARN] CSV parsing failed: {e}")
                
                # Strategy 1: Pandas read_html
                if df is None and ('text/html' in content_type or url_lower.startswith('http')):
                    print("[STRATEGY] Strategy 1: Pandas read_html...")
                    try:
                        dfs = pd.read_html(StringIO(response.text))
                        if dfs:
                            valid_dfs = [d for d in dfs if len(d) >= 3 and len(d.columns) >= 2]
                            if valid_dfs:
                                df = max(valid_dfs, key=len)
                                print(f"[HTML] Found table: {len(df)} rows x {len(df.columns)} cols")
                    except Exception as e:
                        print(f"   [WARN] read_html failed: {e}")
                
                # Strategy 2: BeautifulSoup parsing
                if df is None:
                    print("[STRATEGY] Strategy 2: BeautifulSoup parsing...")
                    try:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        table = self._parse_html_table(soup)
                        df = table if table is not None else None
                        if df is not None:
                            print(f"[SOUP] Parsed: {len(df)} rows x {len(df.columns)} cols")
                    except Exception as e:
                        print(f"   [WARN] BeautifulSoup parsing failed: {e}")
                
                # Strategy 3: Extract div lists
                if df is None:
                    print("[STRATEGY] Strategy 3: Div/list extraction...")
                    try:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        df = self._extract_from_div_lists(soup)
                        if df is not None:
                            print(f"[DIV] Extracted: {len(df)} rows x {len(df.columns)} cols")
                    except Exception as e:
                        print(f"   [WARN] Div extraction failed: {e}")
                
                if df is not None and len(df) > 0:
                    df = self.clean_scraped_data(df)
                    print(f"[SUCCESS] Scraping successful!")
                    return df
                
                print(f"[RETRY] No valid data found, retrying...")
                time.sleep(2)
                
            except requests.exceptions.Timeout:
                print(f"[TIMEOUT] Request timeout on attempt {attempt + 1}")
                time.sleep(3)
            except requests.exceptions.ConnectionError:
                print(f"[NETWORK] Connection error on attempt {attempt + 1}")
                time.sleep(3)
            except Exception as e:
                print(f"[ERROR] Unexpected error on attempt {attempt + 1}: {e}")
                time.sleep(2)
        
        print("[FAILED] Scraping failed after all attempts")
        return None
    
    def _parse_html_table(self, soup):
        """Parse HTML table element"""
        try:
            table = soup.find('table')
            if table is None:
                return None
            
            headers = []
            rows = []
            
            thead = table.find('thead')
            if thead:
                for th in thead.find_all('th'):
                    headers.append(th.get_text(strip=True))
            else:
                first_row = table.find('tr')
                if first_row:
                    for th in first_row.find_all(['th', 'td']):
                        headers.append(th.get_text(strip=True))
            
            tbody = table.find('tbody') or table
            for tr in tbody.find_all('tr')[1 if not thead else 0:]:
                row = []
                for td in tr.find_all(['td', 'th']):
                    row.append(td.get_text(strip=True))
                if row:
                    rows.append(row)
            
            if rows and headers:
                df = pd.DataFrame(rows, columns=headers)
                return df
            
            return None
        except Exception as e:
            print(f"[ERROR] Error parsing table: {e}")
            return None
    
    def _extract_from_div_lists(self, soup):
        """Extract data dari struktur div/list"""
        try:
            data = []
            selectors = ['div.item', 'div.card', 'div.product', 'article', 'li.item', 'li.result']
            
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    for item in items:
                        row = {}
                        for elem in item.find_all(['p', 'span', 'a', 'h2', 'h3']):
                            text = elem.get_text(strip=True)
                            if text:
                                row[elem.name] = text
                        
                        if row:
                            data.append(row)
                    
                    if data:
                        df = pd.DataFrame(data)
                        return df
            
            return None
        except Exception as e:
            print(f"[ERROR] Error extracting divs: {e}")
            return None
    
    def clean_scraped_data(self, df):
        """Bersihkan dan standardize data hasil scraping - IMPROVED VERSION"""
        if df is None or len(df) == 0:
            print("[CLEAN] DataFrame kosong, return None")
            return None
        
        print(f"[CLEAN] Starting data cleaning... (input: {len(df)} rows x {len(df.columns)} cols)")
        
        # Remove completely empty columns
        df = df.dropna(axis=1, how='all')
        df = df.loc[:, df.astype(str).ne('').any()]
        
        # Remove completely empty rows
        df = df.dropna(axis=0, how='all')
        df = df[df.astype(str).ne('').any(axis=1)]
        
        # Clean column names
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(r'[\n\r\t]', ' ', regex=True)
        
        # Handle duplicate column names
        if df.columns.duplicated().any():
            cols = pd.Series(df.columns)
            for dup in cols[cols.duplicated()].unique():
                dups = cols[cols == dup].index.tolist()
                for i, idx in enumerate(dups):
                    df.columns.values[idx] = f"{dup}_{i}"
                print(f"[WARN] Duplicate column renamed: {dup}")
        
        # Clean string columns
        for col in df.columns:
            try:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.strip()
                    # Replace 'nan' string dengan NaN asli
                    df[col] = df[col].replace(['nan', 'None', '', 'N/A', 'n/a'], np.nan)
            except Exception as e:
                print(f"[WARN] Error cleaning column {col}: {e}")
        
        # Reset index
        df = df.reset_index(drop=True)
        
        # Apply column mapping
        print("[MAP] Applying column mapping...")
        df = self.map_columns(df)
        
        # Create synthetic columns jika ada yang missing
        df = self.create_synthetic_columns(df)
        
        # Extract coordinates
        print("[COORDS] Extracting coordinates...")
        df = self.extract_coordinates(df)
        
        # Validate rating column jika ada
        if 'rating' in df.columns:
            try:
                df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
                # Set rating > 5 atau < 0 menjadi NaN (invalid)
                df.loc[(df['rating'] > 5) | (df['rating'] < 0), 'rating'] = np.nan
                print(f"[CLEAN] Rating column validated: {df['rating'].notna().sum()} valid values")
            except Exception as e:
                print(f"[WARN] Error validating rating: {e}")
        
        # Validate harga column jika ada
        if 'harga' in df.columns:
            try:
                df['harga'] = pd.to_numeric(df['harga'], errors='coerce')
                # Set harga < 0 menjadi NaN (invalid)
                df.loc[df['harga'] < 0, 'harga'] = np.nan
                print(f"[CLEAN] Price column validated: {df['harga'].notna().sum()} valid values")
            except Exception as e:
                print(f"[WARN] Error validating price: {e}")
        
        # Remove duplicate rows berdasarkan 'nama' dan 'provinsi' jika ada
        if 'nama' in df.columns and 'provinsi' in df.columns:
            original_len = len(df)
            df = df.drop_duplicates(subset=['nama', 'provinsi'], keep='first')
            if len(df) < original_len:
                print(f"[CLEAN] Removed {original_len - len(df)} duplicate records")
        
        print(f"[OK] Data cleaned: {len(df)} rows x {len(df.columns)} cols")
        
        if len(df) == 0:
            print("[WARN] Data kosong setelah cleaning!")
            return None
        
        return df
    
    def map_columns(self, df):
        """Map kolom generic ke kolom standar untuk pariwisata - EXTENDED VERSION"""
        column_mapping = {
            'nama': [
                'name', 'destinasi', 'tempat', 'lokasi', 'wisata', 'objek', 'attraction',
                'title', 'site name', 'place', 'destination', 'nama tempat', 'object',
                'attraction name', 'site', 'location name', 'nama lokasi'
            ],
            'provinsi': [
                'province', 'provinsi', 'state', 'region', 'daerah', 'country',
                'negara', 'country/region', 'area', 'province/state', 'administrative region',
                'location', 'wilayah', 'negara/region', 'state/region'
            ],
            'kota': [
                'city', 'kota', 'kabupaten', 'kab/kota', 'kota/kab', 'town',
                'municipality', 'district', 'kecamatan', 'locality', 'city/town',
                'kota/kabupaten'
            ],
            'kategori': [
                'category', 'kategori', 'tipe', 'type', 'jenis', 'kind', 'classification',
                'site category', 'attraction type', 'category type', 'classification type',
                'kategori wisata', 'jenis wisata'
            ],
            'rating': [
                'rating', 'nilai', 'score', 'review', 'rank', 'rate', 'stars',
                'elevation', 'height', 'grade', 'nilai rating'
            ],
            'harga': [
                'price', 'harga', 'biaya', 'cost', 'tarif', 'admission', 'fee',
                'entry fee', 'entrance fee', 'ticket price', 'biaya masuk'
            ],
            'deskripsi': [
                'description', 'deskripsi', 'keterangan', 'detail', 'remarks',
                'notes', 'info', 'information', 'catatan', 'penjelasan', 'info detail'
            ],
        }
        
        mapped_cols = {}
        
        for standard_col, possible_names in column_mapping.items():
            for col in df.columns:
                col_lower = col.lower().strip()
                # Check exact match or partial match
                if col_lower in possible_names or any(pn in col_lower for pn in possible_names if len(pn) > 2):
                    if standard_col not in df.columns:
                        mapped_cols[col] = standard_col
                        break
        
        # Apply mappings
        if mapped_cols:
            df = df.rename(columns=mapped_cols)
            print(f"[MAP] Mapped {len(mapped_cols)} columns: {mapped_cols}")
        
        return df
    
    def create_synthetic_columns(self, df):
        """Create synthetic columns jika kolom penting tidak ada"""
        print("[SYNTHETIC] Creating synthetic columns if missing...")
        
        # Jika tidak ada kategori, coba extract dari nama atau buat default
        if 'kategori' not in df.columns:
            kategori_keywords = {
                'beach': ['beach', 'pantai', 'laut', 'sea', 'coast', 'shore'],
                'mountain': ['mountain', 'gunung', 'peak', 'alpine', 'hiking'],
                'temple': ['temple', 'candi', 'shrine', 'pagoda', 'religious'],
                'museum': ['museum', 'gallery', 'art', 'historical'],
                'city': ['city', 'kota', 'town', 'urban', 'metropolitan'],
                'nature': ['park', 'forest', 'nature', 'hutan', 'taman', 'alam'],
                'water': ['lake', 'danau', 'waterfall', 'air terjun', 'geyser'],
            }
            
            categories = []
            nama_col = 'nama' if 'nama' in df.columns else None
            
            for idx, row in df.iterrows():
                cat = 'Attraction'
                if nama_col:
                    text = str(row[nama_col]).lower()
                    for category, keywords in kategori_keywords.items():
                        if any(kw in text for kw in keywords):
                            cat = category.title()
                            break
                categories.append(cat)
            
            df['kategori'] = categories
            print(f"[SYNTHETIC] Created 'kategori' column with {len(set(categories))} categories")
        
        # Jika tidak ada rating, buat default
        if 'rating' not in df.columns:
            df['rating'] = np.nan
            print("[SYNTHETIC] Created 'rating' column (empty)")
        
        # Jika tidak ada kota, buat default dari provinsi
        if 'kota' not in df.columns and 'provinsi' in df.columns:
            df['kota'] = df['provinsi'].apply(lambda x: str(x).split(',')[0].strip() if pd.notna(x) else 'Unknown')
            print("[SYNTHETIC] Created 'kota' column from 'provinsi'")
        
        return df
    
    def extract_coordinates(self, df):
        """Extract atau generate koordinat otomatis - IMPROVED VERSION"""
        if df is None or len(df) == 0:
            return None
        
        print("[COORDS] Extracting/generating coordinates...")
        
        # Complete and CORRECTED coordinates untuk 34 provinsi Indonesia
        # Dikoreksi untuk akurasi geografis maksimal (lat/lon dari geographic center setiap provinsi)
        province_coords = {
            'Aceh': (5.2, 96.0),  # FIXED: Aceh di FAR NORTH (bukan -5)
            'Sumatera Utara': (2.5, 99.0),  # Dikoreksi
            'Sumatera Barat': (-0.5, 100.5),  # Dikoreksi
            'Riau': (0.25, 101.5),  # Dikoreksi
            'Jambi': (-1.5, 102.7),  # Tetap baik
            'Sumatera Selatan': (-3.2, 104.7),  # Tetap baik
            'Bengkulu': (-3.8, 102.1),  # Dikoreksi
            'Lampung': (-4.5, 105.3),  # Tetap baik
            'Kepulauan Bangka Belitung': (-2.7, 107.6),  # Dikoreksi
            'Kepulauan Riau': (0.8, 101.7),  # Dikoreksi
            'DKI Jakarta': (-6.2, 106.8),  # Tetap baik
            'Jawa Barat': (-6.9, 107.5),  # Tetap baik
            'Jawa Tengah': (-7.5, 110.4),  # Tetap baik
            'DI Yogyakarta': (-7.8, 110.4),  # Tetap baik
            'Daerah Istimewa Yogyakarta': (-7.8, 110.4),  # Tetap baik
            'Jawa Timur': (-7.3, 112.8),  # Tetap baik
            'Banten': (-6.3, 106.2),  # Dikoreksi
            'Bali': (-8.7, 115.2),  # Tetap baik
            'Nusa Tenggara Barat': (-8.5, 117.3),  # Tetap baik
            'Nusa Tenggara Timur': (-8.7, 121.0),  # Tetap baik
            'Kalimantan Barat': (0.0, 111.5),  # FIXED: Center point di equator
            'Kalimantan Tengah': (-1.7, 113.3),  # Tetap baik
            'Kalimantan Selatan': (-3.5, 114.7),  # Tetap baik
            'Kalimantan Timur': (0.5, 116.5),  # Tetap baik
            'Kalimantan Utara': (4.0, 117.6),  # Tetap baik
            'Sulawesi Utara': (1.5, 124.7),  # Tetap baik
            'Sulawesi Tengah': (-1.5, 120.8),  # Dikoreksi
            'Sulawesi Selatan': (-5.5, 120.0),  # FIXED: Dikoreksi dari -5.1477
            'Sulawesi Tenggara': (-4.3, 122.5),  # Tetap baik
            'Gorontalo': (0.7, 122.5),  # Tetap baik
            'Sulawesi Barat': (-2.1, 119.3),  # Tetap baik
            'Maluku': (-3.2, 129.2),  # Tetap baik
            'Maluku Utara': (2.0, 128.0),  # FIXED: Adjusted untuk clarity (utara dari Maluku)
            'Papua': (-4.5, 138.2),  # Tetap baik
            'Papua Barat': (-1.9, 131.3),  # Tetap baik
        }
        
        # Extended tourism coordinates - lebih comprehensive
        tourism_coords = {
            'Bali': (-8.6705, 115.2126),
            'Yogyakarta': (-7.7956, 110.3688),
            'Bandung': (-6.9147, 107.6098),
            'Jakarta': (-6.2088, 106.8456),
            'Surabaya': (-7.2575, 112.7521),
            'Malang': (-7.9827, 112.6345),
            'Medan': (3.5952, 98.6722),
            'Pekanbaru': (0.5271, 101.4489),
            'Makassar': (-5.1477, 119.4327),
            'Semarang': (-6.9702, 110.4203),
            'Palembang': (-2.9081, 104.7549),
            'Banjarmasin': (-3.3243, 114.5971),
            'Pontianak': (-0.0263, 109.3425),
            'Samarinda': (-0.4917, 117.1431),
            'Manado': (1.4748, 124.8244),
            'Kendari': (-3.9701, 122.5137),
            'Ambon': (-3.6959, 128.1814),
            'Jayapura': (-2.5243, 140.6869),
            'Kupang': (-10.1698, 123.6231),
        }
        
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            df['latitude'] = np.nan
            df['longitude'] = np.nan
        
        # Try to get location columns
        location_cols = [col for col in df.columns 
                        if col.lower() in ['provinsi', 'kota', 'lokasi', 'nama', 'destinasi', 'province', 'city', 'location']]
        
        if not location_cols:
            print("[WARN] No location columns found")
            return df
        
        coords_added = 0
        
        for idx in df.index:
            # Skip jika sudah ada valid coordinates
            try:
                lat = pd.to_numeric(df.at[idx, 'latitude'], errors='coerce')
                lon = pd.to_numeric(df.at[idx, 'longitude'], errors='coerce')
                
                if pd.notna(lat) and pd.notna(lon) and -90 <= lat <= 90 and -180 <= lon <= 180:
                    continue
            except:
                pass
            
            # Try to match dengan tourism coordinates
            found = False
            for loc_col in location_cols:
                if found:
                    break
                    
                try:
                    location_text = str(df.at[idx, loc_col]).strip()
                    if not location_text or location_text.lower() == 'nan':
                        continue
                    
                    location_lower = location_text.lower()
                    
                    # First try tourism coordinates (more specific)
                    for place, coords in tourism_coords.items():
                        if place.lower() in location_lower:
                            df.at[idx, 'latitude'] = coords[0]
                            df.at[idx, 'longitude'] = coords[1]
                            found = True
                            coords_added += 1
                            break
                    
                    # Then try province coordinates (more general)
                    # Sort by length descending to match longer names first (e.g., 'Maluku Utara' before 'Maluku')
                    if not found:
                        sorted_provinces = sorted(province_coords.items(), key=lambda x: len(x[0]), reverse=True)
                        for prov, coords in sorted_provinces:
                            if prov.lower() in location_lower:
                                df.at[idx, 'latitude'] = coords[0]
                                df.at[idx, 'longitude'] = coords[1]
                                found = True
                                coords_added += 1
                                break
                except Exception as e:
                    print(f"[WARN] Error processing row {idx}: {e}")
                    continue
        
        print(f"[OK] Coordinates added: {coords_added} rows")
        return df
    
    def validate_data(self, df):
        """Validate data untuk GIS mapping"""
        if df is None or len(df) == 0:
            return False
        
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            return False
        
        valid_coords = df[
            (df['latitude'].notna()) & 
            (df['longitude'].notna()) &
            (df['latitude'] >= -90) & 
            (df['latitude'] <= 90) &
            (df['longitude'] >= -180) & 
            (df['longitude'] <= 180)
        ]
        
        return len(valid_coords) > 0
    
    def save_to_csv(self, df, filename='data_pariwisata.csv'):
        """Save data ke CSV"""
        try:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"[SAVE] Data saved to: {filename}")
        except Exception as e:
            print(f"[ERROR] Error saving file: {e}")
    
    def get_statistics(self, df):
        """Get comprehensive statistics dari data"""
        if df is None or len(df) == 0:
            return {}
        
        stats = {
            'total_records': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'missing_values': df.isnull().sum().to_dict(),
            'data_quality': {},
        }
        
        # Calculate data quality untuk setiap kolom penting
        important_cols = ['nama', 'provinsi', 'kategori', 'rating', 'latitude', 'longitude']
        for col in important_cols:
            if col in df.columns:
                total = len(df)
                non_null = df[col].notna().sum()
                completeness = (non_null / total * 100) if total > 0 else 0
                stats['data_quality'][col] = {
                    'total': total,
                    'non_null': non_null,
                    'completeness': completeness,
                }
        
        # Kategori distribution
        if 'kategori' in df.columns:
            stats['kategori_distribution'] = df['kategori'].value_counts().to_dict()
        
        # Provinsi distribution
        if 'provinsi' in df.columns:
            stats['provinsi_distribution'] = df['provinsi'].value_counts().to_dict()
        
        # Rating statistics
        if 'rating' in df.columns:
            try:
                rating_numeric = pd.to_numeric(df['rating'], errors='coerce')
                stats['rating_stats'] = {
                    'avg': float(rating_numeric.mean()),
                    'min': float(rating_numeric.min()),
                    'max': float(rating_numeric.max()),
                    'median': float(rating_numeric.median()),
                }
            except:
                pass
        
        # Coordinate validation
        if 'latitude' in df.columns and 'longitude' in df.columns:
            valid_coords = self.validate_coordinates(df).sum()
            stats['coordinate_validation'] = {
                'total': len(df),
                'valid': valid_coords,
                'invalid': len(df) - valid_coords,
                'valid_percentage': (valid_coords / len(df) * 100) if len(df) > 0 else 0,
            }
        
        return stats
    
    def get_data_accuracy_report(self, df):
        """Generate detailed accuracy report untuk data"""
        if df is None or len(df) == 0:
            return {}
        
        report = {
            'total_rows': len(df),
            'completeness_by_column': {},
            'data_quality_score': 0.0,
        }
        
        # Calculate completeness untuk setiap kolom
        for col in df.columns:
            total = len(df)
            non_null = df[col].notna().sum()
            completeness = (non_null / total * 100) if total > 0 else 0
            
            report['completeness_by_column'][col] = {
                'completeness_percent': round(completeness, 2),
                'filled': non_null,
                'missing': total - non_null,
            }
        
        # Overall data quality score (weighted)
        weights = {
            'nama': 0.20,
            'provinsi': 0.20,
            'kategori': 0.15,
            'rating': 0.15,
            'latitude': 0.15,
            'longitude': 0.15,
        }
        
        quality_scores = []
        for col, weight in weights.items():
            if col in report['completeness_by_column']:
                completeness = report['completeness_by_column'][col]['completeness_percent']
                quality_scores.append(completeness * weight)
        
        report['data_quality_score'] = round(sum(quality_scores), 2)
        
        return report
    
    @staticmethod
    def validate_coordinates(df):
        """Validate dan tentukan jika coordinate valid"""
        if 'latitude' not in df.columns or 'longitude' not in df.columns:
            return pd.Series(False, index=df.index)
        
        return (
            (df['latitude'].notna()) &
            (df['longitude'].notna()) &
            (df['latitude'] >= -90) &
            (df['latitude'] <= 90) &
            (df['longitude'] >= -180) &
            (df['longitude'] <= 180)
        )
