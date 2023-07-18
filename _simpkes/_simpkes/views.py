from django.shortcuts import render


def index(request):
  context = {
      'title': 'Sistem Pemantauan Kesehatan | Tugas Akhir',
      'heading': 'Sistem Pemantauan Kesehatan',
      'subheading': 'Alessandro Sulistyo',
      'foot': 'Alessandro Sulistyo',
  }
  return render(request, 'index.html', context)
