from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    # path("", views.daftar_pengeluaran, name="daftar_pengeluaran"),
    path("registrasi/", views.register, name="registrasi"),
    path("", views.dashboard, name="dashboard"),
    path("tanggal/<str:tanggal>", views.detail_pengeluaran_tanggal, name="detail_pengeluaran_tanggal"),
    path("catatanHarian/", views.set_catatan_harian, name="set_catatan_harian"),
    path("batasHarian/", views.batas_pengeluaran_harian, name="batas_pengeluaran_harian"),
    
    path("tambah/", views.tambah_pengeluaran, name="tambah_pengeluaran"),
    path("edit/<int:id>/", views.edit_pengeluaran, name="edit_pengeluaran"),
    path("hapus/<int:id>/", views.hapus_pengeluaran, name="hapus_pengeluaran"),
]
