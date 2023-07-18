## Sistem Pemantauan Kesehatan (SIMPKES):

Sistem Pemantauan Kesehatan berbasis Internet of Things

## Instalasi

1. Install **Python 3.8.***.
2. Install **XAMPP**.
3. Import database aplikasi:
   - Jalankan **XAMPP**.
   - Buka phpMyAdmin dengan cara menekan tombol admin pada modul **MySQL**.
   - Pilih **import** pada navbar phpMyAdmin.
   - Tekan **Choose file**.
   - Pilih file **database.sql**.
4. Buka CMD dalam direktori lalu ketik perintah `python -m venv Env` untuk membuat python virtual environment.
5. Jalankan **start-env.bat** untuk masuk ke dalam virtual environment.
6. Ketik perintah `pip install -r requirements.txt` untuk menginstal kebutuhan dari python.
7. Jalankan start-project.bat untuk menjalankan aplikasi.
8. Buka URL http://127.0.0.1:8000/ pada browser yang digunakan untuk membuka aplikasi.
