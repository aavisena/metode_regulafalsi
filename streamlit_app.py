import streamlit as st

st.set_page_config(page_title="Regula Falsi Calculator", layout="wide", page_icon="⚡")

st.markdown(
    """
    <style>
        body { background-color: #f5f7fa; }
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
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='title'>⚡ Metode Regula Falsi – Root Finder App</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Aplikasi profesional untuk mencari akar persamaan non-linear</div>", unsafe_allow_html=True)


st.write("---")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Input Parameter")


    fungsi = st.text_input("Masukkan Fungsi f(x):", "x**3 - x - 2")
    a = st.number_input("Batas bawah (a):", value=1.0)
    b = st.number_input("Batas atas (b):", value=2.0)
    toleransi = st.number_input("Toleransi error:", value=0.0001)


    hitung = st.button("🔍 Hitung Akar", use_container_width=True)


    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ℹ Informasi Metode")
    st.write(
        "Metode Regula Falsi (False Position) menggunakan garis sekant untuk memperkirakan akar persamaan f(x)."
    )
    st.write("""
    *Kelebihan:*
    - Lebih stabil dibanding metode sekant
    - Tidak memerlukan turunan f(x)


    *Kekurangan:*
    - Lebih lambat dibanding Newton-Raphson
    - Bisa stagnan pada beberapa kasus
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
def f(x):
    return eval(fungsi)

if hitung:
    st.write("---")


    colR1, colR2 = st.columns([1.2, 1])


    iterasi = 0
    data = []


    while True:
        fa = f(a)
        fb = f(b)
        c = b - (fb * (b - a)) / (fb - fa)
        fc = f(c)
        
        data.append([iterasi, a, b, c, fa, fb, fc])

        if abs(fc) < toleransi:
            akar = c
            break
            
        if fa * fc < 0:
            b = c
        else:
            a = c
            
        iterasi += 1
        if iterasi > 100:
            akar = None
            break

colR1, colR2 = st.columns(2)

akar = None
data = []

if hitung:  
    
    a_local = a
    b_local = b

    iterasi = 0
    data = []
    
    while True:
        fa = f(a_local)
        fb = f(b_local)

        denom = (fb - fa)
        if denom == 0:
            akar = None
            break

        c = b_local - fb * (b_local - a_local) / denom
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
        if iterasi > 100:
            akar = None
            break

with colR1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ✅ Hasil Perhitungan")

    if akar is not None:
        st.markdown(
            f"<div class='result'>Akar ditemukan pada:<br><b>{akar}</b></div>",
            unsafe_allow_html=True
        )
    else:
        if hitung:
            st.error("Akar tidak ditemukan dalam 100 iterasi atau interval tidak valid.")
        else:
            st.info("Tekan tombol 'Hitung Akar' untuk memulai perhitungan.")

    st.markdown("</div>", unsafe_allow_html=True)

data = []

if data:
    df = pd.DataFrame(data, columns=["Iterasi", "a", "b", "c", "f(a)", "f(b)", "f(c)"])
    
    
    with colR1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📊 Tabel Iterasi")
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
       
    with colR2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📈 Grafik Konvergensi Akar")
        
        fig, ax = plt.subplots()
        ax.plot(df["Iterasi"], df["c"], marker="o")
        ax.set_xlabel("Iterasi")
        ax.set_ylabel("Nilai c (perkiraan akar)")
        ax.set_title("Grafik Konvergensi Metode Regula Falsi")
        st.pyplot(fig, clear_figure=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    with colR1:
        st.info("Tabel iterasi akan muncul setelah perhitungan selesai.")
    with colR2:
        st.info("Grafik konvergensi akan muncul setelah perhitungan selesai.")

st.markdown("<div class='footer'>Dibuat dengan ❤ menggunakan Streamlit • Regula Falsi Professional Edition</div>", unsafe_allow_html=True)

# --- DARK MODE & DASHBOARD VERSION BELOW WILL BE ADDED ---
