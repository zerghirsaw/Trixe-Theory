# Trixe-Theory: Dinamika Trixe (T)

**Kerangka Kerja Matematis untuk Transformasi Informasi dari Kekacauan Probabilistik ke Determinisme Absolut**

**Penulis:** Muhammad Rifat Qolby Almusawa (*Independent Researcher*)

---

## 📌 Abstrak Singkat
Repositori ini berisi naskah pracetak (*preprint*) dan kode simulasi numerik untuk **Model Trixe**. 

Model Trixe memperkenalkan sebuah arsitektur tripartit yang menghubungkan:
1. **$<Xe$ (Domain Probabilistik):** Kekacauan stokastik yang dimodelkan melalui persamaan Langevin dan Fokker-Planck.
2. **$0Xe$ (Mekanisme Stabilisasi):** Jalur transisi menuju Variabel Orbital ($O_v$).
3. **$>Xe$ (Singularitas Informasi):** Operator transformasi yang meruntuhkan entropi probabilitas menjadi kepastian absolut.

Verifikasi numerik di dalam repositori ini juga mendemonstrasikan ambang batas kritis (Titik Bifurkasi) di mana sistem dapat gagal mempertahankan determinisme dan mengalami *runaway feedback* jika gaya respons entropi melampaui daya redam sistem.

## 📂 Struktur Repositori
- `📄 article`  : Dokumen naskah lengkap (format *Preprint* akademis).
- `📝 latex` : Kode sumber LaTeX dari naskah lengkap.
- `🐍 test` : Skrip Python untuk simulasi numerik berbasis metode *Euler-Maruyama*.

## 🔬 Menjalankan Simulasi Numerik
Skrip simulasi `trixe_sim.py` digunakan untuk memvalidasi transisi makrodinamika dan mikrodinamika sistem, serta menguji titik runtuh (*collapse*) dari teori ini.

### Persyaratan Sistem (Dependencies)
Pastikan Anda telah menginstal pustaka Python berikut:
```bash
pip install numpy matplotlib scipy
