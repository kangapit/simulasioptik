import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import datetime

st.set_page_config(page_title="Simulasi Pemantulan & Pembiasan - ILTEC", layout="wide")
# Header like ILTEC
st.markdown("""
<div style="display:flex;align-items:center;gap:12px;">
  <img src="https://raw.githubusercontent.com/openai/branding/main/logo.png" width="60" style="border-radius:6px;">
  <div>
    <h2 style="margin:0;color:#0b5fa5;">ILTEC — Lab Virtual Fisika</h2>
    <div style="color:#0b5fa5;">Simulasi Pemantulan & Pembiasan (untuk calon guru fisika)</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("**Dikembangkan oleh: Dr. Apit Fathurohman, S.Pd., M.Si.**")
st.write("Pilih simulasi lewat menu di samping. Setiap simulasi dilengkapi keterangan konsep dan rumus.")

menu = st.sidebar.selectbox("Pilih Simulasi:", [
    "1. Cermin Datar",
    "2. Cermin Cekung",
    "3. Cermin Cembung",
    "4. Pembiasan Dua Medium (Snellius)",
    "5. Sudut Kritis & TIR",
    "6. Prisma Segitiga (Deviasi)",
    "7. Lensa Cekung",
    "8. Lensa Cembung",
    "9. Sistem Lensa + Cermin",
    "10. Dispersi Cahaya Putih"
])

def draw_mirror_flat(theta_i_deg):
    plt.figure(figsize=(5,4))
    theta = np.radians(theta_i_deg)
    plt.plot([0,0], [-1,1], color='black', linewidth=3)  # mirror
    # incident
    x_in = -np.cos(theta)
    y_in = np.sin(theta)
    plt.plot([x_in,0],[y_in,0], color='red', label='Sinar datang')
    # reflected
    theta_r = theta
    x_r = np.cos(theta_r)
    y_r = np.sin(theta_r)
    plt.plot([0,x_r],[0,y_r], color='green', label='Sinar pantul')
    plt.xlim(-1.2,1.2); plt.ylim(-1.0,1.0)
    plt.axis('off')
    plt.legend(loc='lower center')
    return plt

def generate_simple_report(text):
    """
    Try to generate a PDF report using reportlab if available.
    If not, create a plain text file and return bytes.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        c.setFont("Helvetica", 12)
        y = height - 50
        for line in text.splitlines():
            c.drawString(40, y, line)
            y -= 14
            if y < 50:
                c.showPage()
                y = height - 50
        c.save()
        buffer.seek(0)
        return buffer.read(), "application/pdf", ".pdf"
    except Exception as e:
        # fallback to plain text bytes
        b = text.encode('utf-8')
        return b, "text/plain", ".txt"

def make_download_button(data_bytes, mime, filename, label):
    b64 = base64.b64encode(data_bytes).decode()
    href = f'<a href="data:{mime};base64,{b64}" download="{filename}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Each simulation shows explanation, interactive widgets, visualization, and a "buat laporan" action.
if menu == "1. Cermin Datar":
    st.header("1. Cermin Datar — Pemantulan Satu Sinar")
    theta = st.slider("Sudut datang (°)", 0, 80, 30)
    st.latex(r"\theta_i = \theta_r")
    st.write("Konsep: Pada cermin datar, sudut datang sama dengan sudut pantul terhadap garis normal.")
    fig = draw_mirror_flat(theta)
    st.pyplot(fig)
    report_text = f"Cermin Datar\nTanggal: {datetime.datetime.now()}\nSudut datang: {theta}°\nKesimpulan: Sudut pantul = {theta}°\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_cermin_datar{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "2. Cermin Cekung":
    st.header("2. Cermin Cekung (Konvergen)")
    f = st.slider("Jarak fokus f (cm)", 2.0, 100.0, 10.0)
    do = st.slider("Jarak benda d_o (cm)", 1.0, 300.0, 25.0)
    # thin mirror formula (mirror formula): 1/f = 1/do + 1/di
    try:
        di = 1.0 / (1.0/f - 1.0/do)
    except ZeroDivisionError:
        di = float('inf')
    M = -di / do if di != float('inf') else 0.0
    st.write("Rumus: 1/f = 1/d_o + 1/d_i")
    st.write(f"Bayangan terbentuk pada jarak d_i = {di:.2f} cm (positif: nyata di depan cermin).")
    st.write(f"Perbesaran (M) = {M:.2f}")
    st.write("Keterangan: Jika d_o > f maka bayangan nyata dan terbalik; jika d_o < f maka bayangan maya dan tegak.")

    # simple ray diagram (approximate)
    plt.figure(figsize=(6,3))
    plt.axvline(0, color='black', linewidth=3)
    plt.scatter([-do],[0], color='blue', label='Benda')
    if np.isfinite(di):
        plt.scatter([di],[0], color='orange', label='Bayangan')
    plt.xlim(-max(do,abs(di),f)*1.2, max(do,abs(di),f)*1.2)
    plt.ylim(-1,1)
    plt.legend(); plt.axis('off')
    st.pyplot(plt)

    report_text = f"Cermin Cekung\nTanggal: {datetime.datetime.now()}\nf={f} cm\nd_o={do} cm\nd_i={di}\nM={M}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_cermin_cekung{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "3. Cermin Cembung":
    st.header("3. Cermin Cembung (Divergen)")
    f = st.slider("Jarak fokus f (cm)", 2.0, 100.0, 10.0)
    do = st.slider("Jarak benda d_o (cm)", 1.0, 300.0, 25.0)
    # convex mirror formula: 1/f = 1/do + 1/di  with f negative; here we treat f as positive given by UI but result behind mirror
    f_eff = -abs(f)
    try:
        di = 1.0 / (1.0/f_eff - 1.0/do)
    except ZeroDivisionError:
        di = float('inf')
    st.write("Cermin cembung selalu menghasilkan bayangan maya, lebih kecil, dan tegak.")
    st.write(f"Bayangan maya terbentuk sejauh |d_i| = {abs(di):.2f} cm di belakang cermin.")

    report_text = f"Cermin Cembung\nTanggal: {datetime.datetime.now()}\nf={f} cm (ditafsirkan negatif sebagai cermin cembung)\nd_o={do} cm\nd_i={di}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_cermin_cembung{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "4. Pembiasan Dua Medium (Snellius)":
    st.header("4. Pembiasan Dua Medium — Hukum Snellius")
    n1 = st.slider("Indeks bias medium 1 (n1)", 1.0, 2.5, 1.0)
    n2 = st.slider("Indeks bias medium 2 (n2)", 1.0, 2.5, 1.5)
    theta1 = st.slider("Sudut datang θ1 (°)", 0, 89, 30)
    # compute theta2 using Snell's law with domain check
    arg = n1*np.sin(np.radians(theta1))/n2
    if abs(arg) <= 1.0:
        theta2 = np.degrees(np.arcsin(arg))
        st.write(f"Sudut bias θ2 = {theta2:.2f}°")
    else:
        theta2 = None
        st.warning("Sudut datang lebih besar dari sudut kritis — tidak ada sudut bias (total internal reflection)")
    st.latex(r"n_1 \sin \theta_1 = n_2 \sin \theta_2")
    st.write("Keterangan: Jika n1 > n2 dan sudut datang besar, terjadi Total Internal Reflection (TIR).")

    report_text = f"Pembiasan Dua Medium\nTanggal: {datetime.datetime.now()}\nn1={n1}\nn2={n2}\nθ1={theta1}\nθ2={theta2}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_pembiasan{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "5. Sudut Kritis & TIR":
    st.header("5. Sudut Kritis dan Total Internal Reflection (TIR)")
    n1 = st.slider("Indeks bias medium dalam (n1)", 1.0, 2.5, 1.5)
    n2 = st.slider("Indeks bias medium luar (n2)", 1.0, 2.5, 1.0)
    if n1 > n2:
        theta_c = np.degrees(np.arcsin(n2/n1))
        st.write(f"Sudut kritis θ_c = {theta_c:.2f}°")
        st.write("Jika sudut datang > θ_c maka terjadi TIR (sinar dipantulkan sepenuhnya).")
    else:
        st.warning("n1 <= n2 → tidak terjadi TIR untuk kasus ini.")
    report_text = f"Sudut Kritis & TIR\nTanggal: {datetime.datetime.now()}\nn1={n1}\nn2={n2}\nθ_c={locals().get('theta_c', None)}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_sudut_kritis{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "6. Prisma Segitiga (Deviasi)":
    st.header("6. Prisma Segitiga — Sudut Deviasi")
    A = st.slider("Sudut puncak prisma A (°)", 10, 80, 60)
    n = st.slider("Indeks bias prisma n", 1.0, 2.0, 1.5)
    i = st.slider("Sudut datang i (°)", 0, 80, 40)
    # approximate using small-angle relations and Snell's law twice
    try:
        r1 = np.degrees(np.arcsin(np.sin(np.radians(i))/n))
        r2 = A - r1
        e = np.degrees(np.arcsin(n*np.sin(np.radians(r2))))
        D = i + e - A
    except Exception:
        D = float('nan')
    st.write(f"Sudut deviasi D ≈ {D:.2f}°")
    st.latex(r"D = i + e - A")
    st.write("Prisma menyebabkan deviasi dan, untuk cahaya putih, dispersi spektrum.")
    report_text = f"Prisma\nTanggal: {datetime.datetime.now()}\nA={A}\nn={n}\ni={i}\nD={D}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_prisma{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "7. Lensa Cekung":
    st.header("7. Lensa Cekung (Divergen)")
    f = -abs(st.slider("Jarak fokus f (cm, tanda negatif)", 2.0, 100.0, 10.0))
    do = st.slider("Jarak benda d_o (cm)", 1.0, 300.0, 25.0)
    try:
        di = 1.0 / (1.0/f - 1.0/do)
    except ZeroDivisionError:
        di = float('inf')
    st.write("Lensa cekung menghasilkan bayangan maya di sisi benda (di negatif secara tanda).")
    st.write(f"Perhitungan d_i (tanda): {di:.2f} cm")
    report_text = f"Lensa Cekung\nTanggal: {datetime.datetime.now()}\nf={f}\nd_o={do}\nd_i={di}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_lensa_cekung{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "8. Lensa Cembung":
    st.header("8. Lensa Cembung (Konvergen)")
    f = st.slider("Jarak fokus f (cm)", 2.0, 100.0, 10.0)
    do = st.slider("Jarak benda d_o (cm)", 1.0, 300.0, 25.0)
    try:
        di = 1.0 / (1.0/f - 1.0/do)
    except ZeroDivisionError:
        di = float('inf')
    M = -di/do if di != float('inf') else 0.0
    st.write(f"Bayangan terbentuk pada d_i = {di:.2f} cm. Perbesaran M = {M:.2f}")
    report_text = f"Lensa Cembung\nTanggal: {datetime.datetime.now()}\nf={f}\nd_o={do}\nd_i={di}\nM={M}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_lensa_cembung{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "9. Sistem Lensa + Cermin":
    st.header("9. Sistem Lensa + Cermin (Karakter sederhana)")
    f_l = st.slider("Fokus lensa f_l (cm)", 5.0, 200.0, 50.0)
    f_c = st.slider("Fokus cermin f_c (cm)", 5.0, 200.0, 75.0)
    do = st.slider("Jarak benda awal (cm)", 10.0, 400.0, 100.0)
    try:
        di1 = 1.0 / (1.0/f_l - 1.0/do)
        di2 = 1.0 / (1.0/f_c - 1.0/di1)
    except Exception:
        di1 = di2 = float('nan')
    st.write(f"Bayangan sementara d_i1 = {di1:.2f} cm → Bayangan akhir d_i2 = {di2:.2f} cm")
    report_text = f"Sistem Lensa+Cermin\nTanggal: {datetime.datetime.now()}\nf_l={f_l}\nf_c={f_c}\nd_o={do}\ndi1={di1}\ndi2={di2}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_sistem{ext}", "⬇️ Download Laporan Hasil Simulasi")

elif menu == "10. Dispersi Cahaya Putih":
    st.header("10. Dispersi Cahaya Putih oleh Prisma (Spektrum sederhana)")
    angle = st.slider("Sudut prisma (°)", 10, 80, 60)
    colors = ['violet','indigo','blue','green','yellow','orange','red']
    plt.figure(figsize=(7,2))
    for i,c in enumerate(colors):
        plt.plot([0, np.cos(np.radians(angle))],[i, i+np.sin(np.radians(angle))], linewidth=6)
    plt.axis('off'); plt.title("Spektrum warna (ilustratif)")
    st.pyplot(plt)
    report_text = f"Dispersi Prisma\nTanggal: {datetime.datetime.now()}\nSudut prisma={angle}\n"
    data, mime, ext = generate_simple_report(report_text)
    make_download_button(data, mime, f"laporan_dispersiprism{ext}", "⬇️ Download Laporan Hasil Simulasi")

st.markdown('---')
st.caption("Panduan singkat: gunakan slider untuk mengubah parameter. Tekan tombol download untuk menyimpan hasil observasi.")
