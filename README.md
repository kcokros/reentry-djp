# PDF Document Processor

Aplikasi **Streamlit** untuk memproses dan mengekstrak data terstruktur dari file PDF **LHPT** dan **LHP2DK**. Aplikasi ini memproses dokumen PDF yang diunggah dan menghasilkan file CSV yang berisi data dan analisis utama dari dokumen tersebut.

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

Instal dependensi dengan perintah berikut:
```bash
pip install streamlit pdfplumber pandas
Memulai
Clone Repository
bash
Copy code
git clone https://github.com/yourusername/pdf-document-processor.git
cd pdf-document-processor
Jalankan Aplikasi
Arahkan ke direktori proyek.
Jalankan aplikasi Streamlit:
bash
Copy code
streamlit run app.py
Buka URL yang disediakan di browser Anda untuk mengakses aplikasi.
Cara Menggunakan
Unggah File PDF:

Pilih menu LHPT Processor atau LHP2DK Processor di sidebar.
Unggah satu atau beberapa file PDF melalui fitur drag and drop atau penjelajahan file.
Proses File:

Klik tombol "Upload".
Aplikasi akan mengekstrak data yang diperlukan dan menampilkan hasilnya dalam tabel.
Unduh Hasil:

Klik tombol Download CSV untuk menyimpan data yang telah diproses dalam format CSV.
Lihat Data yang Diproses:

Lihat pratinjau data hasil ekstraksi langsung di dalam aplikasi.
Struktur File
bash
Copy code
pdf-document-processor/
├── app.py                  # Aplikasi utama Streamlit
├── README.md               # Dokumentasi proyek
├── requirements.txt        # Daftar dependensi
Contoh Output
Output CSV LHPT:
Nama File	Nomor LHPT	Tahun Pajak	Data Pemicu	Data Penguji	...
LHPT_Example.pdf	LAP-1234	2023	pemicu-xyz	penguji-abc	...
Output CSV LHP2DK:
Jenis Data	NOMOR_LHPT	Indikasi Ketidakpatuhan	Modus Ketidakpatuhan	Total Potensi Awal	Total Potensi Akhir
Data Penguji Example	5678	Indikasi Contoh	Modus Contoh	1000000.00	1200000.00
Pengembangan di Masa Depan
Tambahkan penanganan error untuk file PDF yang tidak valid atau rusak.
Termasuk visualisasi data untuk wawasan yang diekstrak.
Dukungan untuk format dokumen tambahan.
Kontribusi
Kontribusi sangat diterima! Harap fork repository ini dan buat pull request untuk peningkatan fitur atau perbaikan bug.

Lisensi
Proyek ini dilisensikan di bawah MIT License. Lihat file LICENSE untuk detail lebih lanjut.

Kontak
Untuk pertanyaan atau dukungan, hubungi:

Nama: Nama Anda
Email: email.anda@example.com
GitHub: yourusername
yaml
Copy code

---

### Cara Menggunakan:
1. Salin teks di atas.
2. Tempel ke file `README.md` dalam proyek Anda.
3. Simpan dan tambahkan file tersebut ke repository GitHub Anda.

Jika ada bagian yang ingin disesuaikan lebih lanjut, beri tahu saya! 😊
