import streamlit as st
st.set_page_config(
    page_title="Regula Falsi App",
    page_icon="⚡",
    layout="wide"
)
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

h1 {
    text-align: center;
    font-weight: 800;
    font-size: 42px !important;
    color: #ffffff;
}

.header-box {
    background: linear-gradient(90deg, #2b5876, #4e4376);
    padding: 40px 10px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.subtext {
    text-align: center;
    color: #eeeeee;
    font-size: 18px;
}

.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.08);
}

.result-box {
    background: #e8f5e9;
    padding: 15px;
    border-left: 6px solid #1b5e20;
    border-radius: 8px;
    font-size: 18px;
}

.footer {
    margin-top: 40px;
    text-align: center;
    color: #777;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>⚡ Metode Regula Falsi</h1>
    <p class="subtext">Aplikasi profesional untuk mencari akar persamaan non-linear</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("⚙ Pengaturan Aplikasi")
st.sidebar.info("Gunakan menu ini untuk mengatur parameter perhitungan Regula Falsi.")
st.sidebar.write("Developer: Akbar Maulana")

st.markdown("### 🧮 Input Parameter")
with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        fungsi = st.text_input("Masukkan Fungsi f(x):", "x**3 - x - 2")

    with col2:
        a = st.number_input("Batas bawah (a):", value=1.0)

    with col3:
        b = st.number_input("Batas atas (b):", value=2.0)

tol = st.number_input("Toleransi Error:", value=0.0001)

btn = st.button("🔍 Hitung Akar", use_container_width=True)

def f(x): 
    return eval(fungsi)

if btn:
    st.markdown("### 📌 Hasil Perhitungan")

    iterasi = 0
    data = []

    while True:
        fa = f(a)
        fb = f(b)
        c = b - (fb * (b - a)) / (fb - fa)
        fc = f(c)

        data.append([iterasi, a, b, c, fa, fb, fc])

        if abs(fc) < tol:
            akar = c
            break

        if fa * fc < 0:
            b = c
        else:
            a = c

        iterasi += 1
        if iterasi >= 100:
            akar = None
            break

    if akar is not None:
        st.markdown(
            f"<div class='result-box'>Akar ditemukan pada: <b>{akar}</b></div>",
            unsafe_allow_html=True,
        )
    else:
        st.error("❌ Akar tidak ditemukan hingga 100 iterasi.")

    df = pd.DataFrame(data, columns=["Iterasi", "a", "b", "c", "f(a)", "f(b)", "f(c)"])
    st.markdown("### 📊 Tabel Iterasi")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 📈 Grafik Konvergensi Akar")
    plt.figure(figsize=(7,4))
    plt.plot(df["Iterasi"], df["c"], marker="o")
    plt.xlabel("Iterasi")
    plt.ylabel("Nilai c")
    plt.title("Grafik Konvergensi Metode Regula Falsi")
    st.pyplot(plt)

st.markdown("""
<div class="footer">
    Dibuat dengan ❤ oleh Akbar Maulana • Streamlit Regula Falsi UI Modern Edition
</div>
""", unsafe_allow_html=True)
