Siap, Aqil. Mari kita rapikan dokumentasi ini agar menjadi panduan yang solid di dalam `docs/steps.md`. Saya sesuaikan formatnya agar mudah dibaca di Windows (PowerShell) dan mencakup apa yang baru saja kita lakukan dengan sukses.

Berikut adalah draf isi untuk file `docs/steps.md`:

---

# Dokumentasi Deployment Gamelingo (Google Cloud Run)

Dokumen ini berisi langkah-langkah untuk melakukan deployment manual dari mesin lokal (Windows) ke Google Cloud Platform.

## 1. Inisialisasi Environment

Pastikan Google Cloud SDK sudah terinstal di Windows dan terminal sudah diarahkan ke folder project.

```powershell
# Inisialisasi akun dan pilih project (automation-489502)
gcloud init

# Pastikan konfigurasi menunjuk ke project yang benar
gcloud config set project automation-489502

```

## 2. Deployment API (FastAPI)

Deployment dilakukan langsung dari source code menggunakan **Cloud Build** (server-side build).

### Langkah-langkah:

1. Masuk ke direktori service API:
```powershell
cd apps/api

```


2. Jalankan perintah deploy:
```powershell
gcloud run deploy gamelingo-api `
  --source . `
  --region asia-southeast2 `
  --allow-unauthenticated

```



### Parameter Penting:

* `--source .`: Menginstruksikan Google untuk memaketkan file di folder saat ini dan membangun Docker image secara otomatis di cloud.
* `--region asia-southeast2`: Lokasi server di Jakarta (latensi rendah).
* `--allow-unauthenticated`: Membuat API dapat diakses publik tanpa token autentikasi IAM.

## 3. Post-Deployment (Monitoring)

Setelah deployment selesai, URL service akan muncul di terminal. Untuk memantau jika ada error:

```powershell
# Melihat log secara real-time dari terminal
gcloud run logs tail gamelingo-api --region asia-southeast2

```

## 4. Environment Variables (Opsional)

Jika ingin menambahkan atau memperbarui variabel environment (seperti URL database) tanpa deploy ulang:

```powershell
gcloud run services update gamelingo-api `
  --set-env-vars="DATABASE_URL=your_db_url_here" `
  --region asia-southeast2

```

---

### Tips untuk Pengembangan Selanjutnya:

* **File `.gcloudignore**`: Pastikan file ini ada di root atau di dalam `apps/api` untuk mencegah folder `node_modules`, `__pycache__`, atau `.venv` ikut terunggah, yang bisa memperlambat proses deployment.
* **Port**: Cloud Run secara default menggunakan port **8080**, pastikan FastAPI mendengarkan pada port tersebut (via variabel environment `PORT`).