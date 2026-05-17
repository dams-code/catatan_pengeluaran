from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Kategori(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nama
    
    
class Pengeluaran(models.Model):
    METODE_PEMBAYARAN = [
        ("cash", "Cash"),
        ("transfer", "Transfer Bank"),
        ("ewallet", "E-Wallet"),
        ("kartu_debit", "Kartu Debit"),
        ("kartu_kredit", "Kartu Kredit"),
        ("qris", "QRIS"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.SET_NULL,
        null=True,
        related_name="pengeluaran"
    )
    judul = models.CharField(max_length=150)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal = models.DateField()
    metode_pembayaran = models.CharField(
        max_length=20,
        choices=METODE_PEMBAYARAN,
        default="cash"
    )
    catatan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.judul

class CatatanHarian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal = models.DateField()
    catatan =models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("user", "tanggal")
        
    def __str__(self):
        return f"Catatan {self.user.username} - {self.tanggal}"
    
class BatasPengeluaranHarian(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tanggal = models.DateField()
    jumlah_batas = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ("user", "tanggal")
        
    def __str__(self):
        return f"Batas {self.user.username} - {self.tanggal}"