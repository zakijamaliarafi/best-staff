import streamlit as st
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)
pd.set_option('mode.chained_assignment', None)
import matplotlib.pyplot as plt
import base64
import requests


kriteria = pd.DataFrame({'Kriteria': ['C1', 'C2', 'C3', 'C4', 'C5'],
                         'Keterangan': ['Kehadiran Dalam Setiap Kegiatan', 'Keberhasilan Pelaksanaan Proker', 'Keaktifan Staff', 'Kedisiplinan Staff', 'Ketertiban Pelaksanaan Piket'],
                         'Kategori': ['Benefit', 'Cost', 'Benefit', 'Benefit', 'Benefit'],
                         'Bobot Kriteria': [5, 5, 4, 4, 3]}).set_index('Kriteria')

bobot = pd.DataFrame([{'Kriteria': 'Normalisasi Bobot', 'C1': 0.238095238, 'C2': 0.238095238, 'C3': 0.19047619, 'C4': 0.19047619, 'C5': 0.142857143}]).set_index('Kriteria')

sc_kehadiran = pd.DataFrame({'Kualifikasi': ['Selalu hadir tanpa absen', 'Hadir 90-99% dari seluruh kegiatan', 'Hadir 80-89% dari seluruh kegiatan', 'Hadir 70-79% dari seluruh kegiatan', 'Hadir kurang dari 70% dari seluruh kegiatan'],
                          'Skala': [5, 4, 3, 2, 1]}).set_index('Kualifikasi')

sc_keberhasilan = pd.DataFrame({'Kualifikasi': ['Proker tidak terlaksana atau gagal total', 'Proker terlaksana tetapi tidak sesuai target', 'Proker terlaksana dengan hasil yang kurang memuaskan', 'Proker terlaksana dengan hasil cukup baik', 'Proker terlaksana dengan sangat sukses'],
                          'Skala': [5, 4, 3, 2, 1]}).set_index('Kualifikasi')

sc_keaktifan = pd.DataFrame({'Kualifikasi': ['Sangat aktif, selalu berinisiatif dan inovatif', 'Aktif, sering berinisiatif dan inovatif', 'Cukup aktif, kadang-kadang berinisiatif', 'Kurang aktif, jarang berinisiatif', 'Tidak aktif, tidak pernah berinisiatif'],
                          'Skala': [5, 4, 3, 2, 1]}).set_index('Kualifikasi')

sc_kedisiplinan = pd.DataFrame({'Kualifikasi': ['Sangat disiplin, tidak pernah terlambat atau melanggar aturan', 'Disiplin, jarang terlambat atau melanggar aturan', 'Cukup disiplin, kadang-kadang terlambat', 'Kurang disiplin, sering terlambat', 'Tidak disiplin, selalu terlambat atau melanggar aturan'],
                          'Skala': [5, 4, 3, 2, 1]}).set_index('Kualifikasi')

sc_ketertiban = pd.DataFrame({'Kualifikasi': ['Sangat tertib, selalu mengikuti jadwal piket', 'Tertib, jarang absen dari jadwal piket', 'Cukup tertib, kadang-kadang absen dari jadwal piket', 'Kurang tertib, sering absen dari jadwal piket', 'Tidak tertib, selalu absen dari jadwal piket'],
                          'Skala': [5, 4, 3, 2, 1]}).set_index('Kualifikasi')

alternatif = pd.DataFrame({'Alternatif' : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                           'Kehadiran' : ['Selalu hadir tanpa absen', 'Hadir 90-99% dari seluruh kegiatan', 'Hadir 80-89% dari seluruh kegiatan', 'Hadir 70-79% dari seluruh kegiatan', 'Hadir kurang dari 70% dari seluruh kegiatan', 'Selalu hadir tanpa absen', 'Hadir 90-99% dari seluruh kegiatan', 'Hadir 80-89% dari seluruh kegiatan', 'Hadir 70-79% dari seluruh kegiatan', 'Hadir kurang dari 70% dari seluruh kegiatan'],
                           'Keberhasilan Proker' : ['Proker terlaksana dengan hasil cukup baik', 'Proker terlaksana dengan hasil yang kurang memuaskan', 'Proker terlaksana dengan sangat sukses', 'Proker tidak terlaksana atau gagal total', 'Proker terlaksana tetapi tidak sesuai target', 'Proker terlaksana dengan hasil yang kurang memuaskan', 'Proker terlaksana dengan hasil cukup baik', 'Proker terlaksana tetapi tidak sesuai target', 'Proker terlaksana dengan hasil yang kurang memuaskan', 'Proker terlaksana dengan sangat sukses'],
                           'Keaktifan' : ['Aktif, sering berinisiatif dan inovatif', 'Sangat aktif, selalu berinisiatif dan inovatif', 'Cukup aktif, kadang-kadang berinisiatif', 'Kurang aktif, jarang berinisiatif', 'Tidak aktif, tidak pernah berinisiatif', 'Aktif, sering berinisiatif dan inovatif', 'Sangat aktif, selalu berinisiatif dan inovatif', 'Cukup aktif, kadang-kadang berinisiatif', 'Kurang aktif, jarang berinisiatif', 'Tidak aktif, tidak pernah berinisiatif'],
                           'Kedisiplinan' : ['Cukup disiplin, kadang-kadang terlambat', 'Disiplin, jarang terlambat atau melanggar aturan', 'Sangat disiplin, tidak pernah terlambat atau melanggar aturan', 'Kurang disiplin, sering terlambat', 'Tidak disiplin, selalu terlambat atau melanggar aturan', 'Cukup disiplin, kadang-kadang terlambat', 'Sangat disiplin, tidak pernah terlambat atau melanggar aturan', 'Cukup disiplin, kadang-kadang terlambat', 'Kurang disiplin, sering terlambat', 'Tidak disiplin, selalu terlambat atau melanggar aturan'],
                           'Ketertiban Piket' : ['Sangat tertib, selalu mengikuti jadwal piket', 'Tertib, jarang absen dari jadwal piket', 'Cukup tertib, kadang-kadang absen dari jadwal piket', 'Kurang tertib, sering absen dari jadwal piket', 'Tidak tertib, selalu absen dari jadwal piket', 'Tertib, jarang absen dari jadwal piket', 'Sangat tertib, selalu mengikuti jadwal piket', 'Tertib, jarang absen dari jadwal piket', 'Kurang tertib, sering absen dari jadwal piket', 'Tidak tertib, selalu absen dari jadwal piket']}).set_index('Alternatif')

nilai_sk = pd.DataFrame({'Alternatif' : ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                         'C1' : [5, 4, 3, 2, 1, 5, 4, 3, 2, 1],
                         'C2' : [2, 3, 1, 5, 4, 3, 2, 4, 3, 1],
                         'C3' : [4, 5, 3, 2, 1, 4, 5, 3, 2, 1],
                         'C4' : [3, 4, 5, 2, 1, 3, 5, 3, 2, 1],
                         'C5' : [5, 4, 3, 2, 1, 4, 5, 4, 2, 1]}).set_index('Alternatif')

vektor_s = pd.DataFrame({'Alternatif': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                        'Vektor S': [2.512805136, 2.309782705, 2.545527892, 1.155938576, 0.7188733488, 2.209978421, 2.740317934, 1.729902911, 1.305436911, 1]}).set_index('Alternatif')

chart_vektor_s = pd.DataFrame({'Alternatif': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                        'Vektor S': [2.512805136, 2.309782705, 2.545527892, 1.155938576, 0.7188733488, 2.209978421, 2.740317934, 1.729902911, 1.305436911, 1]})


vektor_v = pd.DataFrame({'Alternatif': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                        'Vektor V': [0.1378498689, 0.1267122701, 0.1396450052, 0.06341358467, 0.03943664214, 0.1212371112, 0.1503309838, 0.09490066946, 0.0716149074, 0.05485895702]}).set_index('Alternatif')

chart_vektor_v = pd.DataFrame({'Alternatif': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                        'Vektor V': [0.1378498689, 0.1267122701, 0.1396450052, 0.06341358467, 0.03943664214, 0.1212371112, 0.1503309838, 0.09490066946, 0.0716149074, 0.05485895702]})

rank = pd.DataFrame({'Alternatif': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
                        'Hasil': [0.1378498689, 0.1267122701, 0.1396450052, 0.06341358467, 0.03943664214, 0.1212371112, 0.1503309838, 0.09490066946, 0.0716149074, 0.05485895702],
                        'Ranking': [3, 4, 2, 8, 10, 5, 1, 6, 7, 9]}).set_index('Alternatif')


def table_of_contents():
    st.sidebar.title('Daftar Isi')
    st.sidebar.markdown('''
        1. [Menentukan Kriteria dan Bobot](#menentukan-kriteria-dan-bobot)  
        2. [Menghitung Normalisasi Bobot](#menghitung-normalisasi-bobot)
        3. [Menentukan Skala Penilaian dan Kualifikasi](#menentukan-skala-penilaian-dan-kualifikasi)
        4. [Data Alternatif](#data-alternatif)
        5. [Perubahan Nilai Skala Kriteria Alternatif](#perubahan-nilai-skala-kriteria-alternatif)
        6. [Menghitung Vektor S](#menghitung-vektor-s)
        7. [Menghitung Vektor V](#menghitung-vektor-v)
        8. [Hasil Perangkingan](#hasil-perangkingan)
    ''', unsafe_allow_html=True)

table_of_contents()

response = requests.get("https://sf16-va.tiktokcdn.com/obj/eden-va2/nb-shivsn-ryhs/ljhwZthlaukjlkulzlp/lark-topics/ai-glossary/decision-support-system-dss.webp")
image_data = base64.b64encode(response.content).decode('utf-8')

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{image_data}" style="height: 200px;width: 100%;object-fit: cover;">
    </div>
    """,
    unsafe_allow_html=True
)

st.title('Sistem Pendukung Keputusan - Metode Weighted Product')
st.write('Perhitungan Pendukung Keputusan dengan Metode WP untuk Pemilihan Staff Terbaik dalam Organisasi Dewan Legislatif Mahasiswa.')
st.divider()

st.subheader('Menentukan Kriteria dan Bobot')
st.write('Tabel Kriteria dan Bobot Kriteria :')
st.write(kriteria)
st.divider()

st.subheader('Menghitung Normalisasi Bobot')
st.write('Rumus Normalisasi Bobot :')
st.latex(r'W_{j} = \frac{W_{j}}{\sum{W_{j}}}')
st.write('Contoh Hitung Normalisasi Bobot :')
st.latex(r'W_{1} = \frac{5}{5+5+4+4+3} = 0.238095238')
st.write('Hasil Normalisasi Bobot :')
st.write(bobot)
st.divider()

st.subheader('Menentukan Skala Penilaian dan Kualifikasi')
st.write('Tabel Skala Kriteria Kehadiran Dalam Setiap Kegiatan :')
st.write(sc_kehadiran)
st.write('Tabel Skala Kriteria Keberhasilan Pelaksanaan Proker :')
st.write(sc_keberhasilan)
st.write('Tabel Skala Kriteria Keaktifan Staff :')
st.write(sc_keaktifan)
st.write('Tabel Skala Kriteria Kedisiplinan Staff :')
st.write(sc_kedisiplinan)
st.write('Tabel Skala Kriteria Ketertiban Pelaksanaan Piket :')
st.write(sc_ketertiban)
st.divider()

st.subheader('Data Alternatif')
st.write('Data Alternatif Staff DLM :')
st.write(alternatif)
st.divider()

st.subheader('Perubahan Nilai Skala Kriteria Alternatif')
st.write('Tabel Nilai Skala Kriteria Alternatif :')
st.write(nilai_sk)
st.divider()

st.subheader('Menghitung Vektor S')
st.write('Rumus Vektor S :')
st.latex(r'S_{i} = \prod_{j=1}^{n} (x_{ij})^{w_{j}}')
st.write('Contoh Hitung Vektor S dengan A :')
st.latex(r'S_{A} = (5)^{0.238095238} \times (2)^{-0.238095238} \times (4)^{0.19047619} \times (3)^{0.19047619} \times (5)^{0.142857143} = 2.512805136')
st.write('Tabel Hasil Perhitungan Vektor S :')
st.write(vektor_s)
chart_vektor_s = chart_vektor_s.set_index('Alternatif')
fig_s, ax_s = plt.subplots(figsize=(10, 6))
chart_vektor_s.plot(kind='bar', ax=ax_s, color='skyblue')
ax_s.set_title('Vektor S')
ax_s.set_ylabel('Nilai Vektor S')
ax_s.set_xlabel('Alternatif')
plt.tight_layout()
st.pyplot(fig_s)
st.divider()

st.subheader('Menghitung Vektor V')
st.write('Rumus Vektor V :')
st.latex(r'V_{i} = \frac{S_{i}}{\prod_{j=1}^{n} (x_{ij})^{w_{j}}}')
st.write('Contoh Hitung Vektor V dengan A :')
st.latex(r'V_{A} = \frac{2.512805136}{18.22856384} = 0.1378498689')
st.write('Tabel Hasil Perhitungan Vektor V :')
st.write(vektor_v)
chart_vektor_v = chart_vektor_v.set_index('Alternatif')
fig_v, ax_v = plt.subplots(figsize=(10, 6))
chart_vektor_v.plot(kind='bar', ax=ax_v, color='lightgreen')
ax_v.set_title('Vektor V')
ax_v.set_ylabel('Nilai Vektor V')
ax_v.set_xlabel('Alternatif')
plt.tight_layout()
st.pyplot(fig_v)
st.divider()

st.subheader('Hasil Perangkingan')
st.write('Tabel Ranking Alternatif :')
st.write(rank)