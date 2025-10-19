
ILTEC — Lab Virtual Fisika
Paket: Pemantulan & Pembiasan Cahaya (10 simulasi)
Dikembangkan oleh: Dr. Apit Fathurohman, S.Pd., M.Si.

Isi paket:
- simulasi_fisika.py   -> Streamlit app (jalankan dengan `streamlit run simulasi_fisika.py`)
- index.html           -> Halaman embed untuk website ILTEC (ganti iframe src)
- README.txt           -> Panduan ini

Petunjuk singkat menjalankan (local / server):
1. Siapkan Python 3.8+ dan pip.
2. (Opsional) buat virtualenv:
   python -m venv venv
   source venv/bin/activate  (Linux/Mac)  atau  venv\Scripts\activate (Windows)
3. Pasang dependensi (opsional: reportlab untuk PDF):
   pip install streamlit matplotlib numpy reportlab
   Jika tidak ingin PDF, Anda boleh melewatkan reportlab; aplikasi akan menyediakan file .txt sebagai fallback.
4. Jalankan aplikasi:
   streamlit run simulasi_fisika.py
5. Untuk menayangkan di website ILTEC:
   - Deploy ke Streamlit Cloud (https://streamlit.io/cloud) atau server yang mendukung.
   - Ambil URL publik dan tempelkan ke <iframe src="YOUR_APP_URL"></iframe> pada index.html.
6. Jika menggunakan WordPress, buat halaman baru dan masukkan kode iframe (pastikan WordPress mengizinkan iframe/embedding).

Kontak pengembang / edit:
- Ganti teks "Dikembangkan oleh..." pada simulasi_fisika.py bila ingin tampilan lain.
