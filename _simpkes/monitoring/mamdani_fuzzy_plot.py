import shutil
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql
from PIL import Image

# Fungsi Keanggotaan
spo2_mf = {"start": 85, "end": 100, "Rendah": [85, 90, 92.5], "Kurang": [90, 92.5, 95], "Normal": [92.5, 95, 100]}
bpm_mf = {"start": 50, "end": 110, "Rendah": [50, 60, 80], "Normal": [60, 80, 100], "Tinggi": [80, 100, 110]}
temp_mf = {"start": 35, "end": 38, "Rendah": [35, 35.5, 36.5], "Normal": [35.5, 36.5, 37.5], "Tinggi": [36.5, 37.5, 38]}
hipoksemia_mf = {
    "start": 0,
    "end": 100,
    "Hipoksemia Berat": [0, 20, 40],
    "Hipoksemia Sedang": [20, 40, 60],
    "Hipoksemia Ringan": [40, 60, 80],
    "Sehat": [60, 80, 100]
}


# Trapesium Kiri
def trapmfL(pos, x0, x1):
  if pos >= x1:
    nilai = 0.0
  elif pos <= x0:
    nilai = 1.0
  elif x0 <= pos <= x1:
    nilai = (x1 - pos) / (x1 - x0)

  if nilai > 1:
    nilai = 1.0

  return nilai


# Segitiga
def trimf(pos, x0, x1, x2):
  if pos <= x0 or pos >= x2:
    nilai = 0.0
  elif x0 <= pos <= x1:
    nilai = (pos - x0) / (x1 - x0)
  elif x1 <= pos <= x2:
    nilai = (x2 - pos) / (x2 - x1)

  if nilai > 1:
    nilai = 1.0

  return nilai


# Trapesium Kanan
def trapmfR(pos, x0, x1):
  if pos <= x0:
    nilai = 0.0
  elif pos >= x1:
    nilai = 1.0
  elif x0 <= pos <= x1:
    nilai = (pos - x0) / (x1 - x0)

  if nilai > 1:
    nilai = 1.0

  return nilai


def fuzzifikasi(mf, pos):

  derajat_fuzzy = []
  for nama, nilai in mf.items():
    if nama != 'start' and nama != 'end':
      if nilai[0] == mf["start"]:
        y = trapmfL(pos, x0=nilai[1], x1=nilai[2])
        derajat_fuzzy.append([nama, round(y, 1)])
      elif nilai[2] == mf["end"]:
        y = trapmfR(pos, x0=nilai[0], x1=nilai[1])
        derajat_fuzzy.append([nama, round(y, 1)])
      else:
        y = trimf(pos, x0=nilai[0], x1=nilai[1], x2=nilai[2])
        derajat_fuzzy.append([nama, round(y, 1)])

  return derajat_fuzzy


def inferensi(input1, input2, input3):

  output = []
  for spo2 in input1:
    for bpm in input2:
      for temp in input3:

        # R1-R9
        if spo2[0] == "Rendah" and bpm[0] == "Rendah" and temp[0] == "Rendah":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Rendah" and bpm[0] == "Rendah" and temp[0] == "Normal":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Rendah" and bpm[0] == "Rendah" and temp[0] == "Tinggi":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])

        elif spo2[0] == "Rendah" and bpm[0] == "Normal" and temp[0] == "Rendah":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Rendah" and bpm[0] == "Normal" and temp[0] == "Normal":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Rendah" and bpm[0] == "Normal" and temp[0] == "Tinggi":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])

        elif spo2[0] == "Rendah" and bpm[0] == "Tinggi" and temp[0] == "Rendah":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Rendah" and bpm[0] == "Tinggi" and temp[0] == "Normal":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Rendah" and bpm[0] == "Tinggi" and temp[0] == "Tinggi":
          output.append(["Hipoksemia Berat", min(spo2[1], bpm[1], temp[1])])

        # R10-R18
        elif spo2[0] == "Kurang" and bpm[0] == "Rendah" and temp[0] == "Rendah":
          output.append(["Hipoksemia Sedang", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Kurang" and bpm[0] == "Rendah" and temp[0] == "Normal":
          output.append(["Hipoksemia Ringan", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Kurang" and bpm[0] == "Rendah" and temp[0] == "Tinggi":
          output.append(["Hipoksemia Sedang", min(spo2[1], bpm[1], temp[1])])

        elif spo2[0] == "Kurang" and bpm[0] == "Normal" and temp[0] == "Rendah":
          output.append(["Hipoksemia Sedang", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Kurang" and bpm[0] == "Normal" and temp[0] == "Normal":
          output.append(["Hipoksemia Ringan", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Kurang" and bpm[0] == "Normal" and temp[0] == "Tinggi":
          output.append(["Hipoksemia Sedang", min(spo2[1], bpm[1], temp[1])])

        elif spo2[0] == "Kurang" and bpm[0] == "Tinggi" and temp[0] == "Rendah":
          output.append(["Hipoksemia Sedang", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Kurang" and bpm[0] == "Tinggi" and temp[0] == "Normal":
          output.append(["Hipoksemia Ringan", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Kurang" and bpm[0] == "Tinggi" and temp[0] == "Tinggi":
          output.append(["Hipoksemia Sedang", min(spo2[1], bpm[1], temp[1])])

        # R19-R27
        elif spo2[0] == "Normal" and bpm[0] == "Rendah" and temp[0] == "Rendah":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Normal" and bpm[0] == "Rendah" and temp[0] == "Normal":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Normal" and bpm[0] == "Rendah" and temp[0] == "Tinggi":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])

        elif spo2[0] == "Normal" and bpm[0] == "Normal" and temp[0] == "Rendah":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Normal" and bpm[0] == "Normal" and temp[0] == "Normal":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Normal" and bpm[0] == "Normal" and temp[0] == "Tinggi":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])

        elif spo2[0] == "Normal" and bpm[0] == "Tinggi" and temp[0] == "Rendah":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Normal" and bpm[0] == "Tinggi" and temp[0] == "Normal":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])
        elif spo2[0] == "Normal" and bpm[0] == "Tinggi" and temp[0] == "Tinggi":
          output.append(["Sehat", min(spo2[1], bpm[1], temp[1])])

  return output


def agregasi(perpotongan):

  x_start = hipoksemia_mf["start"]
  max_curname = perpotongan[0][0]

  for x in range(hipoksemia_mf["start"], hipoksemia_mf["end"] + 1):
    x_max = max(fuzzifikasi(hipoksemia_mf, x), key=lambda m: m[1])
    curname = x_max[0]

    if max_curname != curname:
      for i in perpotongan:
        if i[0] == max_curname:
          i.append(x_start)
          i.append(x - 1)

      max_curname = curname
      x_start = x

    elif x == hipoksemia_mf["end"]:
      for i in perpotongan:
        if i[0] == max_curname:
          i.append(x_start)
          i.append(x)

  return perpotongan


def defuzzifikasi(hasil_agregasi):
  pembilang = 0.0
  penyebut = 0.0

  for i in hasil_agregasi:
    nilai = i[1]
    start = i[2]
    end = i[3]

    total_item = 0.0

    for x in range(start, end + 1):
      total_item += x
      penyebut += nilai

    pembilang += total_item * nilai

  return pembilang / penyebut


id = int(sys.argv[1])
spo2_input = float(sys.argv[2])
bpm_input = float(sys.argv[3])
temp_input = float(sys.argv[4])

# Step 1 - Fuzzifikasi
spo2_nilai = fuzzifikasi(spo2_mf, spo2_input)
bpm_nilai = fuzzifikasi(bpm_mf, bpm_input)
temp_nilai = fuzzifikasi(temp_mf, temp_input)
df_spo2 = pd.DataFrame(np.asarray(spo2_nilai))
df_spo2.to_csv('out_fuzz_spo2.csv', header=False, index=False)
df_bpm = pd.DataFrame(np.asarray(bpm_nilai))
df_bpm.to_csv('out_fuzz_bpm.csv', header=False, index=False)
df_temp = pd.DataFrame(np.asarray(temp_nilai))
df_temp.to_csv('out_fuzz_temp.csv', header=False, index=False)

# Step 2 - Inferensi
inferensi_output = inferensi(spo2_nilai, bpm_nilai, temp_nilai)
df_inferensi = pd.DataFrame(np.asarray(inferensi_output))
df_inferensi.to_csv('out_inferensi.csv', header=False, index=False)

# Step 3 - Agregasi
agregasi_output = agregasi(inferensi_output)
df_agregasi = pd.DataFrame(np.asarray(agregasi_output))
df_agregasi.to_csv('out_agregasi.csv', header=False, index=False)

HB = []
HB_val = []

HS = []
HS_val = []

HR = []
HR_val = []

S = []
S_val = []

for i in range(len(agregasi_output)):
  if agregasi_output[i][0] == 'Hipoksemia Berat':
    HB.append([agregasi_output[i][0], agregasi_output[i][1]])
    HB_val.append(agregasi_output[i][1])
  elif agregasi_output[i][0] == 'Hipoksemia Sedang':
    HS.append([agregasi_output[i][0], agregasi_output[i][1]])
    HS_val.append(agregasi_output[i][1])
  elif agregasi_output[i][0] == 'Hipoksemia Ringan':
    HR.append([agregasi_output[i][0], agregasi_output[i][1]])
    HR_val.append(agregasi_output[i][1])
  elif agregasi_output[i][0] == 'Sehat':
    S.append([agregasi_output[i][0], agregasi_output[i][1]])
    S_val.append(agregasi_output[i][1])

maxArr = [max(HB), max(HS), max(HR), max(S)]
np.savetxt('max.csv', maxArr, fmt='%s', delimiter=',')

# Step 4 - Defuzzifikasi
deffuzifikasi_output = defuzzifikasi(agregasi_output)
df_spo2 = pd.DataFrame(np.asarray(['{0:.3f}'.format(deffuzifikasi_output / 100)]))
df_spo2.to_csv('out_defuzz.csv', header=False, index=False)

fuzzifikasi_output = fuzzifikasi(hipoksemia_mf, deffuzifikasi_output)
hasil = [maxArr[0][0], maxArr[0][1]]
for item in maxArr:
  if item[1] > hasil[1]:
    hasil = [item[0], item[1]]

df_hasil = pd.DataFrame(np.asarray(hasil))
df_hasil.to_csv('out_hasil.csv', header=False, index=False)

# To DB
db = pymysql.connect(host='localhost', user='root', password='', database='tugasakhir')
cursor = db.cursor()
cursor.execute('INSERT INTO riwayat(id_data_sensor, spo2, bpm, temp, status) VALUES (%s, %s, %s, %s, %s)', (id, spo2_input, bpm_input, temp_input, hasil[0]))
db.commit()
cursor.close()

spo2_rendah = [1, 1, 0, 0, 0]
spo2_kurang = [0, 0, 1, 0, 0]
spo2_normal = [0, 0, 0, 1, 1]
spo2_x = [85, 90, 92.5, 95, 100]

bpm_rendah = [1, 1, 0, 0, 0]
bpm_kurang = [0, 0, 1, 0, 0]
bpm_normal = [0, 0, 0, 1, 1]
bpm_x = [50, 60, 80, 100, 110]

temp_rendah = [1, 1, 0, 0, 0]
temp_kurang = [0, 0, 1, 0, 0]
temp_normal = [0, 0, 0, 1, 1]
temp_x = [35, 35.5, 36.5, 37.5, 38]

# PLOT
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(10, 10))

ax0.plot(spo2_x, spo2_rendah, label="SpO2 Rendah")
ax0.plot(spo2_x, spo2_kurang, label="SpO2 Kurang")
ax0.plot(spo2_x, spo2_normal, label="SpO2 Normal")
ax0.set_title("Fungsi Keanggotaan SpO2")
ax0.legend(loc='center right')

ax1.plot(bpm_x, bpm_rendah, label="BPM Rendah")
ax1.plot(bpm_x, bpm_kurang, label="BPM Kurang")
ax1.plot(bpm_x, bpm_normal, label="BPM Normal")
ax1.set_title("Fungsi Keanggotaan BPM")
ax1.legend(loc='center right')

ax2.plot(temp_x, temp_rendah, label="Suhu Rendah")
ax2.plot(temp_x, temp_kurang, label="Suhu Kurang")
ax2.plot(temp_x, temp_normal, label="Suhu Normal")
ax2.set_title("Fungsi Keanggotaan Suhu")
ax2.legend(loc='center right')

plt.tight_layout()
plt.savefig("plot_MF.jpg")

berat = [1, 1, 0, 0, 0, 0]
sedang = [0, 0, 1, 0, 0, 0]
ringan = [0, 0, 0, 1, 0, 0]
sehat = [0, 0, 0, 0, 1, 1]
X = [0, 20, 40, 60, 80, 100]

# PLOT
fig, (ax0) = plt.subplots(figsize=(10, 5))

plt.xlim(0, 100)
plt.ylim(0, 1)

ax0.patch.set_facecolor('b')
ax0.fill_between(X, max(HB_val), berat, color='w')
ax0.fill_between(X, 1, berat, color='w')
ax0.plot(X, berat, label="Berat")
ax0.plot(X, sedang, label="Sedang")
ax0.plot(X, ringan, label="Ringan")
ax0.plot(X, sehat, label="Sehat")
ax0.legend(loc='center right')

plt.savefig("plot_berat.png")

fig, (ax0) = plt.subplots(figsize=(10, 5))

plt.xlim(0, 100)
plt.ylim(0, 1)

ax0.patch.set_facecolor('y')
ax0.fill_between(X, max(HS_val), sedang, color='w')
ax0.fill_between(X, 1, sedang, color='w')
ax0.plot(X, berat, label="Berat")
ax0.plot(X, sedang, label="Sedang")
ax0.plot(X, ringan, label="Ringan")
ax0.plot(X, sehat, label="Sehat")
ax0.legend(loc='center right')

plt.savefig("plot_sedang.png")

fig, (ax0) = plt.subplots(figsize=(10, 5))

plt.xlim(0, 100)
plt.ylim(0, 1)

ax0.patch.set_facecolor('g')
ax0.fill_between(X, max(HR_val), ringan, color='w')
ax0.fill_between(X, 1, ringan, color='w')
ax0.plot(X, berat, label="Berat")
ax0.plot(X, sedang, label="Sedang")
ax0.plot(X, ringan, label="Ringan")
ax0.plot(X, sehat, label="Sehat")
ax0.legend(loc='center right')

plt.savefig("plot_ringan.png")

fig, (ax0) = plt.subplots(figsize=(10, 5))

plt.xlim(0, 100)
plt.ylim(0, 1)

ax0.patch.set_facecolor('r')
ax0.fill_between(X, max(S_val), sehat, color='w')
ax0.fill_between(X, 1, sehat, color='w')
ax0.plot(X, berat, label="Berat")
ax0.plot(X, sedang, label="Sedang")
ax0.plot(X, ringan, label="Ringan")
ax0.plot(X, sehat, label="Sehat")
ax0.legend(loc='center right')

plt.savefig("plot_sehat.png")

img1 = Image.open("plot_berat.png").convert("RGBA")
img2 = Image.open("plot_sedang.png").convert("RGBA")
img3 = Image.open("plot_ringan.png").convert("RGBA")
img4 = Image.open("plot_sehat.png").convert("RGBA")

blend1 = Image.blend(img1, img2, 0.5).save("blend1.png")
blend2 = Image.blend(img3, img4, 0.5).save("blend2.png")

blend1 = Image.open("blend1.png").convert("RGBA")
blend2 = Image.open("blend2.png").convert("RGBA")
blend = Image.blend(blend1, blend2, 0.5).save("blend.png")

fig, (ax0) = plt.subplots(figsize=(10, 5))

plt.xlim(0, 100)
plt.ylim(0, 1)

cog = '{0:.3f}'.format(deffuzifikasi_output)
xFill = np.full(6, float(cog))

ax0.plot(X, berat, label="Berat")
ax0.plot(X, sedang, label="Sedang")
ax0.plot(X, ringan, label="Ringan")
ax0.plot(X, sehat, label="Sehat")
ax0.plot(xFill, X, label="COG = " + str(cog), color='k')
ax0.legend(loc='center right')

plt.savefig("plot_cog.png", transparent=True)

blend = Image.open("blend.png")
cog = Image.open("plot_cog.png")
Image.alpha_composite(blend, cog).save("cog.png")

src_path = r"blend.png"
dst_path = r"static\img\blend.png"
shutil.move(src_path, dst_path)

src_path = r"cog.png"
dst_path = r"static\img\cog.png"
shutil.move(src_path, dst_path)
