import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Konfigurasi Halaman
st.set_page_config(page_title="Regula Falsi Calculator", layout="wide", page_icon="⚡")

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #f5f7fa; }
        .title { text-align: center; font-size: 42px; color: #2b5876; font-weight: bold; padding-bottom: 10px; }
        .subtitle { text-align: center; font-size: 20px; color: #4a6572; margin-bottom: 30px; }
        .card { padding: 25px; border-radius: 15px; background: white; border: 1px solid #e0e6ed; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .result-box { padding: 20px; border-radius: 10px; background-color: #e8f5e9; color: #1b5e20; border-left: 5px solid #4caf50; font-size: 18px; }
        .footer { margin-top: 50px; text-align: center; color: #7b8794; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='title'>⚡ Metode Regula Falsi – Root Finder</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Aplikasi profesional untuk mencari akar persamaan non-linear secara numerik</div>", unsafe_allow_html=True)

# Sidebar / Input Area
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Input Parameter")
    
    fungsi_input = st.text_input("Masukkan Fungsi f(x):", "x**3 - x - 2", help="Contoh: x**3 - x - 2 atau np.sin(x)")
    a_input = st.number_input("Batas bawah (a):", value=1.0, format="%.4f")
    b_input = st.number_input("Batas atas (b):", value=2.0, format="%.4f")
    toleransi = st.number_input("Toleransi error:", value=0.0001, format="%.6f")
    max_iter = st.slider("Maksimum Iterasi:", 10, 100, 50)

    hitung = st.button("🔍 Hitung Akar Sekarang", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ℹ️ Prinsip Kerja")
    st.write("Metode **Regula Falsi** (Posisi Palsu) mencari akar dengan menghubungkan titik $f(a)$ dan $f(b)$ dengan garis lurus (sekant). Titik potong garis tersebut dengan sumbu $x$ menjadi estimasi akar baru ($c$).")
    st.latex(r"c = b - \frac{f(b)(b - a)}{f(b) - f(a)}")
    st.markdown("</div>", unsafe_allow_html=True)

# Fungsi Evaluasi
def f(x):
    # Memungkinkan penggunaan fungsi numpy seperti np.sin, np.exp, dll
    return eval(fungsi_input, {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp, "log": np.log})

# Logika Perhitungan
if hitung:
    try:
        a, b = a_input, b_input
        fa, fb = f(a), f(b)
        
        if fa * fb >= 0:
            st.error("⚠️ Kesalahan: f(a) dan f(b) harus memiliki tanda berbeda (f(a)*f(b) < 0). Pilih rentang lain!")
        else:
            data = []
            akar_ditemukan = None
            
            for i in range(max_iter):
                fa, fb = f(a), f(b)
                c = b - (fb * (b - a)) / (fb - fa)
                fc = f(c)
                
                data.append({"Iterasi": i+1, "a": a, "b": b, "c": c, "f(a)": fa, "f(b)": fb, "f(c)": fc})
                
                if abs(fc) < toleransi:
                    akar_ditemukan = c
                    break
                
                # Update batas
                if fa * fc < 0:
                    b = c
                else:
                    a = c
            
            df = pd.DataFrame(data)

            # --- DISPLAY HASIL ---
            st.divider()
            res_col, gra_col = st.columns([1, 1])

            with res_col:
                st.markdown("### ✅ Hasil Akhir")
                if akar_ditemukan is not None:
                    st.markdown(f"""
                    <div class='result-box'>
                        Akar ditemukan pada x ≈ <b>{akar_ditemukan:.6f}</b><br>
                        Nilai f(x) ≈ {f(akar_ditemukan):.8f}<br>
                        Total Iterasi: {len(df)}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Iterasi maksimum tercapai tanpa memenuhi toleransi.")
                
                st.markdown("### 📊 Tabel Iterasi")
                st.dataframe(df.style.format("{:.6f}"), use_container_width=True)

            with gra_col:
                st.markdown("### 📈 Visualisasi")
                
                # Plot Konvergensi
                fig, ax = plt.subplots(2, 1, figsize=(8, 10))
                
                # Subplot 1: Nilai c per iterasi
                ax[0].plot(df["Iterasi"], df["c"], marker='o', color='#2b5876')
                ax[0].set_title("Konvergensi Nilai c")
                ax[0].set_xlabel("Iterasi")
                ax[0].set_ylabel("Estimasi Akar (c)")
                ax[0].grid(True, linestyle='--', alpha=0.6)

                # Subplot 2: Fungsi f(x)
                x_vals = np.linspace(a_input - 1, b_input + 1, 200)
                y_vals = [f(val) for val in x_vals]
                ax[1].plot(x_vals, y_vals, color='#e67e22', label=f"f(x) = {fungsi_input}")
                ax[1].axhline(0, color='black', lw=1)
                if akar_ditemukan:
                    ax[1].scatter([akar_ditemukan], [0], color='red', zorder=5, label="Akar")
                ax[1].set_title("Grafik Fungsi f(x)")
                ax[1].legend()
                ax[1].grid(True, linestyle='--', alpha=0.6)
                
                plt.tight_layout()
                st.pyplot(fig)

    except Exception as e:
        st.error(f"Terjadi kesalahan dalam ekspresi matematika: {e}")

st.markdown("<div class='footer'>Dibuat dengan ❤️ menggunakan Streamlit • Regula Falsi Engine v2.0</div>", unsafe_allow_html=True)
