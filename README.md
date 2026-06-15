# Personal Mock E-Commerce Analytics Platform

Sebuah platform dashboard monitoring analitik *e-commerce* interaktif yang dibangun menggunakan **Streamlit**, **Pandas**, **NumPy**, dan **Plotly Express**. Aplikasi ini mengimplementasikan  *real-time data stream pipeline* dengan fitur dekorator inovatif `@st.fragment`, yang dipadukan dengan fitur segmentasi konsumen (*customer segmentation engine*) berbasis pembobotan matriks nilai kontribusi belanja (*scoring system*)

By **Alif Faqih**

---

## Fitur Utama Dashboard

* **Real-Time Data Stream**: Menggunakan dekorator penayangan parsial dari Streamlit (`@st.fragment(run_every=2)`) untuk menginjeksikan data simulasi transaksi secara berkala setiap 2 detik tanpa memicu muat ulang (*rerun*) pada keseluruhan halaman
* **Dual Export Data Pipeline**: Fasilitas ekspor data transaksi mentah hasil filter ke dalam dua jenis format berkas industri: **CSV** (berbasis teks terstruktur) dan **Parquet** (berbasis penyimpanan kolom biner berkinerja tinggi)
* **Multi Tab Report**: Pembagian sudut pandang analitik tingkat tinggi ke dalam 5 panel interaktif:
    * **Tren Runtun Waktu**: Memetakan omset fluktuasi harian berjalan serta beban volume transaksi operasional per jam kerja (*Hourly Load*)
    * **Analisis Behavior Pelanggan**: Menyajikan visualisasi proporsi sebaran klaster segmen dan sebaran distribusi kurir logistik pilihan
    * **Komoditas & Geospasial**: Peta sebaran spasial pendapatan regional (`px.scatter_geo`) dikombinasikan dengan ranking produk lokal terpopuler (`px.sunburst` dan `px.treemap`).
    * **Deteksi Gagal Beli**: Panel diagnosis *Root Cause Analysis* (RCA) untuk mengukur volume kebocoran finansial (*financial bleeding*) berdasarkan penyebab teknis kegagalan transaksi.
    * **Rangking & Rating Teratas**: Papan peringkat strategis yang memuat daftar 10 konsumen loyal, 10 produk terlaris, dan 10 ptoduk rating terbaik.
* **Live Audit Log**: Menyediakan tabel live data (*Live Transaction Audit Log*) untuk keperluan verifikasi kepatuhan data seketika.

---

## Arsitektur & Spesifikasi Teknologi

* **Interface**: Streamlit
* **Mesin Manipulasi Data**: Pandas & NumPy
* **Visualisasi**: Plotly Express & Plotly Graph Objects
* **Penyimpanan Status Sesi**: Streamlit Session State (`st.session_state`)
* **Format Berkas Ekspor**: CSV (`utf-8`) & Apache Parquet (via mesin pembantu `pyarrow` atau `fastparquet`)

---

## Sistem Penilaian & Klasterisasi Perilaku

Sistem dasbor ini membangun profil perilaku pelanggan secara dinamis menggunakan formula **Customer Score (0-100)** yang menggabungkan nilai akumulasi belanja (*Monetary Value*) dan tingkat keaktifan bertransaksi (*Frequency Value*):

$$\text{Customer Score} = \left( \frac{\text{Total Belanja Individual}}{\text{Maks. Total Belanja Populasi}} \times 70 \right) + \left( \frac{\text{Frekuensi Beli Individual}}{\text{Maks. Frekuensi Beli Populasi}} \times 30 \right)$$

Berdasarkan metrik skor dan data kurir di atas, pelanggan akan otomatis diklasifikasikan ke dalam salah satu dari 5 segmen aturan bisnis berikut:

1. **Whale**: Pelanggan dengan kontribusi nilai akumulasi belanja sangat tinggi ($> \text{Rp } 15.000.000$).
2. **Express Enthusiast**: Pelanggan dengan nilai belanja $> \text{Rp } 2.500.000$ dan secara konsisten memilih metode pengiriman instan (`Instant` / `Same Day`).
3. **Bulk Shopper**: Pelanggan grosir yang membeli barang dengan total kuantitas volume barang terbanyak ($\ge 20 \text{ unit}$).
4. **Discount Hunter**: Pelanggan yang nilai pemanfaatan potongan diskonnya melampaui $30\%$ dari total belanja kotor asli.
5. **Casual Buyer**: Pelanggan umum ritel yang tidak memenuhi kriteria empat klasifikasi di atas.

---
## Panduan Eksekusi
1. **Kloning Repositori**: 
git clone [https://github.com/username/mock-ecommerce-analytics.git](https://github.com/username/mock-ecommerce-analytics.git)
cd mock-ecommerce-analytics
2. **Virtual Environment** :
python -m venv venv
venv\Scripts\activate
3.  **Dependencies** : 
pip install -r requirements.txt
4. **Run Program** :
streamlit run analytics_stream_complete.py
        *atau*
python -m streamlit run analytics_stream_complete.py

## Flowchart
```mermaid
graph TD
    A([START]) --> B[Set Page Configuration & Inject Kustom CSS Layout]
    B --> C{Apakah st.session_state<br>'db_transaksi' sudah ada?}
    
    C -- Tidak --> D[Jalankan init_historical_data<br>Generate 250 Data Awal Bulan Mei 2026] --> E
    C -- Ya --> E[Muat Data dari Sesi Master db_transaksi]
    
    E --> F[Render Sidebar UI:<br>Tombol Reset, Slicer Ekspor, Filter Wilayah & Tanggal]
    F --> G[Deteksi Interaksi Sidebar]
    
    G --> G1{Apakah Tombol<br>Reset Ditekan?}
    G1 -- Ya --> G2[Bersihkan & Inisialisasi Ulang Sesi Data] --> B
    
    G1 -- Tidak --> G3{Apakah Tombol<br>Unduh Ditekan?}
    G3 -- Ya --> G4[Saring Data & Konversi ke CSV / Parquet] --> G5([Unduh File Selesai])
    
    G3 -- Tidak --> H[Masuk ke Area Fragment Kontainer:<br>@st.fragment run_every=2]
    
    H --> H1{Apakah Pipa Data<br>Stream Aktif?}
    H1 -- Ya --> H2[Jalankan inject_high_scale_stream<br>Injeksi 0 s/d 30 Transaksi Acak Baru] --> H3
    H1 -- Tidak --> H3[Set Transaksi Baru Masuk = 0]
    
    H3 --> I[Saring Salinan Data Master Berdasarkan Filter Global Wilayah & Rentang Waktu]
    I --> J[Hitung Metrik Finansial & Jalankan Fungsi<br>calculate_advanced_behavior_and_scoring]
    
    J --> K[Render Kartu KPI Ekeskutif:<br>Jumlah Transaksi, Sukses, Total GMV, Data Baru]
    K --> L[Render 5 Tab Visualisasi Analitik Interaktif Plotly:<br>Tren Waktu, Behavior, Spasial, RCA Gagal, Ranking]
    L --> M[Render Live Transaction Audit Log & Master Stream Log]
    
    M --> N[Tunggu Siklus Penyegaran Fragment Berikutnya: 2 Detik] --> H