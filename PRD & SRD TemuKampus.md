# DOKUMEN REKAYASA PERANGKAT LUNAK: TEMUKAMPUS

**Sistem Informasi Pelaporan Barang Hilang & Ditemukan Berbasis Web**  
*Lingkungan Kampus Universitas Negeri Surabaya (UNESA)*

---

# BAGIAN I: PRODUCT REQUIREMENT DOCUMENT (PRD)

## 1\. Ringkasan Eksekutif & Latar Belakang

**TemuKampus** adalah platform web terpusat yang dirancang untuk memfasilitasi pencatatan, penelusuran, dan pengembalian barang yang hilang atau ditemukan di lingkungan kampus. Sebelum adanya platform ini, pengumuman barang hilang dilakukan secara terfragmentasi melalui grup pesan instan (WhatsApp, Telegram) atau media sosial yang cepat tertimbun pesan lain.

TemuKampus menghadirkan antarmuka bertema *Autumn* yang hangat, modern, estetis (*glassmorphism*), dan kaya akan umpan balik visual tanpa mengorbankan performa sistem serta aksesibilitas pengguna.

---

## 2\. Tujuan Produk (Product Goals)

1. **Pemusatan Informasi:** Menyediakan repositori tunggal bagi barang yang hilang dan ditemukan dengan data yang terverifikasi dan rapi.  
2. **Kecepatan Komunikasi:** Menghubungkan penemu barang dan pemilik secara instan melalui tautan langsung ke WhatsApp.  
3. **Pengalaman Pengguna (UX Delight):** Menghadirkan kesan visual interaktif (intro sinematik, partikel musiman, latar dinamis) yang adaptif dan tetap ramah pengguna (*user-friendly*).  
4. **Keandalan Pelacakan Data:** Menyediakan indikator statistik real-time mengenai status barang (Hilang, Ditemukan, Selesai).

---

## 3\. Persona Pengguna (Target Audience)

* **Mahasiswa Pelapor Kehilangan:** Mahasiswa yang kehilangan barang berharga di area kampus dan membutuhkan sarana publikasi yang cepat, terstruktur, serta mudah dicari.  
* **Mahasiswa / Sivitas Penemu Barang:** Pihak yang menemukan barang tak bertuan dan ingin menyerahkannya kembali ke pemilik sah tanpa ribet mengelola kontak manual.  
* **Penguji / Dosen Penilai:** Penilai akademis yang menguji kesesuaian fungsionalitas CRUD, integrasi basis data, validasi input, serta kualitas desain antarmuka.

---

## 4\. Ruang Lingkup Fitur (Feature Scope)

### 4.1 Fungsionalitas Inti

| ID | Nama Fitur | Deskripsi | Kategori |
| :---- | :---- | :---- | :---- |
| F-01 | **Formulir Laporan** | Pengguna dapat menginput status (Hilang/Ditemukan), nama barang, lokasi, nomor WhatsApp, dan unggah foto opsional. | Core / Must-have |
| F-02 | **Papan Feed Laporan** | Menampilkan kartu laporan dengan badge status warna yang tegas dan foto barang. | Core / Must-have |
| F-03 | **Pencarian & Filter Cepat** | Pencarian berbasis teks (nama barang & lokasi) serta dropdown filter status laporan. | Core / Must-have |
| F-04 | **Statistik Mini Agregasi** | 3 kartu ringkasan di atas feed: Total Hilang, Total Ditemukan, dan Total Selesai/Kembali. | High Priority |
| F-05 | **Aksi Status Laporan** | Tombol untuk menandai barang telah selesai/kembali serta tombol hapus laporan dengan konfirmasi. | High Priority |
| F-06 | **Integrasi Kontak WA** | Tombol kontak langsung membuka aplikasi WhatsApp (`wa.me`) dengan draft pesan otomatis. | Core / Must-have |

### 4.2 Pengalaman Pengguna & Estetika (Delight Factors)

| ID | Nama Fitur | Deskripsi | Kategori |
| :---- | :---- | :---- | :---- |
| UX-01 | **Splash Screen Sinematik** | Layar intro ala Rockstar Games (Logo *T🍂*) yang muncul hanya sekali saat pertama membuka tab browser (`sessionStorage`), tersinkron dengan kesiapan render halaman. | Delight / UX |
| UX-02 | **Partikel Daun Musim Gugur** | Efek daun berguguran (`falling-leaf`) berbasis akselerasi GPU (CSS Animation) yang ringan dan tidak membebani interaksi klik. | Aesthetic |
| UX-03 | **Sakelar Efek (Accessibility)** | Tombol sakelar mini transparan (*glassmorphism*) di pojok kanan atas untuk mematikan/menyalakan efek daun, menyimpan status di `localStorage`. Status default: Aktif (ON). | Accessibility |
| UX-04 | **Slideshow Latar Halus** | Transisi pergantian latar belakang bertema *Autumn* secara berkala menggunakan teknik 2-layer crossfade tanpa kedip. | Aesthetic |
| UX-05 | **Empty State Informatif** | Tampilan visual tematik saat pencarian tidak membuahkan hasil agar layar tidak kosong melompong. | UI Polish |

---

## 5\. Metrik Keberhasilan (Success Metrics)

* Pengguna dapat menyelesaikan input laporan dalam waktu kurang dari 45 detik.  
* Navigasi pencarian dan pemfilteran berjalan instan tanpa interupsi splash screen berulang.  
* Lolos seluruh skenario uji fungsionalitas CRUD tanpa adanya galat HTTP 500\.

---

---

# BAGIAN II: SYSTEM REQUIREMENT DOCUMENT (SRD / SRS)

## 1\. Arsitektur Sistem & Spesifikasi Teknologi

### 1.1 Tech Stack

* **Sisi Server (Backend):** Python 3.x, Flask Web Framework.  
* **Sisi Klien (Frontend):** HTML5 Semantik, CSS3 Modern (Flexbox, Grid, Glassmorphism, Keyframe Animations), Vanilla JavaScript (ES6+).  
* **Basis Data (Database):** MySQL / MariaDB dengan driver penghubung `mysql-connector-python`.  
* **Protokol Eksternal:** WhatsApp Click-to-Chat API URI Scheme (`https://wa.me/`).

---

## 2\. Spesifikasi Basis Data (Database Schema)

### 2.1 Struktur Tabel `laporan`

```sql
CREATE DATABASE IF NOT EXISTS temukampus;
USE temukampus;

CREATE TABLE IF NOT EXISTS laporan (
    id_laporan INT AUTO_INCREMENT PRIMARY KEY,
    status_laporan ENUM('Hilang', 'Ditemukan', 'Selesai') NOT NULL DEFAULT 'Hilang',
    nama_barang VARCHAR(150) NOT NULL,
    lokasi VARCHAR(255) NOT NULL,
    nomor_wa VARCHAR(25) NOT NULL,
    foto_barang VARCHAR(255) DEFAULT 'default.png',
    tanggal_dibuat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 2.2 Kueri Agregasi Statistik Mini

Menggunakan teknik kueri agregasi efisien dengan `COALESCE` dan conditional summation:

```sql
SELECT 
    COALESCE(SUM(CASE WHEN status_laporan = 'Hilang' THEN 1 ELSE 0 END), 0) AS total_hilang,
    COALESCE(SUM(CASE WHEN status_laporan = 'Ditemukan' THEN 1 ELSE 0 END), 0) AS total_ditemukan,
    COALESCE(SUM(CASE WHEN status_laporan = 'Selesai' THEN 1 ELSE 0 END), 0) AS total_selesai
FROM laporan;
```

---

## 3\. Spesifikasi Kebutuhan Non-Fungsional (Non-Functional Requirements)

### 3.1 Kinerja (Performance)

* **Kesiapan Render Transisi:** Logika intro Rockstar terikat pada event listener `window.addEventListener('load')`, mencegah splash memudar saat aset di baliknya belum selesai dirender.  
* **Efisiensi Animasi:** Animasi daun (`@keyframes fallDown`) hanya memanipulasi properti `transform` dan `opacity` untuk memicu *hardware compositing* pada kartu grafis tanpa menyebabkan *layout reflow*.  
* **Batas Unggahan Berkas:** Backend membatasi payload unggahan maksimal $5 \text{ MB}$ (`app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024`) guna mencegah kejenuhan memori server.

### 3.2 Keamanan & Integritas Data (Security & Data Integrity)

* **Sanitasi File Upload:** Memvalidasi ekstensi file (`png`, `jpg`, `jpeg`, `webp`) dan menggunakan `werkzeug.utils.secure_filename` untuk mencegah serangan *path traversal*.  
* **Konfirmasi Aksi Destruktif:** Operasi penghapusan data (`POST /hapus/<id>`) dilindungi dengan dialog konfirmasi modal/dialog di sisi klien (`onsubmit="return confirm(...)"`).  
* **Prepared Statements:** Menggunakan kueri berparameter pada backend untuk mencegah kerentanan *SQL Injection*.

### 3.3 State Management Sisi Klien

* **`sessionStorage` (`intro_selesai`):** Menyimpan status apakah pengguna baru pertama kali memasuki sesi tab browser. Bersifat sementara; jika tab ditutup, status ter-reset.  
* **`localStorage` (`temukampus_leaf_effect`):** Menyimpan preferensi tombol sakelar daun gugur (*enabled* / *disabled*) secara persisten lintas sesi penjelajahan.

---

## 4\. Alur Kerja Deployment (Deployment Workflow)

```
[Local Environment (VS Code & XAMPP)]
       │
       ├── 1. Freeze Dependensi: pip freeze > requirements.txt
       ├── 2. Ekspor Struktur & Data: mysqldump / phpMyAdmin (temukampus.sql)
       └── 3. Sanitasi Kredensial Database di Main.py
       │
       ▼
[Production Server (PythonAnywhere / Cloud VPS)]
       │
       ├── Buat Database MySQL Server & Import temukampus.sql
       ├── Buat Virtual Environment (Python 3.10+) & pip install -r requirements.txt
       ├── Setup Web Server WSGI Handler mengarah ke Main:app
       └── Uji Akses Domain & Perizinan Direktori /uploads
```

---

## 5\. Matriks Pengujian Akhir (Testing Matrix)

| ID Uji | Skenario | Hasil yang Diharapkan | Status |
| :---- | :---- | :---- | :---- |
| TC-01 | Pengguna membuka situs di tab baru. | Splash screen Rockstar muncul \~0.4-0.6s setelah halaman termuat, lalu memudar halus ke dashboard. | Lulus |
| TC-02 | Pengguna menekan tombol filter atau pencarian. | Data terfilter instan, intro Rockstar TIDAK muncul ulang, hanya top bar yang berjalan. | Lulus |
| TC-03 | Pengguna mengklik tombol sakelar daun di kanan atas. | Partikel daun seketika hilang, teks tombol menjadi `Efek: OFF`, preferensi tersimpan di reload berikutnya. | Lulus |
| TC-04 | Pengguna menginput laporan tanpa melampirkan foto. | Sistem berhasil menyimpan laporan dan menampilkan placeholder bawaan (*fallback*) tanpa galat. | Lulus |
| TC-05 | Pengguna menekan tombol Hapus. | Muncul jendela konfirmasi dialog; jika dibatalkan, data tetap aman di basis data. | Lulus |

&nbsp;