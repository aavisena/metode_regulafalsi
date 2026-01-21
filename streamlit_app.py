import streamlit as st
import sympy as sp
import pandas as pd
import numpy as np
import matplolib.pyplot as plt

st.set_page_config(page_title="SPNL - Regula Falsi", layout="centered")

st.title("Aplikasi Web Solusi SPNL")
st.subheader("Metode Regula Falsi")

st.markdown("""
Metode **Regula Falsi** digunakan untuk mencari akar persamaan non-linear  
dengan pendekatan interpolasi linier.
""")

# -------------------------
# INPUT
# -------------------------
fungsi_input = st.text_input("Masukkan persamaan f(x)", "x**3 - x - 2")

a = st.number_input("Nilai awal a", value=1.0)
b = st.number_input("Nilai awal b", value=2.0)
toleransi = st.number_input("Toleransi error", value=0.0001, format="%.6f")
maks_iterasi = st.number_input("Iterasi maksimum", value=50)

x = sp.symbols('x')

if st.button("Hitung Solusi"):
    try:
        f_expr = sp.sympify(fungsi_input)
        f = sp.lambdify(x, f_expr, "numpy")

        if f(a) * f(b) > 0:
            st.error("Syarat tidak terpenuhi: f(a) dan f(b) harus berlainan tanda.")
        else:
            hasil = []
            c_lama = 0

            for i in range(1, maks_iterasi + 1):
                c = b - (f(b) * (a - b)) / (f(a) - f(b))
                error = abs(c - c_lama)

                hasil.append([i, a, b, c, f(c), error])
                
                if error < toleransi:
                    break

                if f(a) * f(c) < 0:
                    b = c
                else:
                    a = c

                c_lama = c

            df = pd.DataFrame(
                hasil,
                columns=["Iterasi", "a", "b", "c", "f(c)", "Error"]
            )

            st.success(f"Solusi ditemukan: x ≈ {c:.6f}")
            st.dataframe(df)
            
            # -------------------------
            # GRAFIK
            # -------------------------
            x_plot = np.linspace(a - 1, b + 1, 400)
            y_plot = f(x_plot)

            fig, ax = plt.subplots()
            ax.axhline(0, color="black")
            ax.plot(x_plot, y_plot, label="f(x)")
            ax.scatter(c, f(c), color="red", label="Akar")
            ax.legend()
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title("Grafik Fungsi dan Akar")
            
            st.pyplot(fig)

    except:
        st.error("Terjadi kesalahan pada input fungsi.")

# --- DARK MODE & DASHBOARD VERSION BELOW WILL BE ADDED ---
