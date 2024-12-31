# PDF Document Processor

Aplikasi **Streamlit** sangat sederhana untuk memproses dan mengekstrak data terstruktur dari file PDF **LHPT** dan **LHP2DK**. Aplikasi ini memproses dokumen PDF yang diunggah dan menghasilkan file CSV yang berisi data dan analisis utama dari dokumen tersebut.

---

## Fitur

1. **Proses PDF LHPT**:
   - Mengekstrak detail penting seperti:
     - **Nomor LHPT**, **Tahun Pajak**, **Data Pemicu**, dan **Data Penguji**.
     - Bidang analisis keuangan: **Analisis Laporan Keuangan**, **Transfer Pricing**, **PPH Penghasilan**, dan lainnya.
     - Indikator kepatuhan seperti **Indikasi Ketidakpatuhan**, **Modus Ketidakpatuhan**, dan **Treatment**.
   - Mendukung pengolahan banyak file PDF sekaligus.
   - Menghasilkan file CSV yang dapat diunduh.

2. **Proses PDF LHP2DK**:
   - Mengekstrak data utama seperti:
     - **Jenis Data**, **Indikasi Ketidakpatuhan**, **Modus Ketidakpatuhan**, dan lainnya.
     - Potensi pajak: **Total Potensi Awal** dan **Total Potensi Akhir**.
   - Mendukung batch processing dan menghasilkan output CSV terstruktur.

3. **Antarmuka Ramah Pengguna**:
   - Unggah file PDF secara interaktif untuk satu atau beberapa file.
   - Menampilkan progress bar dan status selama pemrosesan.
   - Memperlihatkan data hasil ekstraksi dan menyediakan tombol unduh hasil.

---

## Persyaratan

### Python Dependencies
Library Python yang diperlukan untuk menjalankan aplikasi ini:
- `streamlit`
- `pdfplumber`
- `pandas`
- `re`

Cara Menggunakan
Unggah File PDF:

Pilih menu LHPT Processor atau LHP2DK Processor di sidebar.
Unggah satu atau beberapa file PDF melalui fitur drag and drop atau penjelajahan file.
Proses File:

Klik tombol "Upload".
Aplikasi akan mengekstrak data yang diperlukan dan menampilkan hasilnya dalam tabel.
Unduh Hasil:

Klik tombol Download CSV untuk menyimpan data yang telah diproses dalam format CSV.

Kontribusi
Kontribusi sangat diterima! Harap fork repository ini dan buat pull request untuk peningkatan fitur atau perbaikan bug.

Kontak
Untuk pertanyaan atau dukungan, hubungi:
Nama: Kartiko C.S.
Email: kartiko.sewoyo@kemenkeu.go.id
