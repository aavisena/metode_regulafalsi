import streamlit as st
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Regula Falsi Calculator", layout="wide", page_icon="⚡")

# ================== STYLE ==================
st.markdown("""
<style>
.title { text-align:center; font-size:42px; font-weight:bold; color:#2b5876; }
.subtitle { text-align:center; font-size:20px; color:#4a6572; }
.card {
    padding:20px;
    border-radius:20px;
    background:white;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
}
.result {
    padding:15px;
    border-radius:10px;
    background:#e8f5e9;
    color:#1b5e20;
    font-size:20px;
}
.footer {
    margin-top:30px;
    text-align:center;
    color:#7b8794;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>⚡ Metode Regula Falsi</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Aplikasi Web Pencari Akar Persamaan Non-Linear</div>", unsafe_allow_html=True)
st.write("---")

# ================== INPUT ==================
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Input Parameter")

    fungsi_input = st.text_input("Masukkan fungsi f(x):", "x**3 - x - 2")
    a = st.number_input("Batas bawah (a):", value=1.0)
    b = st.number_input("Batas atas (b):", value=2.0)
    toleransi = st.number_input("Toleransi error:", value=0.0001, format="%.6f")
    max_iter = st.number_input("Iterasi maksimum:", value=100)

    hitung = st.button("🔍 Hitung Akar", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ℹ️ Informasi Metode")
    st.write("""
Metode **Regula Falsi** menggunakan interpolasi linier
untuk mencari akar persamaan non-linear.
""")
    st.markdown("</div>", unsafe_allow_html=True)

# ================== PROSES ==================
if hitung:
    x = sp.symbols('x')

    try:
        fx_expr = sp.sympify(fungsi_input)
        f = sp.lambdify(x, fx_expr, "numpy")

        if f(a) * f(b) > 0:
            st.error("❌ f(a) dan f(b) harus berlainan tanda.")
        else:
            data = []
            a0, b0 = a, b

            for i in range(1, max_iter + 1):
                fa = f(a0)
                fb = f(b0)

                c = b0 - fb * (b0 - a0) / (fb - fa)
                fc = f(c)

                data.append([i, a0, b0, c, fa, fb, fc])

                if abs(fc) < toleransi:
                    akar = c
                    break

                if fa * fc < 0:
                    b0 = c
                else:
                    a0 = c
            else:
                akar = None

            colR1, colR2 = st.columns(2)

            with colR1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### ✅ Hasil Perhitungan")

                if akar is not None:
                    st.markdown(
                        f"<div class='result'>Akar ditemukan:<br><b>{akar:.6f}</b></div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.error("Akar tidak ditemukan.")
                st.markdown("</div>", unsafe_allow_html=True)

                df = pd.DataFrame(
                    data,
                    columns=["Iterasi", "a", "b", "c", "f(a)", "f(b)", "f(c)"]
                )

                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📊 Tabel Iterasi")
                st.dataframe(df, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with colR2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("### 📈 Grafik Konvergensi")

                fig, ax = plt.subplots()
                ax.plot(df["Iterasi"], df["c"], marker="o")
                ax.set_xlabel("Iterasi")
                ax.set_ylabel("Nilai c")
                ax.set_title("Konvergensi Regula Falsi")
                st.pyplot(fig)

                st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

st.markdown("<div class='footer'>Dibuat dengan ❤️ menggunakan Streamlit</div>", unsafe_allow_html=True)
