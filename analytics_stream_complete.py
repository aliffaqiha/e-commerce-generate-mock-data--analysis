import streamlit as st
import pandas as pd
import numpy as np
import datetime
import random
import plotly.express as px
import io

st.set_page_config(page_title="Personal Mock E-Commerce Analytics Platform", layout="wide")

WARNA_TEMA = ['#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', '#eff6ff']
WARNA_GAGAL = ['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd']

MAP_WARNA_SEGMEN = {
    'Whale': '#1e3a8a',
    'Express Enthusiast': '#1e40af',
    'Bulk Shopper': '#3b82f6',
    'Discount Hunter': '#60a5fa',
    'Casual Buyer': '#93c5fd'
}

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    .main .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; background-color: #ffffff; }
    body, p, div, h1, h2, h3, h4, h5, h6 { font-family: 'Plus Jakarta Sans', sans-serif !important; }

    .dashboard-header {
        background: #1e40af;
        padding: 24px 32px;
        border-radius: 12px;
        margin-bottom: 24px;
        border: 1px solid #1d4ed8;
    }
    .dashboard-title { color: #ffffff; margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.5px; }
    .dashboard-subtitle { color: #93c5fd; margin: 6px 0 0 0; font-size: 14px; font-weight: 400; }

    .kpi-card {
        background: #ffffff; padding: 24px 20px; border-radius: 12px;
        border: 1px solid #e2e8f0; transition: all 0.2s ease;
    }
    .kpi-card:hover { border-color: #3b82f6; box-shadow: 0 4px 12px rgb(30 64 175 / 0.05); }
    .kpi-value { font-size: 28px; font-weight: 700; color: #1e40af; letter-spacing: -0.5px; line-height: 1; }
    .kpi-label { font-size: 11px; color: #64748b; font-weight: 600; text-transform: uppercase; margin-top: 8px; letter-spacing: 0.5px; }

    .section-title { font-size: 16px; font-weight: 700; color: #1e40af; margin-bottom: 16px; margin-top: 8px; }
    .section-subtitle { font-size: 13px; font-weight: 500; color: #3b82f6; margin-top: 16px; margin-bottom: 8px; }

    .stTabs [data-baseweb="tab-list"] { gap: 4px; background-color: #f1f5f9; padding: 4px; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: transparent; border-radius: 6px; padding: 8px 16px; font-size: 13px; font-weight: 600; color: #64748b; border: none !important; transition: all 0.2s; }
    .stTabs [data-baseweb="tab"]:hover { background-color: #e2e8f0; color: #1e40af; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #1e40af !important; color: #ffffff !important; box-shadow: 0 1px 3px rgb(0 0 0 / 0.1) !important; }
    .stTabs [data-baseweb="tab-border-none"] { display: none; }
    
    .sidebar-section { border-bottom: 1px solid #e2e8f0; padding-bottom: 16px; margin-bottom: 16px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='dashboard-header'>
        <h1 class='dashboard-title'>Personal Mock E-commerce Analytics Platform</h1>
        <p class='dashboard-subtitle'>Sistem monitoring analitik real-time komprehensif, performa kepuasan produk, dan matriks perilaku</p>
    </div>
""", unsafe_allow_html=True)

def generate_random_mei_datetime():
    hari_acak = random.randint(1, 30)
    jam_acak = random.randint(0, 23)
    menit_acak = random.randint(0, 59)
    detik_acak = random.randint(0, 59)
    return datetime.datetime(2026, 5, hari_acak, jam_acak, menit_acak, detik_acak)

def init_historical_data():
    waktu_list = [generate_random_mei_datetime() for _ in range(250)]
    status_pool = ['SUKSES', 'SUKSES', 'SUKSES', 'SUKSES', 'GAGAL']
    alasan_pool = ['Stok Habis (Out of Stock)', 'Saldo Dompet Digital Tidak Cukup', 'Payment Gateway Timeout', 'Dibatalkan oleh Pengguna']

    batch = {
        'waktu': waktu_list,
        'user_id': [f"USER_{random.randint(1001, 1750)}" for _ in range(250)],
        'produk': np.random.choice(['Kopi Susu Literan', 'Kaos Polos Premium', 'Serum Wajah', 'Oli Motor Sintetis', 'Beras Premium Flores 5kg'], size=250),
        'kategori': np.random.choice(['Kuliner', 'Fashion', 'Kecantikan', 'Otomotif & Hobi', 'Sembako & Groceries'], size=250),
        'harga_satuan': np.random.randint(15000, 150000, size=250),
        'jumlah_beli': np.random.randint(1, 3, size=250),
        'nilai_diskon': np.random.randint(0, 5000, size=250),
        'daerah': np.random.choice(['Jabodetabek', 'Jawa Timur', 'Sumatera Utara', 'Sulawesi Selatan'], size=250),
        'metode_pengiriman': np.random.choice(['Instant', 'Same Day', 'Reguler', 'Kargo'], size=250),
        'status_transaksi': [random.choice(status_pool) for _ in range(250)]
    }

    df_init = pd.DataFrame(batch)
    df_init['total_bayar'] = (df_init['harga_satuan'] * df_init['jumlah_beli']) - df_init['nilai_diskon']
    df_init['alasan_gagal'] = df_init.apply(lambda r: random.choice(alasan_pool) if r['status_transaksi'] == 'GAGAL' else 'N/A', axis=1)
    df_init['bintang_review'] = df_init.apply(lambda r: random.randint(1, 5) if r['status_transaksi'] == 'SUKSES' else 0, axis=1)

    return df_init.sort_values(by='waktu', ascending=False).reset_index(drop=True)

if 'db_transaksi' not in st.session_state:
    st.session_state.db_transaksi = init_historical_data()
if 'trx_baru_masuk' not in st.session_state:
    st.session_state.trx_baru_masuk = 0

geo_coords = {
    'Jabodetabek': [-6.2088, 106.8456], 'Jawa Barat': [-6.9175, 107.6191], 'Jawa Tengah': [-7.0051, 110.4381],
    'Jawa Timur': [-7.2575, 112.7521], 'DI Yogyakarta': [-7.7956, 110.3695], 'Sumatera Utara': [3.5952, 98.6722],
    'Sumatera Selatan': [-2.9909, 104.7566], 'Sulawesi Selatan': [-5.1476, 119.4327], 'Kalimantan Timur': [-0.5022, 117.1536],
    'Bali & Nusra': [-8.4095, 115.1889], 'Maluku & Papua': [-2.5337, 140.7181]
}

def inject_high_scale_stream():
    jumlah_trx = random.randint(0, 30)
    st.session_state.trx_baru_masuk = jumlah_trx

    if jumlah_trx == 0:
        return

    pool_pengiriman = ['Instant', 'Same Day', 'Reguler', 'Kargo']
    status_pool = ['SUKSES', 'SUKSES', 'SUKSES', 'GAGAL']
    alasan_pool = ['Stok Habis (Out of Stock)', 'Saldo Dompet Digital Tidak Cukup', 'Payment Gateway Timeout', 'Dibatalkan oleh Pengguna']

    pool_produk = {
        'Gadget & Elektronik': [('iPhone 15 Pro Max', 22500000), ('Laptop Gaming ASUS ROG', 19500000), ('TWS Bass Booster', 350000)],
        'Fashion': [('Jaket Hoodie Oversize', 275000), ('Sepatu Sneakers Lokal', 399000)],
        'Skincare & Kosmetik': [('Serum Glowing', 139000), ('Sunscreen SPF 50', 85000)],
        'Sembako & Groceries': [('Beras Premium 5kg', 79000), ('Minyak Goreng 2L', 38000)]
    }

    batch = {k: [] for k in ['waktu', 'user_id', 'produk', 'kategori', 'harga_satuan', 'jumlah_beli', 'nilai_diskon', 'total_bayar', 'daerah', 'metode_pengiriman', 'status_transaksi', 'alasan_gagal', 'bintang_review']}
    for _ in range(jumlah_trx):
        kat = random.choice(list(pool_produk.keys()))
        prod, harga = random.choice(pool_produk[kat])
        daerah_pilihan = random.choice(list(geo_coords.keys()))
        status_trx = random.choice(status_pool)

        qty = random.randint(1, 3)
        subtotal = harga * qty
        potongan = int(subtotal * random.choice([0, 0.10]))

        batch['waktu'].append(generate_random_mei_datetime())
        batch['user_id'].append(f"USER_{random.randint(1001, 1750)}")
        batch['produk'].append(prod)
        batch['kategori'].append(kat)
        batch['harga_satuan'].append(harga)
        batch['jumlah_beli'].append(qty)
        batch['nilai_diskon'].append(potongan)
        batch['total_bayar'].append(subtotal - potongan)
        batch['daerah'].append(daerah_pilihan)
        batch['metode_pengiriman'].append(random.choice(pool_pengiriman))
        batch['status_transaksi'].append(status_trx)
        batch['alasan_gagal'].append(random.choice(alasan_pool) if status_trx == 'GAGAL' else 'N/A')
        batch['bintang_review'].append(random.randint(1, 5) if status_trx == 'SUKSES' else 0)

    df_batch = pd.DataFrame(batch)
    df_combined = pd.concat([st.session_state.db_transaksi, df_batch], ignore_index=True)
    st.session_state.db_transaksi = df_combined.sort_values(by='waktu', ascending=False).reset_index(drop=True)

def calculate_advanced_behavior_and_scoring(df_source):
    df_sukses = df_source[df_source['status_transaksi'] == 'SUKSES']
    if df_sukses.empty:
        return pd.DataFrame(columns=['user_id', 'total_belanja', 'total_qty', 'total_diskon', 'frekuensi_beli', 'customer_score', 'segmen_analisa'])

    user_profile = df_sukses.groupby('user_id').agg(
        total_belanja=('total_bayar', 'sum'),
        total_qty=('jumlah_beli', 'sum'),
        total_diskon=('nilai_diskon', 'sum'),
        frekuensi_beli=('produk', 'count'),
        pilihan_kurir=('metode_pengiriman', lambda x: x.mode()[0] if not x.mode().empty else 'Reguler')
    ).reset_index()

    max_spend = user_profile['total_belanja'].max() if user_profile['total_belanja'].max() > 0 else 1
    max_freq = user_profile['frekuensi_beli'].max() if user_profile['frekuensi_beli'].max() > 0 else 1
    user_profile['customer_score'] = (
        (user_profile['total_belanja'] / max_spend * 70) +
        (user_profile['frekuensi_beli'] / max_freq * 30)
    ).round(1)

    def segment_rule(row):
        if row['total_belanja'] > 15000000: return 'Whale'
        elif row['pilihan_kurir'] in ['Instant', 'Same Day'] and row['total_belanja'] > 2500000: return 'Express Enthusiast'
        elif row['total_qty'] >= 20: return 'Bulk Shopper'
        elif row['total_diskon'] > (row['total_belanja'] * 0.30): return 'Discount Hunter'
        else: return 'Casual Buyer'

    user_profile['segmen_analisa'] = user_profile.apply(segment_rule, axis=1)
    return user_profile

st.sidebar.markdown("<p style='font-size:12px; font-weight:700; color:#1e40af; text-transform:uppercase; letter-spacing:0.5px;'>Data Pipeline</p>", unsafe_allow_html=True)
mode_aktif = st.sidebar.toggle("Aktifkan Jalur Data Stream", value=True)

if st.sidebar.button("Reset Database Master", type="primary", use_container_width=True):
    st.session_state.db_transaksi = init_historical_data()
    st.session_state.trx_baru_masuk = 0
    st.toast("Database Berhasil Direset!")

st.sidebar.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:12px; font-weight:700; color:#1e40af; text-transform:uppercase; letter-spacing:0.5px;'>Unduh Data Berkas</p>", unsafe_allow_html=True)
dl_start, dl_end = st.sidebar.date_input("Slicing Tanggal Ekspor:", value=(datetime.date(2026, 5, 1), datetime.date(2026, 5, 30)), min_value=datetime.date(2026, 5, 1), max_value=datetime.date(2026, 5, 30), key="download_slicer")
format_ekspor = st.sidebar.selectbox("Format Ekspor Berkas:", options=["CSV", "Parquet"])

df_download_raw = st.session_state.db_transaksi.copy()
df_download_filtered = df_download_raw[(df_download_raw['waktu'].dt.date >= dl_start) & (df_download_raw['waktu'].dt.date <= dl_end)]

if format_ekspor == "CSV":
    buffer_data = df_download_filtered.to_csv(index=False).encode('utf-8')
    nama_berkas = "ecom_data.csv"
    tipe_mime = "text/csv"
else:
    buffer = io.BytesIO()
    df_download_filtered.to_parquet(buffer, index=False)
    buffer_data = buffer.getvalue()
    nama_berkas = "ecom_data.parquet"
    tipe_mime = "application/octet-stream"

st.sidebar.download_button(
    label=f"Unduh {format_ekspor}",
    data=buffer_data,
    file_name=nama_berkas,
    mime=tipe_mime,
    use_container_width=True
)

st.sidebar.markdown("<div class='sidebar-section'></div>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size:12px; font-weight:700; color:#1e40af; text-transform:uppercase; letter-spacing:0.5px;'>Filter Dashboard</p>", unsafe_allow_html=True)
pilihan_wilayah = st.sidebar.multiselect("Wilayah Operasional:", options=list(geo_coords.keys()), default=list(geo_coords.keys()))
rentang_waktu = st.sidebar.date_input("Rentang Waktu Laporan:", value=(datetime.date(2026, 5, 1), datetime.date(2026, 5, 30)), min_value=datetime.date(2026, 5, 1), max_value=datetime.date(2026, 5, 30), key="global_slicer")

@st.fragment(run_every=2)
def render_enterprise_dashboard():
    if mode_aktif:
        inject_high_scale_stream()
    else:
        st.session_state.trx_baru_masuk = 0

    df_raw = st.session_state.db_transaksi.copy()

    if isinstance(rentang_waktu, tuple) and len(rentang_waktu) == 2:
        start_date, end_date = rentang_waktu
        df_filtered = df_raw[(df_raw['waktu'].dt.date >= start_date) & (df_raw['waktu'].dt.date <= end_date)]
    else:
        df_filtered = df_raw

    if pilihan_wilayah:
        df_filtered = df_filtered[df_filtered['daerah'].isin(pilihan_wilayah)]

    df_sukses_full = df_filtered[df_filtered['status_transaksi'] == 'SUKSES']
    df_gagal_full = df_filtered[df_filtered['status_transaksi'] == 'GAGAL']
    df_user_metrics = calculate_advanced_behavior_and_scoring(df_filtered)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{len(df_filtered):,}</div><div class='kpi-label'>Jumlah Transaksi</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{len(df_sukses_full):,}</div><div class='kpi-label'>Transaksi Sukses</div></div>", unsafe_allow_html=True)
    with c3:
        total_revenue = df_sukses_full['total_bayar'].sum() if not df_sukses_full.empty else 0
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>Rp {total_revenue/1e6:.2f}M</div><div class='kpi-label'>Total GMV</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>+{st.session_state.trx_baru_masuk}</div><div class='kpi-label'>Transaksi Baru Masuk</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if df_filtered.empty:
        st.warning("Data kosong berdasarkan kriteria filter global saat ini.")
        return

    tab_waktu, tab_behavior, tab_geo, tab_gagal, tab_ranking = st.tabs([
        "Tren Runtun Waktu", "Analisis Behavior Pelanggan", "Komoditas & Geospasial", "Deteksi Gagal Beli", "Rangking & Rating Teratas"
    ])

    with tab_waktu:
        st.markdown("<div class='section-title'>Fluktuasi Penjualan Harian Berjalan</div>", unsafe_allow_html=True)
        df_sukses_full['hari'] = df_sukses_full['waktu'].dt.date
        rekap_waktu = df_sukses_full.groupby('hari')['total_bayar'].sum().reset_index().sort_values(by='hari')
        fig_line = px.line(rekap_waktu, x='hari', y='total_bayar', markers=True, template="plotly_white", color_discrete_sequence=['#1e40af'])
        fig_line.update_traces(line=dict(width=2), marker=dict(size=6, color='#1e1b4b'))
        fig_line.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=340, xaxis_title="Tanggal", yaxis_title="Omset Terbuku (Rp)")
        st.plotly_chart(fig_line, use_container_width=True)

        st.markdown("<div class='section-subtitle'>Analisis Beban Volume Transaksi Berdasarkan Jam Kerja (Hourly Load)</div>", unsafe_allow_html=True)
        df_filtered['jam'] = df_filtered['waktu'].dt.hour
        rekap_jam = df_filtered.groupby(['jam', 'status_transaksi']).size().reset_index(name='jumlah')
        fig_hourly = px.bar(rekap_jam, x='jam', y='jumlah', color='status_transaksi', color_discrete_map={'SUKSES': '#3b82f6', 'GAGAL': '#bfdbfe'}, barmode='group', template='plotly_white')
        fig_hourly.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=240, xaxis_title="Jam Operasional (00:00 - 23:00)", yaxis_title="Volume Transaksi", legend_title=None)
        st.plotly_chart(fig_hourly, use_container_width=True)

    with tab_behavior:
        st.markdown("<div class='section-title'>Klasterisasi Dominasi Karakter Transaksi Pelanggan</div>", unsafe_allow_html=True)
        b1, b2 = st.columns([1, 1.2])
        with b1:
            rekap_segmen = df_user_metrics['segmen_analisa'].value_counts().reset_index() if not df_user_metrics.empty else pd.DataFrame(columns=['segmen_analisa', 'count'])
            fig_pie = px.pie(rekap_segmen, names='segmen_analisa', values='count', hole=0.5, color='segmen_analisa', color_discrete_map=MAP_WARNA_SEGMEN, template="plotly_white")
            fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320, legend=dict(orientation="h", y=-0.15))
            st.plotly_chart(fig_pie, use_container_width=True)
        with b2:
            fig_box = px.box(df_user_metrics, x='segmen_analisa', y='total_belanja', color='segmen_analisa', color_discrete_map=MAP_WARNA_SEGMEN, template="plotly_white")
            fig_box.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=320, showlegend=False, xaxis_title=None, yaxis_title="Akumulasi Belanja Kontribusi (Rp)")
            st.plotly_chart(fig_box, use_container_width=True)

        st.markdown("<div class='section-subtitle'>Distribusi Preferensi Metode Pengiriman per Segmen Karakter</div>", unsafe_allow_html=True)
        if not df_sukses_full.empty:
            df_behavior_ship = calculate_advanced_behavior_and_scoring(df_filtered)
            df_ship_mix = df_sukses_full.merge(df_behavior_ship[['user_id', 'segmen_analisa']], on='user_id', how='left')
            rekap_ship_mix = df_ship_mix.groupby(['segmen_analisa', 'metode_pengiriman']).size().reset_index(name='total')
            fig_ship_bar = px.bar(rekap_ship_mix, x='total', y='segmen_analisa', color='metode_pengiriman', orientation='h', color_discrete_sequence=WARNA_TEMA, template='plotly_white')
            fig_ship_bar.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=240, xaxis_title="Jumlah Penggunaan Kurir", yaxis_title=None, legend_title=None)
            st.plotly_chart(fig_ship_bar, use_container_width=True)

    with tab_geo:
        st.markdown("<div class='section-title'>Sebaran Wilayah Penjualan & Komoditas Juara Lokal</div>", unsafe_allow_html=True)
        m1, m2 = st.columns([1, 1])
        with m1:
            rekap_geo = df_sukses_full.groupby('daerah')['total_bayar'].sum().reset_index()
            rekap_geo['lat'] = rekap_geo['daerah'].map(lambda x: geo_coords[x][0] if x in geo_coords else 0)
            rekap_geo['lon'] = rekap_geo['daerah'].map(lambda x: geo_coords[x][1] if x in geo_coords else 0)
            fig_map = px.scatter_geo(rekap_geo, lat='lat', lon='lon', text='daerah', size='total_bayar', color='total_bayar', color_continuous_scale='Blues', scope='asia', template="plotly_white")
            fig_map.update_geos(center=dict(lon=118.0, lat=-2.5), projection_scale=4.6, visible=False, showland=True, landcolor="#ffffff")
            fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=320, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)
        with m2:
            geo_product_rank = df_sukses_full.groupby(['daerah', 'produk'])['jumlah_beli'].sum().reset_index()
            geo_product_rank = geo_product_rank.sort_values(by=['daerah', 'jumlah_beli'], ascending=[True, False])
            fig_sunburst_geo = px.sunburst(geo_product_rank, path=['daerah', 'produk'], values='jumlah_beli', color='jumlah_beli', color_continuous_scale='Blues', template="plotly_white")
            fig_sunburst_geo.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=320)
            st.plotly_chart(fig_sunburst_geo, use_container_width=True)

        st.markdown("<div class='section-subtitle'>Pemetaan Kontribusi Pendapatan (GMV) antar Wilayah</div>", unsafe_allow_html=True)
        fig_tree_geo = px.treemap(rekap_geo, path=['daerah'], values='total_bayar', color='total_bayar', color_continuous_scale='Blues', template='plotly_white')
        fig_tree_geo.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=220)
        st.plotly_chart(fig_tree_geo, use_container_width=True)

    with tab_gagal:
        st.markdown("<div class='section-title' style='color:#1e40af;'>Root Cause Analysis & Financial Bleeding Monitor</div>", unsafe_allow_html=True)
        if df_gagal_full.empty:
            st.success("Luar biasa! Tidak ada transaksi gagal terdeteksi dalam filter ini.")
        else:
            g1, g2 = st.columns([1.2, 1])
            with g1:
                rekap_root_cause = df_gagal_full.groupby('alasan_gagal')['total_bayar'].agg(['count', 'sum']).reset_index()
                rekap_root_cause.columns = ['Alasan Gagal', 'Jumlah Kasus', 'Total Kerugian (Rp)']
                fig_fail_bar = px.bar(rekap_root_cause, x='Total Kerugian (Rp)', y='Alasan Gagal', orientation='h', color='Alasan Gagal', color_discrete_sequence=WARNA_GAGAL, template="plotly_white")
                fig_fail_bar.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, showlegend=False, yaxis_title=None)
                st.plotly_chart(fig_fail_bar, use_container_width=True)
            with g2:
                produk_gagal = df_gagal_full.groupby('produk')['jumlah_beli'].sum().reset_index().sort_values(by='jumlah_beli', ascending=False).head(5)
                fig_fail_donut = px.pie(produk_gagal, names='produk', values='jumlah_beli', hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r, template="plotly_white")
                fig_fail_donut.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=280, legend=dict(orientation="h", y=-0.1))
                st.plotly_chart(fig_fail_donut, use_container_width=True)

            st.markdown("<div class='section-subtitle' style='color:#1e40af;'>Klaster Kerugian Finansial Terhadap Lokasi Wilayah Geografis</div>", unsafe_allow_html=True)
            rekap_gagal_geo = df_gagal_full.groupby('daerah')['total_bayar'].sum().reset_index(name='total_kerugian')
            fig_fail_geo = px.scatter(rekap_gagal_geo, x='daerah', y='total_kerugian', size='total_kerugian', color='total_kerugian', color_continuous_scale='Blues', template='plotly_white')
            fig_fail_geo.update_layout(margin=dict(l=20, r=20, t=10, b=10), height=220, xaxis_title=None, yaxis_title="Kebocoran Dana (Rp)", coloraxis_showscale=False)
            st.plotly_chart(fig_fail_geo, use_container_width=True)

    with tab_ranking:
        st.markdown("<div class='section-title'>Papan Peringkat Strategis Korporasi</div>", unsafe_allow_html=True)
        l1, l2, l3 = st.columns([1.2, 0.9, 1.1])
        with l1:
            st.markdown("<p style='font-size:13px; font-weight:700; color:#1e40af; margin-bottom:12px;'>Top 10 Ranking Pelanggan (Scoring System 0-100)</p>", unsafe_allow_html=True)
            if not df_user_metrics.empty:
                top_users = df_user_metrics.sort_values(by='customer_score', ascending=False).head(10).reset_index(drop=True)
                top_users.index += 1
                top_users_display = top_users[['user_id', 'total_belanja', 'frekuensi_beli', 'customer_score']].copy()
                top_users_display['total_belanja'] = top_users_display['total_belanja'].apply(lambda x: f"Rp {x:,.0f}")
                st.dataframe(top_users_display, use_container_width=True)
            else:
                st.info("Belum ada data ranking.")
        with l2:
            st.markdown("<p style='font-size:13px; font-weight:700; color:#1e40af; margin-bottom:12px;'>Top 10 Produk Terlaris (Volume)</p>", unsafe_allow_html=True)
            if not df_sukses_full.empty:
                prod_sales = df_sukses_full.groupby('produk').agg(total_terjual=('jumlah_beli', 'sum')).reset_index().sort_values(by='total_terjual', ascending=False).head(10).reset_index(drop=True)
                prod_sales.index += 1
                st.dataframe(prod_sales, use_container_width=True)
        with l3:
            st.markdown("<p style='font-size:13px; font-weight:700; color:#1e40af; margin-bottom:12px;'>Top 10 Produk dengan Rata-rata Rating Terbaik</p>", unsafe_allow_html=True)
            if not df_sukses_full.empty:
                prod_rating = df_sukses_full.groupby('produk').agg(average_rating=('bintang_review', 'mean'), total_ulasan=('bintang_review', 'count')).reset_index().sort_values(by=['average_rating', 'total_ulasan'], ascending=[False, False]).head(10).reset_index(drop=True)
                prod_rating.index += 1
                prod_rating_display = prod_rating.copy()
                prod_rating_display['average_rating'] = prod_rating_display['average_rating'].apply(lambda x: f"{x:.2f} / 5.00")
                st.dataframe(prod_rating_display, use_container_width=True)

    st.markdown("<br><hr style='border-color:#e2e8f0;'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title' style='color:#475569; font-size:14px;'>Live Transaction Audit Log</div>", unsafe_allow_html=True)
    if not df_sukses_full.empty:
        st.dataframe(df_sukses_full[['waktu', 'user_id', 'produk', 'daerah', 'total_bayar', 'bintang_review']].head(8), use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.checkbox("Buka Pipa Log Master Stream Data (Kondisi Database Asli Tanpa Filter)"):
        st.dataframe(st.session_state.db_transaksi, use_container_width=True)

render_enterprise_dashboard()