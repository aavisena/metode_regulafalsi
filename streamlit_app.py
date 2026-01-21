import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="Regula Falsi Calculator", layout="wide", page_icon="⚡")

# ================= STYLE =================
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 42px;
    color: #2b5876;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    font-size: 20px;
    color: #4a6572;
}
.card {
    padding: 20px;
    border-radius: 20px;
    background: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}
.result {
    padding: 15px;
    border-radius: 10px;
    background-color: #e8f5e9;
    color: #1b5e20;
    font-size: 20px;
}
.footer {
    margin-top: 30px;
    text-align: center;
    color: #7b8794;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>Aplikasi Web Metode Regula Falsi</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Fikri Zaki Avisena Design</div>", unsafe_allow_html=True)
st.write("---")

# ================= INPUT =================
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    fungsi = st.text_input("Masukkan Fungsi f(x):", "x**3 - x - 2")
    a = st.number_input("Batas bawah (a):", value=1.0)
    b = st.number_input("Batas atas (b):", value=2.0)
    toleransi = st.number_input("Toleransi error:", value=0.0001)
    hitung = st.button("🔍 Hitung Akar", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("Metode Regula Falsi menggunakan garis sekant untuk mendekati akar persamaan.")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= FUNCTION =================
def f(x):
    return eval(fungsi, {"x": x, "math": math})

# ================= RESULT AREA (SELALU ADA) =================
colR1, colR2 = st.columns([1.2, 1])

akar = None
data = []

# ================= PROCESS =================
if hitung:
    try:
        a_local = a
        b_local = b
        iterasi = 0

        if f(a_local) * f(b_local) > 0:
            st.error("f(a) dan f(b) harus berlainan tanda")
        else:
            while iterasi <= 100:
                fa = f(a_local)
                fb = f(b_local)
                c = b_local - fb * (b_local - a_local) / (fb - fa)
                fc = f(c)

                data.append([iterasi, a_local, b_local, c, fa, fb, fc])

                if abs(fc) < toleransi:
                    akar = c
                    break

                if fa * fc < 0:
                    b_local = c
                else:
                    a_local = c

                iterasi += 1

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")

# ================= OUTPUT =================
with colR1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ✅ Hasil Perhitungan")

    if hitung and akar is not None:
        st.markdown(f"<div class='result'>Akar ditemukan:<br><b>{akar}</b></div>", unsafe_allow_html=True)
    elif hitung:
        st.warning("Akar tidak ditemukan")
    else:
        st.info("Tekan tombol **Hitung Akar**")

    st.markdown("</div>", unsafe_allow_html=True)

if len(data) > 0:
    df = pd.DataFrame(data, columns=["Iterasi", "a", "b", "c", "f(a)", "f(b)", "f(c)"])

    with colR1:
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

st.markdown("<div class='footer'>Aplikasi Web Metode Regula Falsi</div>", unsafe_allow_html=True)
