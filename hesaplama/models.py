from django.db import models
from django.contrib.auth.models import User

class MesaiKaydi(models.Model):
    baslangic_tarihi = models.DateTimeField()
    bitis_tarihi = models.DateTimeField()
    muhendis = models.CharField(max_length=100, null=True, blank=True)
    yapilan_is = models.CharField(max_length=200, null=True, blank=True)
    kule_adi = models.CharField(max_length=100, null=True, blank=True)
    kule_tipi = models.CharField(max_length=100, null=True, blank=True)
    aciklama = models.TextField( null=True, blank=True)
    sonuc = models.CharField(max_length=5)  # HH:MM formatı için yeterli uzunluk
    kullanici = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.baslangic_tarihi} - {self.bitis_tarihi})"

