from flask import Flask, render_template, request
import random

app = Flask(__name__)

# --- FUNGSI SIMULASI SCRAPING / PENGUMPULAN DATA ---
# Catatan: Dalam aplikasi nyata, data ini didapat menggunakan 'requests' dan 'BeautifulSoup'
# ke website target (misal: website kemdikbud, jobstreet, dll).
# Di sini saya buat simulasi data agar kode langsung bisa jalan tanpa error koneksi.

def scrape_materi(kategori):
    # Simulasi mengambil data materi belajar
    data = []
    subjects = ["Matematika", "Bahasa Indonesia", "Logika", "Pengetahuan Umum"]
    for i in range(1, 6):
        data.append({
            "judul": f"Paket Soal {kategori} {subjects[i%4]} - Latihan {i}",
            "sumber": "Bank Soal Nasional",
            "link": "#",
            "deskripsi": f"Latihan soal intensif untuk persiapan {kategori} tahun 2025."
        })
    return data

def scrape_universitas():
    # Simulasi data universitas & passing grade
    return [
        {"nama": "Universitas Indonesia", "jurusan": "Ilmu Komputer", "ketetatan": "1.2%", "lokasi": "Depok"},
        {"nama": "Institut Teknologi Bandung", "jurusan": "Teknik Informatika", "ketetatan": "1.5%", "lokasi": "Bandung"},
        {"nama": "Universitas Gadjah Mada", "jurusan": "Kedokteran", "ketetatan": "0.8%", "lokasi": "Yogyakarta"},
        {"nama": "Universitas Airlangga", "jurusan": "Farmasi", "ketetatan": "2.1%", "lokasi": "Surabaya"},
        {"nama": "Institut Teknologi Sepuluh Nopember", "jurusan": "Sistem Informasi", "ketetatan": "1.9%", "lokasi": "Surabaya"},
    ]

def scrape_lowongan():
    # Simulasi scraping lowongan kerja
    return [
        {"posisi": "Data Entry Magang", "perusahaan": "Tech Indo", "gaji": "Rp 2.5jt", "lokasi": "Jakarta"},
        {"posisi": "Admin Media Sosial", "perusahaan": "Creative Agency", "gaji": "Rp 3.0jt", "lokasi": "Remote"},
        {"posisi": "Junior Programmer", "perusahaan": "Startup A", "gaji": "Rp 5.5jt", "lokasi": "Bandung"},
    ]

# --- LOGIKA AI SEDERHANA (PYTHON) ---
def analisa_minat_bakat(nilai_mtk, nilai_bh, minat):
    # Ini adalah logika Python sederhana untuk rekomendasi
    skor = 0
    rekomendasi = []
    
    if minat == "teknik" and int(nilai_mtk) > 80:
        rekomendasi = ["Teknik Informatika", "Sistem Informasi", "Teknik Sipil"]
    elif minat == "kesehatan" and int(nilai_mtk) > 75:
        rekomendasi = ["Kedokteran", "Farmasi", "Kesehatan Masyarakat"]
    elif minat == "sosial":
        rekomendasi = ["Ilmu Komunikasi", "Hubungan Internasional", "Hukum"]
    else:
        rekomendasi = ["Manajemen", "Akuntansi", "Administrasi Bisnis"]
        
    return rekomendasi

# --- ROUTING (ALAMAT WEBSITE) ---

@app.route('/')
def home():
    return render_template('base.html') # Menggunakan file index.html Anda yang sudah dimodif

@app.route('/materi/<tipe>')
def materi_page(tipe):
    # Menangani TKA, SNBT, Kedinasan
    judul_halaman = f"Materi Persiapan {tipe.upper()}"
    data_hasil = scrape_materi(tipe.upper())
    return render_template('page_list.html', judul=judul_halaman, data=data_hasil, tipe="materi")

@app.route('/universitas-favorit')
def univ_page():
    judul_halaman = "Daftar Universitas & Jurusan Favorit"
    data_hasil = scrape_universitas()
    return render_template('page_list.html', judul=judul_halaman, data=data_hasil, tipe="univ")

@app.route('/pekerjaan')
def pekerjaan_page():
    judul_halaman = "Lowongan & Tren Pekerjaan"
    data_hasil = scrape_lowongan()
    return render_template('page_list.html', judul=judul_halaman, data=data_hasil, tipe="kerja")

@app.route('/jurusan-cocok', methods=['GET', 'POST'])
def ai_page():
    hasil = None
    if request.method == 'POST':
        # Ambil data dari form HTML
        nilai_mtk = request.form.get('nilai_mtk')
        nilai_bhs = request.form.get('nilai_bhs')
        minat = request.form.get('minat')
        
        # Proses dengan Python
        hasil = analisa_minat_bakat(nilai_mtk, nilai_bhs, minat)
        
    return render_template('ai_form.html', hasil=hasil)

if __name__ == '__main__':
    app.run(debug=True)