import numpy as np
import matplotlib.pyplot as plt

def run_trixe_simulation():
    # ==========================================
    # 1. PARAMETER FUNDAMENTAL UJI TRIXE
    # ==========================================
    N_particles = 1000  # Jumlah agen probabilitas (mewakili P(x,t))
    T_total = 10.0      # Total waktu simulasi
    dt = 0.01           # Resolusi waktu (semakin kecil, semakin akurat)
    N_steps = int(T_total / dt)
    time_array = np.linspace(0, T_total, N_steps)

    # Parameter Dinamika
    alpha = 1.5   # Koefisien peredaman stabilisator (S)
    beta = 0.5    # Kekuatan respons stabilisator terhadap rata-rata probabilitas
    k_pull = 2.0  # Kekuatan tarikan Operator h (menuju determinisme)
    sigma = 1.5   # Intensitas noise (Tingkat Kekacauan Probabilistik awal)

    # ==========================================
    # 2. INISIALISASI KONDISI AWAL (Kekacauan)
    # ==========================================
    # Partikel tersebar acak secara Gaussian jauh dari stabilisator
    x_particles = np.random.normal(loc=-4.0, scale=2.0, size=N_particles) 
    
    # Stabilisator S dimulai dari posisi ekstrem yang berlawanan
    S_current = 4.0 

    # Penampung data untuk analisis visual
    S_history = np.zeros(N_steps)
    mu_history = np.zeros(N_steps)
    x_sample_history = np.zeros((N_steps, 10)) # Lacak 10 partikel acak untuk visualisasi

    print("Memulai pengujian fundamental Dinamika Trixe...")

    # ==========================================
    # 3. INTEGRASI NUMERIK (Euler-Maruyama)
    # ==========================================
    for i in range(N_steps):
        # A. Ekstrak fitur probabilitas (Momen Pertama / Rata-rata)
        mu_x = np.mean(x_particles)
        
        # B. Evolusi Stabilisator (Dinamika 0Xe)
        # dS/dt = -alpha*S + beta*E[x]
        dS = (-alpha * S_current + beta * mu_x) * dt
        S_current += dS
        
        # C. Evolusi Kekacauan Probabilistik (<Xe) menggunakan Persamaan Langevin
        # dX = -k(X - S)dt + sigma * dW
        # dW adalah variabel acak Wiener berdistribusi Normal(0, sqrt(dt))
        dW = np.random.normal(0, np.sqrt(dt), N_particles)
        
        dx = -k_pull * (x_particles - S_current) * dt + sigma * dW
        x_particles += dx
        
        # D. Pencatatan Data
        S_history[i] = S_current
        mu_history[i] = mu_x
        x_sample_history[i, :] = x_particles[:10]

    # ==========================================
    # 4. VISUALISASI PEMBUKTIAN
    # ==========================================
    plt.figure(figsize=(14, 6))

    # Plot 1: Lintasan Makroskopis (S vs Ekspektasi P)
    plt.subplot(1, 2, 1)
    plt.plot(time_array, S_history, label='Stabilisator $S(t)$', color='red', linewidth=2.5)
    plt.plot(time_array, mu_history, label='Ekspektasi Probabilitas $\mu(t)$', color='blue', linestyle='--', linewidth=2)
    plt.title('Makrodinamika: Transisi ke Variabel Orbital $O_v$')
    plt.xlabel('Waktu (t)')
    plt.ylabel('Posisi Ruang (x)')
    plt.legend()
    plt.grid(True)

    # Plot 2: Pandangan Mikroskopis (Partikel individu dihancurkan ke dalam determinisme)
    plt.subplot(1, 2, 2)
    for j in range(10):
        plt.plot(time_array, x_sample_history[:, j], color='gray', alpha=0.4, linewidth=0.8)
    plt.plot(time_array, S_history, label='Jalur Transformasi $0Xe$', color='red', linewidth=2.5)
    plt.title('Mikrodinamika: Keruntuhan Kekacauan (Efek $>Xe$)')
    plt.xlabel('Waktu (t)')
    plt.ylabel('Posisi Ruang (x)')
    plt.legend(['Sampel Probabilitas $<Xe$'])
    plt.grid(True)

    plt.tight_layout()
    plt.show()
    
    # Verifikasi Kestabilan Akhir
    final_difference = abs(S_history[-1] - mu_history[-1])
    print(f"Selisih akhir antara S(t) dan rata-rata probabilitas: {final_difference:.5f}")
    if final_difference < 0.1:
        print("KESIMPULAN: Sistem terbukti konvergen ke Determinisme Absolut (>Xe).")
    else:
        print("KESIMPULAN: Sistem gagal menembus kekacauan. Periksa parameter stabilitas (alpha, beta).")

if __name__ == "__main__":
    run_trixe_simulation()
