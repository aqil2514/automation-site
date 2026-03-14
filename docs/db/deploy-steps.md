# Dokumentasi Setup & Integrasi Database (Neon.tech)

Dokumen ini mencatat langkah-langkah menghubungkan backend FastAPI dengan database PostgreSQL di Neon.tech.

## 1. Persiapan Database

Database menggunakan **Neon.tech** karena mendukung fitur *serverless* dan *autoscaling*.

* **Project Name:** `gamelingo-automation`
* **Region:** `aws-ap-southeast-1` (Singapore)
* **Status:** Aktif

## 2. Konfigurasi Environment Variable

URL koneksi database dari Neon harus didaftarkan ke Google Cloud Run agar FastAPI dapat melakukan koneksi.

```powershell
# Menambahkan DATABASE_URL ke Google Cloud Run
gcloud run services update gamelingo-api `
  --set-env-vars="DATABASE_URL=postgresql://[USER]:[PASSWORD]@[HOST]/[DB_NAME]?sslmode=require" `
  --region asia-southeast2

```

*Catatan: Gunakan URL dengan mode `pooler` untuk manajemen koneksi yang lebih efisien.*

## 3. Skema Tabel (Auto-Migration)

Skema tabel didefinisikan menggunakan **SQLAlchemy** di dalam `apps/api/main.py`. Tabel akan dibuat secara otomatis saat service dijalankan pertama kali (`Base.metadata.create_all`).

### Struktur Tabel: `raw_contents`

Tabel ini digunakan untuk menampung data mentah hasil *scraping* sebelum diproses oleh AI.

| Kolom | Tipe Data | Deskripsi |
| --- | --- | --- |
| `id` | Integer (PK) | Auto-increment ID |
| `source_url` | String(500) | URL asli berita/sumber |
| `title` | String(500) | Judul asli dari sumber |
| `content_raw` | Text | Isi artikel mentah (HTML/Teks) |
| `image_url` | String(500) | URL gambar utama |
| `status` | String(50) | Status: `pending`, `processed`, `error` |
| `created_at` | DateTime | Waktu data diambil |

## 4. Verifikasi Koneksi

Setelah deploy selesai, verifikasi koneksi dapat dilakukan dengan:

1. Membuka URL Service API: Status `db_connected: true` harus muncul.
2. Mengecek Dashboard Neon.tech: Menu **Tables** harus menampilkan tabel `raw_contents`.

---

**Tips Keamanan:**
Jangan pernah melakukan *commit* file yang berisi `DATABASE_URL` asli ke GitHub. Gunakan file `.env` (lokal) dan *Environment Variables* (Cloud) untuk menjaga keamanan kredensial.