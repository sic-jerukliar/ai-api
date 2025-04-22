# 📸 ESP32-CAM Face Verification & Email Recap API

## 1. Tentang API

API ini merupakan backend berbasis Python Flask yang berfungsi untuk:
- Menerima dan menyimpan gambar dari perangkat seperti ESP32-CAM.
- Menampilkan galeri gambar yang sudah di-upload.
- Memverifikasi wajah siswa berdasarkan gambar dan ID siswa.
- Mengirimkan rekap kehadiran bulanan siswa kepada wali murid melalui email.

## 2. Framework yang Digunakan

- **Flask**: Untuk membangun REST API dan menyajikan konten web.
- **dotenv**: Untuk mengelola credential dan konfigurasi lewat file `.env`.
- **smtplib**: Untuk pengiriman email melalui SMTP.
- **email.mime**: Untuk format email multipart.
- **ThreadPoolExecutor**: Untuk pengiriman email secara paralel.

## 3. How to Use

### 3.1 Install Virtual Environment (venv)

```bash
python -m venv venv
```

### 3.2 Activate Virtual Environment

- **Linux/macOS:**
```bash
source venv/bin/activate
```

- **Windows:**
```bash
venv\Scripts\activate
```

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Buat File `.env`

Buat file `.env` di root project dan masukkan credential berikut:

```env
EMAIL_SMTP=smtp.your-email.com
EMAIL_PORT=587
EMAIL_SENDER=your-email@example.com
EMAIL_PASSWORD=your-secure-password
```

### 3.5 Jalankan Program

```bash
python main.py
```

Setelah dijalankan, server akan aktif di `http://0.0.0.0:5000`.