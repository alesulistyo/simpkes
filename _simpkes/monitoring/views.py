import csv
import sys
from subprocess import run

import pandas as pd
from django.db import connection
from django.shortcuts import render


def dictfetchall(cursor):
  "Return all rows from a cursor as a dict"
  columns = [col[0] for col in cursor.description]
  return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):

  cursor = connection.cursor()
  cursor.execute("SELECT * FROM data_sensor ORDER BY id DESC LIMIT 1")
  datasensor = dictfetchall(cursor)
  cursor.close()

  id = datasensor[0].get('id')
  spo2 = datasensor[0].get('spo2')
  bpm = datasensor[0].get('bpm')
  temp = datasensor[0].get('temp')

  context = {
      'id': id,
      'spo2': spo2,
      'bpm': bpm,
      'temp': temp,
      'title': 'Sistem Pemantauan Kesehatan | Tugas Akhir',
      'heading': 'Sistem Pemantauan Kesehatan',
      'subheading': 'Alessandro Sulistyo',
      'foot': 'Alessandro Sulistyo',
  }
  return render(request, 'monitoring.html', context)


def fuzzy(request):

  cursor = connection.cursor()
  cursor.execute("SELECT * FROM data_sensor ORDER BY id DESC LIMIT 1")
  datasensor = dictfetchall(cursor)
  cursor.close()

  id_new = datasensor[0].get('id')
  spo2_new = datasensor[0].get('spo2')
  bpm_new = datasensor[0].get('bpm')
  temp_new = datasensor[0].get('temp')

  if request.method == 'POST':
    id = request.POST.get('id')
    spo2 = request.POST.get('spo2')
    bpm = request.POST.get('bpm')
    temp = request.POST.get('temp')

    run([sys.executable, 'monitoring\\mamdani_fuzzy_plot.py', id, spo2, bpm, temp], shell=False)

  cursor = connection.cursor()
  cursor.execute("SELECT * FROM riwayat ORDER BY id DESC LIMIT 1")
  result = dictfetchall(cursor)
  cursor.close()

  with open('out_fuzz_spo2.csv') as f:
    r = csv.reader(f)
    mu_spo2 = []
    for line in r:
      mu_spo2.append(line)

  with open('out_fuzz_bpm.csv') as f:
    r = csv.reader(f)
    mu_bpm = []
    for line in r:
      mu_bpm.append(line)

  with open('out_fuzz_temp.csv') as f:
    r = csv.reader(f)
    mu_temp = []
    for line in r:
      mu_temp.append(line)

  with open('out_inferensi.csv') as f:
    r = csv.reader(f)
    inferensi = []
    for line in r:
      inferensi.append(line)

  with open('max.csv') as f:
    r = csv.reader(f)
    max = []
    for line in r:
      max.append(line)

  defuzz = pd.read_csv('out_defuzz.csv', names=['defuzz'])
  defuzz_val = defuzz.iloc[0]['defuzz']

  stat = pd.read_csv('out_hasil.csv', names=['stat'])
  stat_val = stat.iloc[0]['stat']

  context = {
      'id': id_new,
      'spo2': spo2_new,
      'bpm': bpm_new,
      'temp': temp_new,
      'hasil_spo2': result[0].get('spo2'),
      'hasil_bpm': result[0].get('bpm'),
      'hasil_temp': result[0].get('temp'),
      'hasil_waktu': result[0].get('waktu'),
      'hasil_status': result[0].get('status'),
      'mu_spo2': mu_spo2,
      'mu_bpm': mu_bpm,
      'mu_temp': mu_temp,
      'inferensi': inferensi,
      'max': max,
      'deff': defuzz_val,
      'stat': stat_val,
      'title': 'Sistem Pemantauan Kesehatan | Tugas Akhir',
      'heading': 'Sistem Pemantauan Kesehatan',
      'subheading': 'Alessandro Sulistyo',
      'foot': 'Alessandro Sulistyo',
  }
  return render(request, 'fuzzy.html', context)
