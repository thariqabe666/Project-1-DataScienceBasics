# 🎓 Aplikasi Database Mahasiswa FTUI 2021

Aplikasi berbasis *command-line* (CLI) untuk mengelola dan menganalisis data fiktif mahasiswa dari Fakultas Teknik Universitas Indonesia (FTUI) angkatan 2021. Aplikasi ini memungkinkan pengguna untuk melihat, mencari, menambah, dan menganalisis data mahasiswa secara interaktif langsung dari terminal.

Proyek ini dibuat sebagai bagian dari **Capstone Project Module 1** di Purwadhika Digital Technology School.


## ✨ Fitur Utama

Aplikasi ini memiliki 3 menu utama yang kaya akan fitur:

### 1. Tampilkan Data Mahasiswa
Menu ini menyediakan berbagai cara untuk melihat dan mencari data mahasiswa:
* **Tampilkan 100 Data Mahasiswa**: Menampilkan 100 data pertama yang diurutkan berdasarkan nama.
* **Lihat Daftar Departemen & Jurusan**: Menampilkan daftar unik semua departemen dan jurusan yang ada di database.
* **Pencarian Fleksibel**:
    * Cari mahasiswa berdasarkan **Departemen**.
    * Cari mahasiswa berdasarkan **Jurusan**.
    * Cari mahasiswa spesifik berdasarkan **NPM**.

### 2. Tambah Data Mahasiswa Baru
Fitur untuk menambahkan data mahasiswa baru dengan sistem validasi untuk menjaga integritas data:
* **Validasi NPM Unik**: Program akan menolak jika NPM yang dimasukkan sudah ada di database.
* **Validasi Input Terstruktur**: Memastikan input Departemen, IPK, dan Jenis Kelamin sesuai dengan format yang ditentukan.
* **Konfirmasi Pengguna**: Meminta konfirmasi akhir sebelum data disimpan ke database.

### 3. Analisis & Visualisasi Data
Menu ini menyediakan ringkasan statistik dan visualisasi data untuk mendapatkan wawasan:
* **Statistik Deskriptif**: Menampilkan statistik lengkap untuk kolom IPK (rata-rata, standar deviasi, min, max, kuartil) menggunakan Pandas.
* **Agregasi Data**: Menampilkan jumlah total mahasiswa untuk setiap departemen.
* **Visualisasi Data**:
    * **Histogram**: Menampilkan distribusi sebaran IPK seluruh mahasiswa.
    * **Bar Chart**: Menampilkan perbandingan rata-rata IPK antar departemen.

## 🛠️ Teknologi dan Library

* **Bahasa**: Python 3
* **Database**: MySQL
* **Library Python**:
    * `mysql-connector-python`: Untuk koneksi ke database MySQL.
    * `pandas`: Untuk manipulasi, analisis, dan menampilkan data.
    * `seaborn` & `matplotlib`: Untuk membuat visualisasi data.
    * `faker`: Untuk menghasilkan data dummy yang realistis.
    * `numpy`: Untuk membantu generasi data numerik.

## 🚀 Instalasi dan Cara Menjalankan

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer lokal Anda.

### 1. Prasyarat
* Python 3.7 atau lebih baru.
* MySQL Server sudah terinstal dan berjalan.

### 2. Clone Repository
```bash
git clone [https://github.com/thariqabe666/capstone-1.git](https://github.com/thariqabe666/capstone-1.git)
cd capstone-1
```

### 3. Buat Virtual Environment & Instal Dependensi
Sangat disarankan untuk menggunakan *virtual environment*.

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan (Windows)
.\venv\Scripts\activate

# Aktifkan (macOS/Linux)
source venv/bin/activate
```
Buat file `requirements.txt` dan isi dengan teks di bawah ini, lalu jalankan `pip install`.
```txt
mysql-connector-python
pandas
matplotlib
seaborn
Faker
numpy
```
```bash
pip install -r requirements.txt
```

### 4. Setup Database
1.  Buat database baru di MySQL Anda (misalnya, `db_kampus`).
2.  Impor file `.sql` yang telah Anda siapkan ke dalam database tersebut. File ini akan membuat tabel `mahasiswa` dan mengisinya dengan 1000 data dummy.

### 5. Konfigurasi Koneksi
Buka file `capstone_project_1_main_app.py` dan `generate_data.py`, lalu sesuaikan detail koneksi di dalam dictionary `DB_CONFIG` agar sesuai dengan konfigurasi MySQL Anda (terutama `user` dan `password`).

### 6. Jalankan Aplikasi
Untuk menjalankan aplikasi utama, gunakan perintah:
```bash
python capstone_project_1_main_app.py
```

## 📖 Cara Menggunakan
Setelah aplikasi berjalan, Anda akan disambut dengan menu utama. Cukup masukkan angka yang sesuai dengan menu yang ingin Anda akses dan tekan Enter. Ikuti instruksi yang muncul di setiap menu. Untuk keluar dari aplikasi, pilih opsi "Keluar" dari menu utama.

## 📂 Struktur Proyek
```
.
├── capstone_project_1_main_app.py  # File utama aplikasi CLI
├── generate_data.py                # Skrip untuk membuat & memasukkan data dummy
├── database.sql                    # File SQL untuk setup database & tabel
└── README.md                       # Anda sedang membacanya
```
