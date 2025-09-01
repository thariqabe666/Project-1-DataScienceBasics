import mysql.connector
from faker import Faker
import random
import numpy as np

# Konfigurasi dan Koneksi ke Database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '#Abeteknik04',
    'database': 'db_kampus'
}

# Data Departemen & Jurusan FTUI
DEPARTEMEN_JURUSAN = {
    'Departemen Teknik Sipil': ['Teknik Sipil', 'Teknik Lingkungan'],
    'Departemen Teknik Mesin': ['Teknik Mesin', 'Teknik Perkapalan'],
    'Departemen Teknik Elektro': ['Teknik Elektro', 'Teknik Komputer', 'Teknik Biomedik'],
    'Departemen Teknik Metalurgi dan Material': ['Teknik Metalurgi dan Material'],
    'Departemen Arsitektur': ['Arsitektur', 'Arsitektur Interior'],
    'Departemen Teknik Kimia': ['Teknik Kimia', 'Teknik Bioproses'],
    'Departemen Teknik Industri': ['Teknik Industri']
}

# Inisialisasi Faker
fake = Faker('id_ID')  # Menggunakan locale Indonesia

# Pembuatan data dummy mahasiswa Indonesia
def generate_mahasiswa(jumlah):
    list_mahasiswa = []
    npm_terpakai = set() # Menggunakan set untuk memastikan NPM unik dan pengecekan cepat

    for _ in range(jumlah):
        # 1. Jenis Kelamin
        jenis_kelamin = random.choice(['Laki-laki','Perempuan'])

        # 2. Nama sesuai dengan jenis kelamin
        if jenis_kelamin == 'Laki-laki':
            nama = fake.name_male()
        else:
            nama = fake.name_female()

        # 3. Buat NPM 
        while True:
            npm_random = f"21067{random.randint(10000,99999)}"
            if npm_random not in npm_terpakai:
                npm = npm_random
                npm_terpakai.add(npm)
                break 
        
        # 4. Pilih departemen dan jurusan
        departemen = random.choice(list(DEPARTEMEN_JURUSAN.keys()))
        jurusan = random.choice(DEPARTEMEN_JURUSAN[departemen])

        # 5. Angkatan
        angkatan = 2021

        # 6. Generate IPK (mayoritas di atas 3.00)
        # Menggunakan Beta Distribution left skewed
        # Left-skewed (Negative Skewness): If α > β, the distribution is skewed to the left.
        ipk = round(float(np.random.beta(5,1.5)*4),2)
        if ipk > 4.0:
            ipk = 4.0
        
        list_mahasiswa.append((npm, nama, departemen, jurusan, angkatan, ipk, jenis_kelamin))
    return list_mahasiswa

# export data ke csv
def export_to_csv(data, filename='data_mahasiswa.csv'):
    import pandas as pd
    df = pd.DataFrame(data, columns=['NPM', 'Nama', 'Departemen', 'Jurusan', 'Angkatan', 'IPK', 'Jenis Kelamin'])
    df.to_csv(filename, index=False)
    print(f"Data berhasil diekspor ke {filename}")

# Memasukkan data ke database
def insert_to_db(data_mahasiswa):
    """Fungsi untuk memasukkan data ke database MySQL."""
    
    # Query untuk memasukkan data
    query = """
    INSERT INTO mahasiswa 
    (NPM, Nama, Departemen, Jurusan, Angkatan, IPK, JenisKelamin) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn = None
    try:
        # Membuat koneksi ke database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Menggunakan executemany untuk efisiensi saat memasukkan banyak data
        cursor.executemany(query, data_mahasiswa)

        # Commit perubahan
        conn.commit()

        print(f"Berhasil: {cursor.rowcount} data mahasiswa telah dimasukkan ke database.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Koneksi ke database telah ditutup")


if __name__ == "__main__":
    jumlah_data = 1000

    print(f"Menghasilkan {jumlah_data} data mahasiswa")
    data_mahasiswa = generate_mahasiswa(jumlah_data)

    print("Mengekspor ke CSV")
    export_to_csv(data_mahasiswa)

    print("Memasukkan data ke database SQL")
    insert_to_db(data_mahasiswa)



