from django import forms
from .models import Pengeluaran, CatatanHarian, BatasPengeluaranHarian

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PengeluaranForm(forms.ModelForm):
    class Meta:
        model = Pengeluaran
        fields = [
            "kategori",
            "judul",
            "jumlah",
            "metode_pembayaran",
            "catatan",
        ]
        
        widgets = {
            "kategori": forms.Select(attrs={"class": "form-select"}),
            "judul": forms.TextInput(attrs={"class": "form-control"}),
            "jumlah": forms.NumberInput(attrs={"class": "form-control"}),
            "metode_pembayaran": forms.Select(attrs={"class": "form-select"}),
            # "tanggal": forms.DateInput(attrs={"type":"date"}),
            "catatan": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

class RegistrasiForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Masukan Username"
            }),
        }
        
class CatatanHarianForm(forms.ModelForm):
    class Meta:
        model = CatatanHarian
        fields = ["catatan"]
        
        widgets = {
            "catatan": forms.Textarea(attrs={
               "class": "form-control",
               "rows": 4,
               "placeholder": "Isi hasil catatan, hari ini meeting, ngopi, cuci pakaian, dll" 
            }),
        }
        
class BatasPengeluaranHarianForm(forms.ModelForm):
    class Meta:
        model = BatasPengeluaranHarian
        fields = ["jumlah_batas"]
        
        widgets = {
            "jumlah_batas": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Rp. 100000"
            })
        }
        
def __init__(self, *args, **kwargs):
    super(RegistrasiForm, self).__init__(*args, **kwargs)
    
    self.field["username"].widget.attrs.update({
        "class": "form-control",
        "placeholder": "Masukan Username"
    })
    
    self.field["password1"].widget.attrs.update({
        "class": "form-control",
        "placeholder": "Masukan Password",
        "onpaste": "return false",
        "autocomplete": "new-password"
    })
    
    self.field["password2"].widget.attrs.update({
        "class": "form-control",
        "placeholder": "Konfirm Password",
        "onpaste": "return false",
        "autocomplete": "new-password"
    })
