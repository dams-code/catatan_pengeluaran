from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pengeluaran, CatatanHarian, BatasPengeluaranHarian
from .forms import PengeluaranForm, RegistrasiForm, CatatanHarianForm, BatasPengeluaranHarianForm
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta

from django.contrib.auth import login


# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == "POST":
        form = RegistrasiForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegistrasiForm()
        
    return render(request, "registration/registrasi.html", {
        "form": form
    })

@login_required
def dashboard(request):
    hari_ini = timezone.localdate()
    
    daftar_tanggal = []
    chart_tanggal_label = []
    chart_tanggal_data = []
    
    for i in range(6,-1,-1):
        tanggal = hari_ini - timedelta(days=i)
        
        total_harian = Pengeluaran.objects.filter(
            user=request.user,
            tanggal = tanggal
        ).aggregate(
            total = Sum("jumlah")
        )["total"] or 0
        
        daftar_tanggal.append(tanggal)
        chart_tanggal_label.append(tanggal.strftime("%d %b"))
        chart_tanggal_data.append(float(total_harian))
    
    daftar_tanggal = []
    
    for i in range(7):
        tanggal = hari_ini - timedelta(days=i)
        daftar_tanggal.append(tanggal)
        
    return render(request, "transaksi/dashboard.html", {
        "daftar_tanggal": daftar_tanggal,
        "hari_ini": hari_ini,
        "daftar_tanggal": daftar_tanggal,
        "chart_tanggal_label": chart_tanggal_label,
        "chart_tanggal_data": chart_tanggal_data,
    })
    
@login_required
def detail_pengeluaran_tanggal(request, tanggal):
    hari_ini = timezone.localdate()

    try:
        tanggal_dipilih = datetime.strptime(tanggal, "%Y-%m-%d").date()
    except ValueError:
        return redirect("dashboard")
    
    if tanggal_dipilih > hari_ini:
        return redirect("dashboard")
    
    data_pengeluaran = Pengeluaran.objects.filter(
        user=request.user,
        tanggal = tanggal_dipilih
    ).order_by("-created_at")
    
    total_pengeluaran = data_pengeluaran.aggregate(
        total=Sum("jumlah")
    )["total"] or 0
    
    total_per_kategori = data_pengeluaran.values(
        "kategori__nama"
    ).annotate(
        total = Sum("jumlah")
    ).order_by(
        "kategori__nama"
    )
    
    boleh_ubah = tanggal_dipilih == hari_ini
    
    
    catatan_harian = CatatanHarian.objects.filter(
        user = request.user,
        tanggal = tanggal_dipilih
    ).first()
    
    batas_harian = BatasPengeluaranHarian.objects.filter(
        user = request.user,
        tanggal = tanggal_dipilih
    ).first()
    
    jumlah_batas = batas_harian.jumlah_batas if batas_harian else 0
    
    if batas_harian:
        if total_pengeluaran > jumlah_batas:
            status_pengeluaran = "Boros"
            status_class = "danger"
        else:
            status_pengeluaran = "Aman"
            status_class = "success"
    else:
        status_pengeluaran = "Belum Set Batas Pengeluaran"
        status_class = "secondary"
        
    chart_kategori_label = []
    chart_kategori_data = []
    
    for item in total_per_kategori:
        chart_kategori_label.append(item["kategori__nama"] or "Tanpa Kategori")
        chart_kategori_data.append(float(item["total"]))
        
    chart_pengeluaran_label = []
    chart_pengeluaran_data = []
    
    for item in data_pengeluaran:
        chart_pengeluaran_label.append(item.judul)
        chart_pengeluaran_data.append(item.jumlah)
    
    
    return render(request, "transaksi/detail_tanggal.html", {
        "tanggal_dipilih": tanggal_dipilih,
        "data_pengeluaran": data_pengeluaran,
        "total_pengeluaran": total_pengeluaran,
        "total_per_kategori": total_per_kategori,
        "boleh_ubah": boleh_ubah,
        "catatan_harian": catatan_harian,
        "batas_harian": batas_harian,
        "jumlah_batas": jumlah_batas,
        "status_pengeluaran": status_pengeluaran,
        "status_class": status_class,
        "chart_kategori_label": chart_kategori_label,
        "chart_kategori_data": chart_kategori_data,
        "chart_pengeluaran_label": chart_pengeluaran_label,
        "chart_pengeluaran_data": chart_pengeluaran_data,
    })

@login_required
def set_catatan_harian(request):
    hari_ini = timezone.localdate()
    
    catatan_harian = CatatanHarian.objects.filter(
        user=request.user,
        tanggal=hari_ini
    ).first()
    
    if request.method == "POST":
        form = CatatanHarianForm(request.POST, instance=catatan_harian)
        
        if form.is_valid():
            catatan = form.save( commit=False )
            catatan.user = request.user
            catatan.tanggal = hari_ini
            catatan.save()
            
            return redirect("detail_pengeluaran_tanggal", tanggal=hari_ini)
    else:
        form = CatatanHarianForm(instance=catatan_harian)
        
    return render(request, "transaksi/form_CatatanHarian.html", {
        "form": form,
        "hari_ini": hari_ini,
        "catatan_harian": catatan_harian
    })
    
@login_required
def batas_pengeluaran_harian(request):
    hari_ini = timezone.localdate()
    
    batas_harian = BatasPengeluaranHarian.objects.filter(
        user = request.user,
        tanggal = hari_ini
    ).first()
    
    if request.method == "POST":
        form = BatasPengeluaranHarianForm(request.POST, instance=batas_harian)
        
        if form.is_valid():
            batas = form.save(commit=False)
            batas.user = request.user
            batas.tanggal = hari_ini
            batas.save()
            
            return redirect("detail_pengeluaran_tanggal", tanggal=hari_ini)
        
    else:
        form = BatasPengeluaranHarianForm(instance=batas_harian)
    
    return render(request, "transaksi/form_BatasHarian.html", {
        "form": form,
        "hari_ini": hari_ini,
        "batas_harian": batas_harian
    })

# @login_required
# def daftar_pengeluaran(request):
#     data_pengeluaran = Pengeluaran.objects.filter(user=request.user).order_by("-tanggal")
    
#     total_per_kategori = Pengeluaran.objects.filter(user=request.user).values(
#         "kategori__nama"
#     ).annotate(
#         total=Sum("jumlah")
#     ).order_by(
#         "kategori__nama"
#     )
    
#     total_semua = Pengeluaran.objects.filter(user=request.user).aggregate(
#         total=Sum("jumlah")
#     )["total"] or 0
    
    
#     return render(request, "transaksi/daftar_pengeluaran.html", {
#         "data_pengeluaran": data_pengeluaran,
#         "total_per_kategori": total_per_kategori,
#         "total_semua": total_semua
#     })

@login_required
def tambah_pengeluaran(request):
    
    hari_ini = timezone.localdate()
    
    if request.method == "POST":
        form = PengeluaranForm(request.POST)
        
        if form.is_valid():
            pengeluaran = form.save(commit=False)
            pengeluaran.user = request.user
            
            pengeluaran.tanggal = hari_ini
            
            pengeluaran.save()
            # return redirect("daftar_pengeluaran")
            return redirect("detail_pengeluaran_tanggal", tanggal=hari_ini)
        
    else:
        form = PengeluaranForm()
        
    return render(request, "transaksi/form_pengeluaran.html", {
        "form": form,
        "judul": "Tambah Pengeluaran",
        "hari_ini": hari_ini
    })
    
@login_required
def edit_pengeluaran(request, id):
    
    hari_ini = timezone.localdate()
    
    pengeluaran = get_object_or_404(Pengeluaran, id=id, user=request.user)
    
    if pengeluaran.tanggal != hari_ini:
        messages.error(request, "Data Pengeluaran Lama Hanya bisa dilihat Saja")
        return redirect("detail_pengeluaran_tanggal", tanggal=pengeluaran.tanggal)
    
    if request.method == "POST":
        form = PengeluaranForm(request.POST, instance=pengeluaran)
        
        if form.is_valid():
            data = form.save(commit=False)
            
            data.tanggal = hari_ini
            
            data.save()
            # return redirect("daftar_pengeluaran")
            return redirect("detail_pengeluaran_tanggal", tanggal=hari_ini)
    else:
        form = PengeluaranForm(instance=pengeluaran)
        
    return render(request, "transaksi/form_pengeluaran.html", {
        "form": form,
        "judul": "Edit Pengeluaran Hari Ini"
    })    
    
@login_required
def hapus_pengeluaran(request, id):
    hari_ini = timezone.localdate()
    
    pengeluaran = get_object_or_404(Pengeluaran, id=id, user=request.user)
    
    if pengeluaran.tanggal != hari_ini:
        messages.error(request, "Data Pengeluaran Lama Hanya bisa dilihat Saja")
        return redirect("detail_pengeluaran_tanggal", tanggal=pengeluaran.tanggal)
    
    if request.method == "POST":
        pengeluaran.delete()
        return redirect("detail_pengeluaran_tanggal", tanggal=hari_ini)
    
    return render(request, "transaksi/hapus_pengeluaran.html", {
       "pengeluaran": pengeluaran 
    })
    
    