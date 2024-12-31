import streamlit as st
import pdfplumber
import pandas as pd
import re
import os
from io import BytesIO
import tempfile

# Title and sidebar setup
st.title('PDF Document Processor')
processing_type = st.sidebar.radio(
    "Select Processing Type",
    ["Proses LHPT", "Proses LHP2DK"]
)

if processing_type == "Proses LHPT":
    st.header('LHPT PDF Processor')
    # Original LHPT processing code
    
    # Functions for LHPT processing (keeping all the original functions)
    def extract_nomor_lhpt(text):
        match = re.search(r"LAP-\d+/LHPT/[A-Z]+\.\d+/202\d", text)
        return match.group(0) if match else "N/A"

    def extract_tahun_pajak(text):
        match = re.search(r"Tahun Pajak\s*:\s*(\d{4})", text)
        return match.group(1) if match else "N/A"

    def extract_lampiran_data(text, label):
        match = re.findall(rf"{label}-(.*?)\.dsv", text)
        return "; ".join(f"{label}-{item}.dsv" for item in match) if match else "N/A"

    def extract_validasi_data_pemicu(text, field):
        field_map = {
            "Data Digunakan": r"Data digunakan\s*\d+\s*([\d.]+)",
            "Data Tidak Sesuai": r"Data tidak sesuai\s*\d+\s*([\d.]+)",
            "Data Sudah Digunakan": r"Data sudah digunakan\s*\d+\s*([\d.]+)",
            "Data Beririsan": r"Data beririsan\s*\d+\s*([\d.]+)"
        }
        pattern = field_map.get(field, "")
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return float(match.group(1).replace(".", "")) if match.group(1) != "0" else 0
        return 0

    def extract_indikasi_ketidakpatuhan(text):
        if "1. Indikasi Ketidakpatuhan" in text and "2. Modus Ketidakpatuhan" in text:
            start_index = text.find("1. Indikasi Ketidakpatuhan") + len("1. Indikasi Ketidakpatuhan")
            end_index = text.find("2. Modus Ketidakpatuhan")
            return text[start_index:end_index].replace("\n", " ").strip()
        return "Section 'Indikasi Ketidakpatuhan' not found."

    def extract_modus_ketidakpatuhan(text):
        if "2. Modus Ketidakpatuhan" in text and "3. Potensi" in text:
            start_index = text.find("2. Modus Ketidakpatuhan") + len("2. Modus Ketidakpatuhan")
            end_index = text.find("3. Potensi")
            return text[start_index:end_index].replace("\n", " ").strip()
        return "Section 'Modus Ketidakpatuhan' not found."

    def extract_treatment(text):
        match = re.search(r"Berdasarkan penelitian Wajib Pajak.*?(diusulkan.*?\.)", text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else "N/A"

    # Define columns
    columns = [
        "Nama File", "Nomor LHPT", "Tahun Pajak", "Data Pemicu", "Data Penguji",
        "Nilai Data Digunakan", "Nilai Data Tidak Sesuai", "Nilai Data Sudah Digunakan", "Nilai Data Beririsan",
        "Analisis Laporan Keuangan", "Analisis Transfer Pricing",
        "Analisis PPH (Penghasilan)", "Analisis PPH (Biaya)",
        "Mirroring Pemeriksaan", "Pemotongan/Pemungutan", "Analisis PPN-PPNBM",
        "Analisis Pajak Lainnya", "Indikasi Ketidakpatuhan", "Modus Ketidakpatuhan", "Treatment"
    ]

    def extract_data_from_text(text, filename):
        # Extract data using regex patterns
        nomor_lhpt = extract_nomor_lhpt(text)
        tahun_pajak = extract_tahun_pajak(text)
        data_pemicu = extract_lampiran_data(text, "pemicu")
        data_penguji = extract_lampiran_data(text, "penguji")

        nilai_digunakan = extract_validasi_data_pemicu(text, "Data Digunakan")
        nilai_tidak_sesuai = extract_validasi_data_pemicu(text, "Data Tidak Sesuai")
        nilai_sudah_digunakan = extract_validasi_data_pemicu(text, "Data Sudah Digunakan")
        nilai_beririsan = extract_validasi_data_pemicu(text, "Data Beririsan")

        analisis_laporan_keuangan = re.search(r'2\) Analisis Laporan Keuangan\s*Masa Pajak Tahunan 2020(.+?)(3\)|Mirroring)', text, re.DOTALL)
        analisis_transfer_pricing = re.search(r'3\) Analisis Transfer Pricing dan Aspek Perpajakan Internasional\s*Masa Pajak Tahunan 2020(.+?)(4\)|Mirroring)', text, re.DOTALL)
        analisis_pph_penghasilan = re.search(r'a\) Analisis Penghasilan\s*Masa Pajak Tahunan 2020(.+?)b\)', text, re.DOTALL)
        analisis_pph_biaya = re.search(r'b\) Analisis Biaya\s*Masa Pajak Tahunan 2020(.+?)(5\)|Mirroring)', text, re.DOTALL)
        mirroring_pemeriksaan = re.search(r'5\) Mirroring Hasil Pemeriksaan, Keberatan, dan Banding\s*Masa Pajak Tahunan 2020(.+?)(6\)|Pemotongan)', text, re.DOTALL)
        pemotongan_pemungutan = re.search(r'6\) Pajak Penghasilan Pemotongan atau Pemungutan(.+?)(7\)|Analisis)', text, re.DOTALL)
        analisis_ppnbm = re.search(r'7\) Analisis PPN dan/atau PPnBM(.+?)(8\)|Analisis Pajak Lainnya)', text, re.DOTALL)
        analisis_pajak_lainnya = re.search(r'8\) Analisis Pajak Lainnya\s*Masa Pajak Tahunan 2020(.+?)(9\)|Fakta Lapangan|Indikasi)', text, re.DOTALL)
        indikasi_ketidakpatuhan = extract_indikasi_ketidakpatuhan(text)
        modus_ketidakpatuhan = extract_modus_ketidakpatuhan(text)
        treatment = extract_treatment(text)

        return {
            "Nama File": filename,
            "Nomor LHPT": nomor_lhpt,
            "Tahun Pajak": tahun_pajak,
            "Data Pemicu": data_pemicu,
            "Data Penguji": data_penguji,
            "Nilai Data Digunakan": nilai_digunakan,
            "Nilai Data Tidak Sesuai": nilai_tidak_sesuai,
            "Nilai Data Sudah Digunakan": nilai_sudah_digunakan,
            "Nilai Data Beririsan": nilai_beririsan,
            "Analisis Laporan Keuangan": analisis_laporan_keuangan.group(1).strip() if analisis_laporan_keuangan else "N/A",
            "Analisis Transfer Pricing": analisis_transfer_pricing.group(1).strip() if analisis_transfer_pricing else "N/A",
            "Analisis PPH (Penghasilan)": analisis_pph_penghasilan.group(1).strip() if analisis_pph_penghasilan else "N/A",
            "Analisis PPH (Biaya)": analisis_pph_biaya.group(1).strip() if analisis_pph_biaya else "N/A",
            "Mirroring Pemeriksaan": mirroring_pemeriksaan.group(1).strip() if mirroring_pemeriksaan else "N/A",
            "Pemotongan/Pemungutan": pemotongan_pemungutan.group(1).strip() if pemotongan_pemungutan else "N/A",
            "Analisis PPN-PPNBM": analisis_ppnbm.group(1).strip() if analisis_ppnbm else "N/A",
            "Analisis Pajak Lainnya": analisis_pajak_lainnya.group(1).strip() if analisis_pajak_lainnya else "N/A",
            "Indikasi Ketidakpatuhan": indikasi_ketidakpatuhan,
            "Modus Ketidakpatuhan": modus_ketidakpatuhan,
            "Treatment": treatment
        }

    def process_pdf_file(uploaded_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            with pdfplumber.open(tmp_file_path) as pdf:
                text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
                return extract_data_from_text(text, uploaded_file.name)
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            return {col: "N/A" for col in columns}
        finally:
            os.unlink(tmp_file_path)

    def process_and_analyze_data(df):
        analisis_columns = [
            "Analisis Laporan Keuangan",
            "Analisis Transfer Pricing",
            "Analisis PPH (Penghasilan)",
            "Analisis PPH (Biaya)",
            "Mirroring Pemeriksaan",
            "Pemotongan/Pemungutan",
            "Analisis PPN-PPNBM",
            "Analisis Pajak Lainnya"
        ]

        for col in analisis_columns:
            df[f'(AR) {col}'] = df[col].apply(lambda x: re.split(r'Analisis account representative : ', str(x))[0].strip() if pd.notna(x) else x)
            df[f'(KK) {col}'] = df[col].apply(lambda x: re.split(r'Pendapat atas Analisis dari Ketua Kelompok', str(x))[1].strip() if pd.notna(x) and len(re.split(r'Pendapat atas Analisis dari Ketua Kelompok', str(x))) > 1 else '')

        for col in analisis_columns:
            kk_col = f'(KK) {col}'
            df[kk_col] = df[kk_col].apply(lambda x: re.sub(r'^[:\s]+', '', str(x)) if pd.notna(x) else x)

        def cleanse_ar_text(text):
            if pd.notna(text):
                text = re.sub(r'Analisis account representative\s*:', '', text, flags=re.IGNORECASE).strip()
                text = re.sub(r'Pendapat atas Analisis dari Ketua Kelompok.*', '', text, flags=re.IGNORECASE | re.DOTALL).strip()
                text = re.sub(r'^=', '', text).strip()
            return text

        def cleanse_kk_text(text):
            if pd.notna(text):
                text = re.sub(r'^Pendapat atas Analisis dari Ketua Kelompok\s*:', '', text, flags=re.IGNORECASE).strip()
                text = re.sub(r'^=', '', text).strip()
            return text

        for col in df.columns:
            if col.startswith('(AR)'):
                df[col] = df[col].apply(cleanse_ar_text)
            elif col.startswith('(KK)'):
                df[col] = df[col].apply(cleanse_kk_text)

        return df
    
    uploaded_files = st.file_uploader("Upload LHPT PDF files", type=['pdf'], accept_multiple_files=True)
    
    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process each PDF file
        all_data = []
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            extracted_data = process_pdf_file(uploaded_file)
            all_data.append(extracted_data)
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        # Create DataFrame
        df = pd.DataFrame(all_data, columns=columns)
        
        # Process and analyze the data
        df_analyzed = process_and_analyze_data(df)
        
        # Convert DataFrame to CSV
        csv = df_analyzed.to_csv(index=False)
        
        # Create download button
        st.download_button(
            label="Download LHPT Results",
            data=csv,
            file_name="processed_lhpt_data.csv",
            mime="text/csv"
        )
        
        # Show success message
        st.success("LHPT Processing complete! Click the button above to download your CSV file.")
        
        # Display preview of the data
        st.write("Preview of processed LHPT data:")
        st.dataframe(df_analyzed.head())

else:  # Process LHP2DK
    st.header('LHP2DK PDF Processor')
    
    # Functions for LHP2DK processing
    def extract_data_penguji(text):
        start = text.find("Data Penguji")
        end = text.find("2. Indikasi dan Modus Ketidakpatuhan")
        if start == -1 or end == -1:
            return None
        data_penguji_section = text[start:end]

        rows = re.findall(r"(\d+)\.\s(.*?)\s(\d+)", data_penguji_section)
        if rows:
            df = pd.DataFrame(rows, columns=["No", "Jenis Data", "Jumlah Data"])
            return df
        return None

    def extract_potensi(text):
        potensi_section = re.search(r"3\. Potensi\s(.*?)4\. Kemampuan", text, re.DOTALL)
        if not potensi_section:
            return None

        potensi_text = potensi_section.group(1)
        potensi_rows = re.findall(
            r"(\d+)\.\s([\d\s-]+.*?)\s(\d+)\s(\d{6})\s([\d.,]+)\s([\d.,]+)",
            potensi_text
        )
        if potensi_rows:
            df = pd.DataFrame(potensi_rows, columns=[
                "No", "Jenis Pajak", "Kode Jenis Setor", "Masa Pajak", "Potensi Awal", "Potensi Akhir"
            ])
            df["Potensi Awal"] = df["Potensi Awal"].str.replace(".", "", regex=False).astype(float)
            df["Potensi Akhir"] = df["Potensi Akhir"].str.replace(".", "", regex=False).astype(float)
            return df
        return None

    def extract_additional_columns(text):
        indikasi = re.search(r"Indikasi Ketidakpatuhan\s(.*?)(Modus Ketidakpatuhan)", text, re.DOTALL)
        modus = re.search(r"2\.\sModus Ketidakpatuhan(.*?)(3\. Potensi)", text, re.DOTALL)
        kemampuan = re.search(r"Kemampuan Wajib Pajak untuk Membayar Ketetapan Pajak\s*:\s*(\w+)", text)
        rekomendasi = re.search(r"direkomendasikan tindak lanjut berupa\s*:\s*(.*?)\n", text, re.DOTALL)

        return (
            indikasi.group(1).strip() if indikasi else None,
            modus.group(1).strip() if modus else None,
            kemampuan.group(1) if kemampuan else None,
            rekomendasi.group(1).strip() if rekomendasi else None
        )

    def process_lhp2dk_file(uploaded_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            with pdfplumber.open(tmp_file_path) as pdf:
                text = " ".join(page.extract_text() for page in pdf.pages)

            # Extract data
            data_penguji_df = extract_data_penguji(text)
            potensi_df = extract_potensi(text)
            indikasi, modus, kemampuan, rekomendasi = extract_additional_columns(text)
            
            # Extract NOMOR_LHPT from filename
            nomor_lhpt = re.search(r"(\d+)", uploaded_file.name).group(1) if re.search(r"(\d+)", uploaded_file.name) else "UNKNOWN"
            
            # Calculate totals
            total_potensi_awal = potensi_df["Potensi Awal"].sum() if potensi_df is not None else 0
            total_potensi_akhir = potensi_df["Potensi Akhir"].sum() if potensi_df is not None else 0
            
            return {
                "Jenis Data": "; ".join(data_penguji_df["Jenis Data"]) if data_penguji_df is not None else "",
                "NOMOR_LHPT": nomor_lhpt,
                "Indikasi Ketidakpatuhan": indikasi,
                "Modus Ketidakpatuhan": modus,
                "Kemampuan WP": kemampuan,
                "Rekomendasi Tindak Lanjut": rekomendasi,
                "Total Potensi Awal": total_potensi_awal,
                "Total Potensi Akhir": total_potensi_akhir
            }
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            return None
        finally:
            os.unlink(tmp_file_path)

    # File uploader for LHP2DK
    uploaded_files = st.file_uploader("Upload LHP2DK PDF files", type=['pdf'], accept_multiple_files=True)

    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process each PDF file
        all_data = []
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            if "lhp2dk" in uploaded_file.name.lower():
                extracted_data = process_lhp2dk_file(uploaded_file)
                if extracted_data:
                    all_data.append(extracted_data)
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        if all_data:
            # Create DataFrame
            df = pd.DataFrame(all_data)
            
            # Convert DataFrame to CSV
            csv = df.to_csv(index=False)
            
            # Create download button
            st.download_button(
                label="Download LHP2DK Results",
                data=csv,
                file_name="processed_lhp2dk_data.csv",
                mime="text/csv"
            )
            
            # Show success message
            st.success("LHP2DK Processing complete! Click the button above to download your CSV file.")
            
            # Display preview of the data
            st.write("Preview of processed LHP2DK data:")
            st.dataframe(df.head())
        else:
            st.warning("No valid LHP2DK files were processed. Please check your files and try again.")

