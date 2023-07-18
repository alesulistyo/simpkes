from django.db import connection
from django.shortcuts import render


def dictfetchall(cursor):
  "Return all rows from a cursor as a dict"
  columns = [col[0] for col in cursor.description]
  return [dict(zip(columns, row)) for row in cursor.fetchall()]


def index(request):

  cursor = connection.cursor()
  cursor.execute("SELECT * , DATE_FORMAT(waktu, '%d/%m/%y %H:%i:%s') as fwaktu FROM riwayat ORDER BY id DESC")
  data_pengujian = dictfetchall(cursor)
  cursor.close()

  context = {
      'db_pengujian': data_pengujian,
      'title': 'Sistem Pemantauan Kesehatan | Tugas Akhir',
      'heading': 'Sistem Pemantauan Kesehatan',
      'subheading': 'Alessandro Sulistyo',
      'foot': 'Alessandro Sulistyo',
  }
  return render(request, 'riwayat.html', context)
