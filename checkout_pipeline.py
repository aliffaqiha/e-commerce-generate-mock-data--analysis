import streamlit as st
import pandas as pd
import random
import plotly.express as px
import time
import io

st.set_page_config(page_title="E-Commerce Real-Time Simulation Engine", layout="wide")

# Konfigurasi Tema Utama (Hijau & Putih) dan Pembersihan Font / Komponen
st.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700&display=swap');
        * { font-family: 'Plus Jakarta Sans', sans-serif; }
        .stApp { background-color: #ffffff; }
        
        /* Modifikasi Card Metric */
        div[data-testid="stMetric"] {
            background-color: #f8fafc !important;
            padding: 1.5rem !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            border: 1px solid #e2e8f0 !important;
            border-top: 4px solid #059669 !important;
        }
        div[data-testid="stMetricLabel"] { color: #475569 !important; font-size: 0.85rem !important; font-weight: 700 !important; text-transform: uppercase; letter-spacing: 0.05em; }
        div[data-testid="stMetricValue"] { color: #0f172a !important; font-size: 1.85rem !important; font-weight: 700 !important; }
        
        /* Control Box Style */
        .control-box {
            background-color: #f8fafc;
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            margin-bottom: 1.5rem;
        }

        div[data-testid="stTable"] td, div[data-testid="stDataFrame-stTable"] td, .stDataFrame div div div div {
            white-space: pre-line !important;
            vertical-align: top !important;
        }
        
        /* Gaya Navigasi Tab */
        button[data-baseweb="tab"] {
            font-size: 15px !important;
            font-weight: 600 !important;
            color: #64748b !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #059669 !important;
        }
        div[data-baseweb="tab-highlight"] {
            background-color: #059669 !important;
        }
        
        /* Sidebar Styling */
        .sidebar-title {
            font-size: 12px;
            font-weight: 700;
            color: #059669;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 12px;
            margin-top: 16px;
        }
        .sidebar-divider {
            border-bottom: 1px solid #e2e8f0;
            margin: 16px 0;
        }
    </style>
""")

# INITIALIZATION STATE
if "catalog" not in st.session_state:
    random.seed(42)
    
    warna_pool = [
        "Jet Black", "Broken White", "Midnight Navy", "Charcoal Grey", "Olive Drab",
        "Khaki Tan", "Burgundy Maroon", "Spiced Mustard", "Soft Beige", "Terracotta Clay",
        "Pastel Lilac", "Sage Green", "Acid Wash Denim", "Dusty Rose", "Emerald Green",
        "Ash Grey", "Camel Brown", "Navy Blue", "Cream Ivory", "Mint Green", "Ocean Blue"
    ]

    bahan_pool = [
        "Cotton Combed 24s", "Premium Fleece", "Linen Rayon", "Japanese Drill",
        "Sutra Sintetis", "Corduroy", "Faux Leather", "Denim Selvedge", "Dry-Fit Polyester",
        "Baby Terry", "Knit Premium", "Twill Stretch", "Chiffon", "Canvas Premium"
    ]

    aksen_pool = [
        "Oversized Style", "Slim-Fit Cut", "Regular Drop", "Vintage Wash",
        "Minimalist Unlined", "Multi-Pocket Cargo", "Distressed Ripped", "Classic Stripes",
        "High-Waist Design", "Korean Street Look", "Drop Shoulder", "Breathable Mesh",
        "Waterproof Zipper", "Ribbed Texture", "Button-Down Accent"
    ]

    katalog_dasar_ekstrem = [
        ("Kaos Oblong Crewneck", "Pria", 65000),
        ("Kemeja Kerah Shanghai", "Pria", 135000),
        ("Kemeja Flanel Kotak", "Pria", 125000),
        ("Kaos Polo Kerah", "Pria", 95000),
        ("Tshirt V-Neck Polos", "Pria", 60000),
        ("Kemeja Batik Cetak Modern", "Pria", 140000),
        ("Kemeja Kuban Pantai", "Pria", 110000),
        ("Blus Simpel Casual V-Neck", "Wanita", 85000),
        ("Gaun Panjang Maxi Dress", "Wanita", 260000),
        ("Crop Top Casual", "Wanita", 55000),
        ("Blouse Tunik Muslimah", "Wanita", 145000),
        ("Outer Cardigan Rajut", "Wanita", 120000),
        ("Tank Top Rib Premium", "Wanita", 45000),
        ("Midi Skirt Casual", "Wanita", 95000),
        ("Jaket Bomber Zipper", "Unisex", 245000),
        ("Jaket Hoodie Pullover", "Unisex", 195000),
        ("Blazer Kerja Kantor Elegant", "Wanita", 220000),
        ("Sweater Rajut Knitwear", "Unisex", 160000),
        ("Jaket Kulit Motorist", "Unisex", 520000),
        ("Jaket Denim Trucker", "Unisex", 210000),
        ("Jaket Coach Windbreaker", "Unisex", 185000),
        ("Cardigan Kimono Outer", "Unisex", 130000),
        ("Celana Denim Jeans", "Pria", 199000),
        ("Celana Chino Kerja Pants", "Pria", 155000),
        ("Celana Cargo Tactical", "Unisex", 175000),
        ("Celana Jogger Sporty Track", "Unisex", 130000),
        ("Legging Sport High-Waist", "Wanita", 95000),
        ("Celana Kulot Linen Loose-Fit", "Wanita", 145000),
        ("Rok Plisket Panjang Tutu", "Wanita", 110000),
        ("Celana Pendek Boardshorts", "Pria", 70000),
        ("Celana Bahan formal Trouser", "Pria", 185000),
        ("Hot Pants Denim", "Wanita", 80000),
        ("Sport Bra Stretch Active", "Wanita", 89000),
        ("Jersey Olahraga Running", "Unisex", 75000),
        ("Celana Training Trackpants", "Unisex", 115000),
        ("Kaos Singlet Gym Tank", "Pria", 55000),
        ("Sneakers Canvas Vulcanized", "Unisex", 235000),
        ("Sepatu Running Aerodynamic", "Unisex", 410000),
        ("Sepatu Pantofel Formal Loafers", "Pria", 380000),
        ("Sepatu Hak Tinggi High Heels", "Wanita", 295000),
        ("Sepatu Boots Kulit Kasar", "Unisex", 475000),
        ("Sandal Slide Kasual Santai", "Unisex", 45000),
        ("Sepatu Slip On Rajut", "Unisex", 135000),
        ("Sandal Gunung Outdoor", "Unisex", 110000),
        ("Topi Snapback Streetwear", "Unisex", 50000),
        ("Ikat Pinggang Kulit Buckle", "Pria", 75000),
        ("Kaos Kaki Cushion Pack", "Unisex", 30000),
        ("Tas Ransel Backpack Daily", "Unisex", 195000),
        ("Kacamata Hitam Polarized", "Unisex", 85000)
    ]

    fashion_pool = []
    for nama_dasar, gender, harga_base in katalog_dasar_ekstrem:
        jumlah_variasi = random.randint(30, 50)
        nama_terpakai = set()

        while len(nama_terpakai) < jumlah_variasi:
            warna = random.choice(warna_pool)
            bahan = random.choice(bahan_pool)
            aksen = random.choice(aksen_pool)
            nama_produk_lengkap = f"{nama_dasar} {aksen} ({bahan} - {warna})"

            if nama_produk_lengkap not in nama_terpakai:
                nama_terpakai.add(nama_produk_lengkap)
                faktor_acak = random.uniform(0.90, 1.10)
                harga_akhir = round(int(harga_base * faktor_acak), -3)
                
                fashion_pool.append({
                    "Nama Produk": nama_produk_lengkap,
                    "Target Konsumen": gender,
                    "Harga": harga_akhir
                })
                
    st.session_state.catalog = fashion_pool

if "db_log" not in st.session_state:
    st.session_state.db_log = []
if "db_sales" not in st.session_state:
    st.session_state.db_sales = []
if "user_carts" not in st.session_state:
    st.session_state.user_carts = {f"USER_{1000 + i}": {} for i in range(200)}
if "invoice_counter" not in st.session_state:
    st.session_state.invoice_counter = 900001
if "auto_loop_count" not in st.session_state:
    st.session_state.auto_loop_count = 0
if "engine_active" not in st.session_state:
    st.session_state.engine_active = False

# CORE LOGIC INJECTION ENGINE
def jalankan_suntik_data_otomatis():
    users = list(st.session_state.user_carts.keys())
    st.session_state.auto_loop_count += 1
    id_siklus = st.session_state.auto_loop_count
    
    target_sesi = random.randint(1, 50)
    k_aktual = min(target_sesi, len(users))
    active_users = random.sample(users, k=k_aktual)
    
    for user in active_users:
        pilihan_aksi = random.choices(["ADD_TO_CART", "CHECKOUT"], weights=[0.60, 0.40])[0]
        
        if pilihan_aksi == "ADD_TO_CART":
            produk = random.choice(st.session_state.catalog)
            qty = random.randint(1, 3)
            
            cart_saat_ini = st.session_state.user_carts[user]
            cart_saat_ini[produk["Nama Produk"]] = cart_saat_ini.get(produk["Nama Produk"], 0) + qty
            
            string_list_keranjang = "\n".join([f"• ({v}x) {k}" for k, v in cart_saat_ini.items()])
            
            st.session_state.db_log.append({
                "Siklus": id_siklus,
                "User ID": user,
                "Isi Keranjang Terkini": str(string_list_keranjang) if string_list_keranjang else "Kosong",
                "Jenis Aksi": "ADD_TO_CART",
                "Detail Eksekusi": f"Menambahkan ke keranjang: {qty}x {produk['Nama Produk']}"
            })
            
        elif pilihan_aksi == "CHECKOUT":
            cart_saat_ini = st.session_state.user_carts[user]
            
            if cart_saat_ini:
                invoice_id = f"INV-{st.session_state.invoice_counter}"
                st.session_state.invoice_counter += 1
                
                total_checkout_qty = 0
                total_invoice_harga = 0
                
                for prod_name, qty in list(cart_saat_ini.items()):
                    harga_satuan = next((p["Harga"] for p in st.session_state.catalog if p["Nama Produk"] == prod_name), 50000)
                    subtotal = harga_satuan * qty
                    
                    total_checkout_qty += qty
                    total_invoice_harga += subtotal
                    
                    st.session_state.db_sales.append({
                        "Invoice ID": invoice_id,
                        "Siklus": id_siklus,
                        "User ID": user,
                        "Nama Produk": prod_name,
                        "Harga Satuan": harga_satuan,
                        "Kuantitas": qty,
                        "Subtotal": subtotal
                    })
                
                st.session_state.user_carts[user] = {}
                
                st.session_state.db_log.append({
                    "Siklus": id_siklus,
                    "User ID": user,
                    "Isi Keranjang Terkini": "Kosong (Cleared)",
                    "Jenis Aksi": "CHECKOUT",
                    "Detail Eksekusi": f"Checkout {invoice_id}: Membayar bersih {total_checkout_qty} unit item. Total: Rp {total_invoice_harga:,}"
                })

if st.session_state.engine_active:
    jalankan_suntik_data_otomatis()

# MASTER DATA GENERATION
all_logs_df = pd.DataFrame(st.session_state.db_log)
all_sales_df = pd.DataFrame(st.session_state.db_sales)

# --- NAVBAR / SIDEBAR MANAGEMENT ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>Kontrol Sistem</div>", unsafe_allow_html=True)
    st.session_state.engine_active = st.toggle("Inject Data Otomatis", value=st.session_state.engine_active)
    
    if st.button("Kosongkan & Reset Simulasi", use_container_width=True):
        st.session_state.db_log = []
        st.session_state.db_sales = []
        st.session_state.user_carts = {f"USER_{1000 + i}": {} for i in range(200)}
        st.session_state.invoice_counter = 900001
        st.session_state.auto_loop_count = 0
        st.session_state.engine_active = False
        st.rerun()
        
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>Ekspor & Slicing Data</div>", unsafe_allow_html=True)
    
    # Penentuan batas siklus yang tersedia untuk ekspor
    max_siklus_tersedia = int(st.session_state.auto_loop_count)
    
    # PROTEKSI ERROR: Jika siklus masih 0 atau 1, amankan komponen slider
    if max_siklus_tersedia < 2:
        slider_min = 1
        slider_max = 2  # Dipaksa ke 2 agar min_value < max_value
        slider_val = (1, 1)
        slider_disabled = True
    else:
        slider_min = 1
        slider_max = max_siklus_tersedia
        slider_val = (1, max_siklus_tersedia)
        slider_disabled = False
    
    rentang_siklus = st.slider(
        "Slicing Urutan Siklus:",
        min_value=slider_min,
        max_value=slider_max,
        value=slider_val,
        disabled=slider_disabled
    )
    
    format_file = st.selectbox("Format Output:", options=["CSV", "Parquet"])
    
    # Filter dataset penjualan internal berdasarkan hasil slicing
    if not all_sales_df.empty:
        df_ekspor_terfilter = all_sales_df[(all_sales_df['Siklus'] >= rentang_siklus[0]) & (all_sales_df['Siklus'] <= rentang_siklus[1])]
    else:
        df_ekspor_terfilter = pd.DataFrame()

    # Logika pembuatan binary buffer file data download
    if format_file == "CSV":
        data_unduhan = df_ekspor_terfilter.to_csv(index=False).encode('utf-8')
        nama_file_output = "ecom_data.csv"
        mime_type_output = "text/csv"
    else:
        buffer_parquet = io.BytesIO()
        df_ekspor_terfilter.to_parquet(buffer_parquet, index=False)
        data_unduhan = buffer_parquet.getvalue()
        nama_file_output = "ecom_data.parquet"
        mime_type_output = "application/octet-stream"

    st.download_button(
        label=f"Unduh Berkas {format_file}",
        data=data_unduhan,
        file_name=nama_file_output,
        mime=mime_type_output,
        use_container_width=True,
        disabled=df_ekspor_terfilter.empty
    )
    if df_ekspor_terfilter.empty:
        st.caption("Tidak ada data transaksi pada rentang siklus terpilih.")

# --- INTERFACE UTAMA ---
st.title("User Shopping Activity Data Pipeline Engine")
st.markdown("Sistem simulasi penyuntikan data transaksi retail berbasis urutan aktivitas user (event-driven session stream).")

# Status Banner Kontrol
if st.session_state.engine_active:
    st.html("<div style='color: #059669; font-weight: 600; margin-bottom: 20px;'>Aktivitas: RUNNING (Data Mengalir Otomatis...)</div>")
else:
    st.html("<div style='color: #dc2626; font-weight: 600; margin-bottom: 20px;'>Aktivitas: PAUSED (Mesin Berhenti)</div>")

# FILTER INTERFACE UTAMA (Tampilan Data Feed & Log)
if not all_logs_df.empty:
    list_opsi_siklus = ["Semua Siklus Waktu"]
    list_opsi_siklus.extend(sorted(list(all_logs_df['Siklus'].unique())))
    filter_siklus_terpilih = st.selectbox("Filter Tampilan Berdasarkan Periode:", options=list_opsi_siklus)
    
    if filter_siklus_terpilih != "Semua Siklus Waktu":
        df_log_filtered = all_logs_df[all_logs_df['Siklus'] == filter_siklus_terpilih]
        df_sales_filtered = all_sales_df[all_sales_df['Siklus'] == filter_siklus_terpilih] if not all_sales_df.empty else pd.DataFrame()
    else:
        df_log_filtered = all_logs_df
        df_sales_filtered = all_sales_df
else:
    df_log_filtered = pd.DataFrame()
    df_sales_filtered = pd.DataFrame()

# METRIKS INDIKATOR UTAMA
total_omset = df_sales_filtered['Subtotal'].sum() if not df_sales_filtered.empty else 0
total_item_terjual = df_sales_filtered['Kuantitas'].sum() if not df_sales_filtered.empty else 0
total_invoice_sukses = df_sales_filtered['Invoice ID'].nunique() if not df_sales_filtered.empty else 0

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric(label="TOTAL REVENUE / GMV", value=f"Rp {total_omset:,}")
col_m2.metric(label="TOTAL VOLUME ITEM TERJUAL", value=f"{total_item_terjual:,} pcs")
col_m3.metric(label="JUMLAH INVOICE DI-BAYAR", value=f"{total_invoice_sukses:,} Sukses")

st.markdown("---")

# STRUKTUR MENU UTAMA (TABULAR)
tab_log, tab_profiling, tab_fashion, tab_segmentasi = st.tabs([
    "Data Feed & Log Pipeline", 
    "Profiling Aktivitas Pelanggan", 
    "Analisis Preferensi Fashion", 
    "Segmentasi Pengeluaran User"
])

# TAB: DATA FEED & LOG PIPELINE
with tab_log:
    st.subheader("Log Alur Aktivitas User")
    if not df_log_filtered.empty:
        df_log_display = df_log_filtered[['Siklus', 'User ID', 'Isi Keranjang Terkini', 'Jenis Aksi', 'Detail Eksekusi']].sort_index(ascending=False)
        st.dataframe(
            df_log_display, use_container_width=True, hide_index=True,
            column_config={
                "Siklus": st.column_config.TextColumn("Periode", width="small"),
                "User ID": st.column_config.TextColumn("User ID", width="small"),
                "Isi Keranjang Terkini": st.column_config.TextColumn("Daftar Barang di Keranjang", width="large"),
                "Jenis Aksi": st.column_config.TextColumn("Aksi", width="medium"),
                "Detail Eksekusi": st.column_config.TextColumn("Keterangan Log System", width="large")
            }
        )
    else:
        st.info("Belum ada data aktivitas. Nyalakan saklar otomatisasi di panel samping.")

    st.subheader("Transaksi Masuk")
    if not df_sales_filtered.empty:
        df_sales_display = df_sales_filtered[['Invoice ID', 'Siklus', 'User ID', 'Nama Produk', 'Harga Satuan', 'Kuantitas', 'Subtotal']].sort_index(ascending=False)
        st.dataframe(
            df_sales_display, use_container_width=True, hide_index=True,
            column_config={
                "Invoice ID": st.column_config.TextColumn("Invoice ID"),
                "Harga Satuan": st.column_config.NumberColumn("Harga Satuan", format="Rp %d"),
                "Kuantitas": st.column_config.NumberColumn("Qty Terjual", format="%d pcs"),
                "Subtotal": st.column_config.NumberColumn("Subtotal Keluar", format="Rp %d")
            }
        )
    else:
        st.info("Belum ada transaksi finansial sukses.")

# TAB: PROFILING AKTIVITAS PELANGGAN
with tab_profiling:
    st.subheader("Analisis Profiling Interaksi & Konversi Pelanggan")
    
    if not all_logs_df.empty:
        col_prof1, col_prof2 = st.columns([4, 6])
        
        with col_prof1:
            total_atc = len(all_logs_df[all_logs_df['Jenis Aksi'] == "ADD_TO_CART"])
            total_co = len(all_logs_df[all_logs_df['Jenis Aksi'] == "CHECKOUT"])
            conversion_rate = (total_co / total_atc * 100) if total_atc > 0 else 0
            
            st.metric("Macro Conversion Rate Total (ATC -> CO)", f"{conversion_rate:.2f} %")
            
            df_action_count = all_logs_df['Jenis Aksi'].value_counts().reset_index()
            fig_actions = px.pie(df_action_count, values='count', names='Jenis Aksi', 
                                 color='Jenis Aksi', color_discrete_map={"ADD_TO_CART": "#a7f3d0", "CHECKOUT": "#059669"},
                                 hole=0.4, title="Komposisi Beban Event Aktivitas Keseluruhan")
            fig_actions.update_layout(template="plotly_white")
            st.plotly_chart(fig_actions, use_container_width=True)
            
        with col_prof2:
            st.markdown("**10 Pelanggan Paling Aktif**")
            df_user_activity = all_logs_df.groupby(['User ID', 'Jenis Aksi']).size().unstack(fill_value=0).reset_index()
            
            if "ADD_TO_CART" not in df_user_activity.columns: df_user_activity["ADD_TO_CART"] = 0
            if "CHECKOUT" not in df_user_activity.columns: df_user_activity["CHECKOUT"] = 0
            
            df_user_activity['Total Aktivitas'] = df_user_activity["ADD_TO_CART"] + df_user_activity["CHECKOUT"]
            df_user_activity = df_user_activity.sort_values(by='Total Aktivitas', ascending=False).head(10)
            
            st.dataframe(
                df_user_activity, use_container_width=True, hide_index=True,
                column_config={
                    "User ID": st.column_config.TextColumn("User ID"),
                    "ADD_TO_CART": st.column_config.NumberColumn("Jml Add To Cart"),
                    "CHECKOUT": st.column_config.NumberColumn("Jml Checkout"),
                    "Total Aktivitas": st.column_config.NumberColumn("Total Hit Konten")
                }
            )
    else:
        st.info("Membutuhkan data log untuk menganalisis profile perilaku pelanggan.")

# TAB: ANALISIS PREFERENSI FASHION
with tab_fashion:
    st.subheader("Tren Preferensi Atribut Fashion Pelanggan")
    
    if not all_sales_df.empty:
        def ekstrak_atribut(row):
            nama_mentah = row['Nama Produk']
            try:
                base_name = nama_mentah.split(" (")[0]
                part_attributes = nama_mentah.split(" (")[1].replace(")", "").split(" - ")
                return pd.Series([base_name, part_attributes[0], part_attributes[1]])
            except:
                return pd.Series([nama_mentah, "Lainnya", "Lainnya"])

        df_fashion_parsed = all_sales_df.copy()
        df_fashion_parsed[['Kategori Baju', 'Bahan Kain', 'Varian Warna']] = df_fashion_parsed.apply(ekstrak_atribut, axis=1)
        
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            st.markdown("**Model Pakaian Terfavorit**")
            df_model = df_fashion_parsed.groupby('Kategori Baju')['Kuantitas'].sum().reset_index().sort_values(by='Kuantitas', ascending=False)
            fig_model = px.bar(df_model, x='Kuantitas', y='Kategori Baju', orientation='h', color_discrete_sequence=['#059669'])
            fig_model.update_layout(template="plotly_white", showlegend=False, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_model, use_container_width=True)
            
        with col_f2:
            st.markdown("**Bahan Kain Paling Disukai**")
            df_bahan = df_fashion_parsed.groupby('Bahan Kain')['Kuantitas'].sum().reset_index()
            fig_bahan = px.pie(df_bahan, values='Kuantitas', names='Bahan Kain', color_discrete_sequence=px.colors.sequential.Greens_r)
            fig_bahan.update_layout(template="plotly_white")
            st.plotly_chart(fig_bahan, use_container_width=True)
            
        with col_f3:
            st.markdown("**Varian Warna Terlaris**")
            df_warna = df_fashion_parsed.groupby('Varian Warna')['Kuantitas'].sum().reset_index().sort_values(by='Kuantitas', ascending=False)
            fig_warna = px.bar(df_warna, x='Varian Warna', y='Kuantitas', color_discrete_sequence=['#34d399'])
            fig_warna.update_layout(template="plotly_white")
            st.plotly_chart(fig_warna, use_container_width=True)
    else:
        st.info("Preferensi gaya belanja fashion akan muncul setelah ada transaksi checkout finansial.")

# TAB: SEGMENTASI PENGELUARAN USER
with tab_segmentasi:
    st.subheader("Segmentasi Kelas Pengeluaran Pelanggan")
    
    if not all_sales_df.empty:
        df_monetary = all_sales_df.groupby('User ID')['Subtotal'].sum().reset_index()
        df_monetary.columns = ['User ID', 'Total Belanja']
        
        def tentukan_segmen(total):
            if total >= 1500000:
                return "Whale / Pelanggan Utama"
            elif total >= 500000:
                return "Core Buyer / Loyal"
            else:
                return "Budget Shopper / Strategis"
                
        df_monetary['Segmen Pengguna'] = df_monetary['Total Belanja'].apply(tentukan_segmen)
        
        col_seg1, col_seg2 = st.columns([6, 4])
        
        with col_seg1:
            st.markdown("**Tabel Klasifikasi Nilai Pelanggan (Akumulasi Sejarah)**")
            st.dataframe(
                df_monetary.sort_values(by='Total Belanja', ascending=False),
                use_container_width=True, hide_index=True,
                column_config={
                    "User ID": st.column_config.TextColumn("User ID"),
                    "Total Belanja": st.column_config.NumberColumn("Akumulasi Dana Belanja", format="Rp %d"),
                    "Segmen Pengguna": st.column_config.TextColumn("Kategori Segmen")
                }
            )
            
        with col_seg2:
            st.markdown("**Distribusi Komponen Pasar Pelanggan**")
            df_seg_count = df_monetary['Segmen Pengguna'].value_counts().reset_index()
            fig_seg = px.pie(df_seg_count, values='count', names='Segmen Pengguna', color='Segmen Pengguna',
                             color_discrete_map={
                                 "Whale / Pelanggan Utama": "#047857",
                                 "Core Buyer / Loyal": "#10b981",
                                 "Budget Shopper / Strategis": "#a7f3d0"
                             })
            fig_seg.update_layout(template="plotly_white")
            st.plotly_chart(fig_seg, use_container_width=True)
            
            with st.expander("Metodologi Ambang Batas Segmen (Rule-based Thresholds)"):
                st.markdown("""
                - **Whale / Utama**: Belanja kumulatif **>= Rp 1.500.000** (Kontributor profit terbesar).
                - **Core Buyer**: Belanja kumulatif **Rp 500.000 s/d Rp 1.499.000** (Pelanggan reguler setia).
                - **Budget Shopper**: Belanja kumulatif **< Rp 500.000** (Pelanggan sangat sensitif harga).
                """)
    else:
        st.info("Belum ada nominal dana terakumulasi. Jalankan simulasi untuk membentuk peta segmentasi pasar.")

# LIVE DATA REFRESH TICKER LOOP
if st.session_state.engine_active:
    time.sleep(3.0)
    st.rerun()