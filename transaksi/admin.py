from django.contrib import admin
from .models import Kategori, Pengeluaran, CatatanHarian, BatasPengeluaranHarian

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    list_display = ("nama", "user", "created_at")
    search_fields = ("nama",)
    
    
@admin.register(Pengeluaran)
class PengeluaranAdmin(admin.ModelAdmin):
    list_display = ("judul", "kategori", "jumlah", "tanggal", "metode_pembayaran", "user")
    list_filter = ("kategori", "metode_pembayaran", "tanggal")
    search_fields = ("judul", "catatan")


@admin.register(CatatanHarian)
class CatatanHarianAdmin(admin.ModelAdmin):
    list_display = ("user", "tanggal", "created_at")
    search_fields = ("user__username", "catatan")
    list_filter = ("tanggal",)
    
    
@admin.register(BatasPengeluaranHarian)
class BatasPengeluaranHarianAdmin(admin.ModelAdmin):
    list_display = ("user", "tanggal", "jumlah_batas", "created_at")
    search_fields = ("user__username",)
    list_filter = ("tanggal",)
    
# Register your models here.
