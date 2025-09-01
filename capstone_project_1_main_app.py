import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfigurasi Database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '#Abeteknik04',
    'database': 'db_kampus'
}

# i. Clear Screen
def clear_screen():
    # Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Untuk MacOS dan Linux
    else:
        _ = os.system('clear')

# ii. Membuat dan mengembalikan koneksi ke database
def create_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error saat koneksi ke database: {err}")
        return None
    
# Fitur 1: Menampilkan data mahasiswa
# Opsi: Menampilkan semua data, filter, atau cari data
def tampilkan_data():
    conn = create_connection()
    if conn is None:
        return
    
    while True:
        clear_screen()
        print("---Menu Tampilkan Data Mahasiswa---")
        print("1. Tampilkan 100 Data Mahasiswa")
        print("2. Tampilkan Data Departemen")
        print("3. Tampilkan Data Jurusan")
        print("4. Filter/Cari Data Berdasarkan Departemen")
        print("5. Filter/Cari Data Berdasarkan Jurusan")
        print("6. Cari Data Berdasarkan NPM")
        print("7. Kembali ke Menu Utama")
        pilihan = input("Pilih Menu (1-7): ")

        if pilihan == '1':
            try:
                # Menggunakan pandas untuk membaca dan menampilkan data dengan rapi
                df = pd.read_sql("SELECT * FROM mahasiswa ORDER BY Nama ASC LIMIT 100", conn)
                print("\n--- 100 Data Mahasiswa FTUI 2021 ---")
                print(df.to_string()) # .to_string() agar semua baris ditampilkan
            except Exception as e:
                print(f"Terjadi error: {e}")
            input("\nTekan Enter untuk Kembali")

        elif pilihan == '2':
            try:
                df = pd.read_sql("SELECT DISTINCT Departemen FROM mahasiswa ORDER BY Departemen ASC", conn)
                print("\n--- Daftar Departemen ---")
                print(df.to_string())
            except Exception as e:
                print(f"Terjadi error: {e}")
            input("\nTekan Enter untuk Kembali")

        elif pilihan == '3':
            try:
                df = pd.read_sql("SELECT DISTINCT Jurusan FROM mahasiswa ORDER BY Jurusan ASC", conn)
                print("\n--- Daftar Jurusan ---")
                print(df.to_string())
            except Exception as e:
                print(f"Terjadi error: {e}")
            input("\nTekan Enter untuk Kembali")

        elif pilihan == '4':
            try:
                keyword = input("Masukkan nama Departemen yang dicari: ")
                query = "SELECT * FROM mahasiswa WHERE Departemen LIKE %s"
                # Menggunakan %keyword% untuk pencarian yang lebih fleksibel
                df = pd.read_sql(query, conn, params=[f"%{keyword}%"])

                if df.empty:
                    print(f"\nTidak ada hasil pencarian untuk '{keyword}'.")
                else:
                    print(f"\n--- Hasil Pencarian untuk '{keyword}' ---")
                    print(df.to_string())
            except Exception as e:
                print(f"Terjadi error {e}")
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '5':
            try:
                keyword = input("Masukkan nama Jurusan yang dicari: ")
                query = "SELECT * FROM mahasiswa WHERE Jurusan LIKE %s"
                df = pd.read_sql(query, conn, params=[f"%{keyword}%"])

                if df.empty:
                    print(f"\nTidak ada hasil pencarian untuk '{keyword}'.")
                else:
                    print(f"\n--- Hasil Pencarian untuk '{keyword}' ---")
                    print(df.to_string())
            except Exception as e:
                print(f"Terjadi error {e}")
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '6':
            try:
                npm = input("Masukkan NPM yang dicari: ")
                query = "SELECT * FROM mahasiswa WHERE NPM = %s"
                df = pd.read_sql(query, conn, params=[npm])

                if df.empty:
                    print(f"\nTidak ada mahasiswa dengan NPM '{npm}'.")
                else:
                    print(f"\n--- Hasil Pencarian untuk NPM '{npm}' ---")
                    print(df.to_string())
            except Exception as e:
                print(f"Terjadi error {e}")
            input("\nTekan Enter untuk kembali...")
        
        elif pilihan == '7':
            break
        else:
            input("Pilihan tidak valid. Tekan Enter untuk mencoba lagi...")
    
    if conn  and conn.is_connected():
        conn.close()


# Fitur 2: Menambahkan data mahasiswa ke database
# Opsi: Validasi input (NPM unik, rentang IPK, Jenis Kelamin)
def tambah_data():
    conn = create_connection()
    if conn is None:
        return
    
    cursor = conn.cursor()

    clear_screen()
    print("--- Menu Tambah Data Mahasiswa Baru")

    try:
        # Validasi 1: Pengecekan keunikan NPM
        while True:
            npm = input("Masukkan NPM (10 digit, contoh: 2106712345): ")
            cursor.execute("SELECT NPM FROM mahasiswa WHERE NPM = %s", (npm,))
            if cursor.fetchone():
                print(f"ERROR: NPM {npm} sudah terdaftar. Silakan periksa kembali input NPM.")
            else:
                break
        
        nama = input("Masukkan Nama Lengkap: ")

        # Ambil daftar departemen dari database untuk validasi
        cursor.execute("SELECT DISTINCT Departemen FROM mahasiswa")
        departemen_valid = [item[0] for item in cursor.fetchall()]
        while True:
            print("\nPilihan Departemen:", ", ".join(departemen_valid))
            departemen = input("Masukkan Departemen: ")
            if departemen in departemen_valid:
                break
            else:
                print("ERROR: Departemen tidak valid")
        
        jurusan = input("Masukkan Jurusan: ")
        angkatan = int(input("Masukkan Angkatan (contoh: 2021): "))

        # Validasi 2: Pengecekan rentang IPK
        while True:
            try:
                ipk = float(input("Masukkan IPK (0.00-4.00): "))
                if 0.0 <= ipk <= 4.00:
                    break
                else:
                    print("ERROR: IPK harus di antara 0.00 dan 4.00")
            except ValueError:
                print("ERROR: Masukkan angka yang valid untuk IPK.")

        # Validasi 3: Pengecekan pilihan Jenis Kelamin
        while True:
            jenis_kelamin = input("Masukkan Jenis Kelamin (Laki-laki atau Perempuan): ")
            if jenis_kelamin in ['Laki-laki','Perempuan']:
                break
            else:
                print("ERROR: Pilihan hanya Laki-laki atau Perempuan")

        # Konfirmasi sebelum menyimpan data
        print("\n--- Rekap Input Data Baru ---")
        print(f"NPM: {npm}\nNama: {nama}\nDepartemen: {departemen}\nJurusan: {jurusan}")
        print(f"Angkatan: {angkatan}\nIPK: {ipk}\nJenis Kelamin: {jenis_kelamin}")

        konfirmasi = input("Apakah Anda yakin ingin menyimpa data ini? (y/n): ").lower()

        if konfirmasi == 'y':
            query = """
            INSERT INTO mahasiswa (NPM, Nama, Departemen, Jurusan, Angkatan, IPK, JenisKelamin)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data_baru = (npm,nama,departemen,jurusan,angkatan,ipk,jenis_kelamin)
            cursor.execute(query,data_baru)
            conn.commit()
            print("\nSUKSES: Data mahasiswa baru berhasil disimpan!")
        else:
            print("\nBATAL: Data tidak disimpan")
    
    except mysql.connector.Error as err:
        print(f"\nError saat menyimpan data: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

    input("\nTekan Enter untuk kembali ke menu utama")

# Fitur 3: Menampilkan statistik dan visualisasi data.
# Opsi: Statistik lengkap (.describe), value_counts, dan plot gabungan.
def analisis_data():
    conn = create_connection()
    if conn is None:
        return
    
    # Ambil semua data ke DataFrame untuk analisis
    try:
        df = pd.read_sql("SELECT * FROM mahasiswa", conn)
    except Exception as e:
        print(f"Gagal mengambil data: {e}")
        if conn and conn.is_connected():
            conn.close()
        return
    
    while True:
        clear_screen()
        print("--- Menu Analisis & Visualisasi Data ---")
        print("1. Tampilkan Statistik Deskriptif IPK")
        print("2. Tampilkan Jumlah Mahasiswa per Departemen")
        print("3. Visualisasi: Distribusi IPK (Histogram)")
        print("4. Visualisasi: Rata-rata IPK er Departemen (Bar Chart)")
        print("5. Kembali ke Menu Utama")
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == '1':
            print("\n---Statistik Deskriptif IPK Mahasiswa---")
            print(df['IPK'].describe())
            input("\nTekan Enter untuk kembali...")
        
        elif pilihan == '2':
            print("\n---Jumlah Mahasiswa per Departemen---")
            print(df['Departemen'].value_counts())
            input("\nTekan Enter untuk kembali...")
        
        elif pilihan == '3':
            print("\n---Menampilkan Plot Distribusi IPK---")
            sns.histplot(df['IPK'], kde=True)
            plt.xlabel('IPK')
            plt.ylabel('Frekuensi')
            plt.show()
        
        elif pilihan == '4':
            print("\n---Menampilkan Plot Rata-rata IPK per Departemen")
            # Menghitung rata-rata IPK per departemen
            avg_ipk_departemen = df.groupby('Departemen')['IPK'].mean().sort_values(ascending=False)

            plt.figure(figsize=(10,6)) # Agar tabel tidak bertumpuk
            sns.barplot(x=avg_ipk_departemen.values, y=avg_ipk_departemen.index)
            plt.title('Rata-rata IPK per Departemen')
            plt.xlabel('Rata-rata IPK')
            plt.ylabel('Departemen')
            plt.tight_layout() # Merapikan layout
            plt.show()

        elif pilihan == '5':
            break
        else:
            input("Pilihan tidak valid. Tekan Enter untuk mencoba lagi...")

    if conn and conn.is_connected():
        conn.close()

# Fungsi utama untuk menjalankan aplikasi
def main():
    while True:
        clear_screen()
        print("==================================================")
        print("     Aplikasi Database Mahasiswa FTUI 2021")
        print("==================================================")
        print("Menu Utama:")
        print("1. Tampilkan Data Mahasiswa")
        print("2. Tambah Data Mahasiswa Baru")
        print("3. Analisis & Visualisasi Data")
        print("4. Keluar")
        print("__________________________________________________")

        pilihan = input("Pilih Menu (1-4): ")

        if pilihan =='1':
            tampilkan_data()
        elif pilihan == '2':
            tambah_data()
        elif pilihan == '3':
            analisis_data()
        elif pilihan == '4':
            print("Terima kasih telah menggunakan aplikasi ini. Sampai Jumpa!🙏😊")
            break
        else:
            input("Pilihan tidak valid. Tekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    main()


    


        
