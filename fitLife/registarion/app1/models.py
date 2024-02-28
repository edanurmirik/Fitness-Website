from django.db import models
from django.contrib.auth.models import User

class userInformation(models.Model):
    user= models.ForeignKey(User,default=1 ,on_delete=models.CASCADE)
    ad=models.CharField(max_length=50)
    soyad=models.CharField(max_length=50)
    dogumTarihi=models.DateField()
    cinsiyetler=(
        ('E', 'Erkek'),
        ('K', 'Kadın'),
        ('D', 'Diğer'),
    )
    cinsiyet = models.CharField(max_length=1, choices=cinsiyetler, null=True)
    telefonNumarasi=models.CharField(max_length=20)
    profilFotografi=models.ImageField(upload_to='profile_images', blank=True, null=True)
    rol=models.CharField(default='null',max_length=20)

class antrenor(models.Model):
    user = models.ForeignKey(User,default=1 ,on_delete=models.CASCADE)
    uzmanlikAlanlari=(
        ('KA','Kilo Aldırma'),
        ('KV','Kilo Verdirme'),
        ('KK','Kilo Koruma'),
        ('KKA','Kas Kazandırma')
    )
    uzmanlikAlani=models.CharField(max_length=3, choices=uzmanlikAlanlari, null=True)
    deneyim=models.CharField(max_length=20)

class danisan(models.Model):
    user = models.ForeignKey(User, default=1 ,on_delete=models.CASCADE)
    kilo=models.FloatField()
    boy=models.FloatField()
    vucutYagOrani=models.FloatField()
    kasKutlesi=models.FloatField()
    vucutKitleIndeksi=models.FloatField()
    istekler=(
        ('KA','Kilo Aldırma'),
        ('KV','Kilo Verdirme'),
        ('KK','Kilo Koruma'),
        ('KKA','Kas Kazandırma')
    )
    istek=models.CharField(max_length=3, choices=istekler, null=True)

class eslesme(models.Model):
    danisan = models.IntegerField()
    antrenor = models.IntegerField()

class danisan_kayitlari(models.Model):
    user=models.ForeignKey(User, default=1 ,on_delete=models.CASCADE)
    tarih=models.DateField()
    kilo=models.FloatField()
    vucutYagOrani=models.FloatField()
    kasKutlesi=models.FloatField()
    vucutKitleIndeksi=models.FloatField()

class egzersiz_beslenme_planlari(models.Model):
    istekler=(
        ('KA','Kilo Aldırma'),
        ('KV','Kilo Verdirme'),
        ('KK','Kilo Koruma'),
        ('KKA','Kas Kazandırma')
    )
    istek=models.CharField(max_length=3, choices=istekler, null=True)
    egzersiz_content=models.TextField()
    beslenme_content=models.TextField()
    antrenor = models.ForeignKey(User,default=1 ,on_delete=models.CASCADE)
    baslik = models.TextField(default=" ")

class plan_eslesme(models.Model):
    antrenor = models.ForeignKey(User,default=1 ,on_delete=models.CASCADE)
    plan_id = models.CharField(max_length=3)
    danisan = models.CharField(max_length=3)

