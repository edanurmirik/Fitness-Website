from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app1.models import userInformation,antrenor,danisan,eslesme,danisan_kayitlari,egzersiz_beslenme_planlari,plan_eslesme
from itertools import zip_longest

@login_required(login_url='login')
def anasayfa(request):
    return HttpResponse("basariliii")

def HomePage(request):
    user_info = userInformation.objects.get(user=request.user)

    context = {
        'ad': user_info.ad,
        'soyad': user_info.soyad,
        'profilFotografi': user_info.profilFotografi.url if user_info.profilFotografi else None,
    }

    if user_info.rol == 'Danışan':
        return render(request, 'home_danisan.html', context)

    elif user_info.rol == 'Antrenör':
        return render(request, 'home_antrenor.html', context)

    return render(request, 'bilgileriKaydet.html', {"error":"Giriş Başarısız"})

def SignUpPage(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        repassword=request.POST.get('repassword')

        if password!=repassword:
            return render (request,'signup.html', {"error":"Passwords do not match"})
        else:
            my_user=User.objects.create_user(username,email,password)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method =='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('bilgileriKaydet')
        else:
            return render (request,'login.html', {"error":"Username or password incorrect"})

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def bilgileriKaydet(request):
    user_id = request.user.id
    print(user_id)

    existing_record = userInformation.objects.filter(user_id=user_id).exists()
    user_info = userInformation.objects.filter(user_id=user_id).first()

    if existing_record:
        context = {
        'ad': user_info.ad,
        'soyad': user_info.soyad,
    }
        return redirect('home')

    if request.method== 'POST':
        user_id=user_id
        ad=request.POST.get('ad')
        soyad=request.POST.get('soyad')
        dogumTarihi=request.POST.get('dogumTarihi')
        cinsiyet=request.POST.get('cinsiyet')
        telefonNumarasi=request.POST.get('telefonNumarasi')
        profilFotografi=request.POST.get('profilFotografi')
        rol=request.POST.get('rol')

        my_user=userInformation(user_id=user_id,ad=ad,soyad=soyad,dogumTarihi=dogumTarihi,cinsiyet=cinsiyet,telefonNumarasi=telefonNumarasi,profilFotografi=profilFotografi,rol=rol)
        my_user.save()

        return redirect('home')
        
    return render (request,'bilgileriKaydet.html')

def danisanBilgileriKaydet(request):
    user_id = request.user.id
    existing_record = danisan.objects.filter(user_id=user_id).exists()

    if existing_record:
        danisan_obj = danisan.objects.get(user_id=user_id)
        if request.method == 'POST':
            danisan_obj.kilo = request.POST.get('kilo')
            danisan_obj.boy = request.POST.get('boy')
            danisan_obj.vucutYagOrani = request.POST.get('vucutyagorani')
            danisan_obj.kasKutlesi = request.POST.get('kaskutlesi')
            danisan_obj.vucutKitleIndeksi = request.POST.get('vucutkitleindeksi')
            danisan_obj.istek = request.POST.get('istek')
            danisan_obj.save()

            # Danışanın isteğine uygun antrenör bulma işlemi
            exist1 = antrenor.objects.filter(uzmanlikAlani=danisan_obj.istek).exists()
            if exist1:
                antrenor_list = antrenor.objects.filter(uzmanlikAlani=danisan_obj.istek)

                # En fazla 5 danışanı olan bir antrenörü bulma
                suitable_antrenor = None
                for antrenor_instance in antrenor_list:
                    danisan_count = eslesme.objects.filter(antrenor=antrenor_instance.user_id).count()
                    if danisan_count < 5:
                        suitable_antrenor = antrenor_instance
                        break

                # Eğer uygun antrenör bulunamazsa, farklı bir antrenör seç
                if suitable_antrenor is None:
                    suitable_antrenor = antrenor_list.first()

                # Danışanı uygun antrenöre eşle
                my_user = eslesme(danisan=user_id, antrenor=suitable_antrenor.user_id)
                my_user.save()

            return redirect('home')

    if request.method == 'POST':
        user_id = user_id
        kilo = request.POST.get('kilo')
        boy = request.POST.get('boy')
        vucutyagorani = request.POST.get('vucutyagorani')
        kaskutlesi = request.POST.get('kaskutlesi')
        vucutkitleindeksi = request.POST.get('vucutkitleindeksi')
        istek = request.POST.get('istek')

        my_user = danisan(user_id=user_id, kilo=kilo, boy=boy, vucutYagOrani=vucutyagorani,
                           kasKutlesi=kaskutlesi, vucutKitleIndeksi=vucutkitleindeksi, istek=istek)
        my_user.save()

        # Danışanın isteğine uygun antrenör bulma işlemi
        exist1 = antrenor.objects.filter(uzmanlikAlani=istek).exists()
        if exist1:
            antrenor_list = antrenor.objects.filter(uzmanlikAlani=istek)

            # En fazla 5 danışanı olan bir antrenörü bulma
            suitable_antrenor = None
            for antrenor_instance in antrenor_list:
                danisan_count = eslesme.objects.filter(antrenor=antrenor_instance.user_id).count()
                if danisan_count < 5:
                    suitable_antrenor = antrenor_instance
                    break

            # Eğer uygun antrenör bulunamazsa, farklı bir antrenör seç
            if suitable_antrenor is None:
                suitable_antrenor = antrenor_list.first()

            # Danışanı uygun antrenöre eşle
            my_user = eslesme(danisan=user_id, antrenor=suitable_antrenor.user_id)
            my_user.save()

        return redirect('home')

    return render(request, 'fizikselOzelliklerKaydet.html')  # Burada HTML dosya adını düzelttim


def antrenorBilgileriKaydet(request):
    user_id = request.user.id

    existing_record = antrenor.objects.filter(user_id=user_id).exists()
    if existing_record:
        antrenor_obj = antrenor.objects.get(user_id=user_id)
        if request.method == 'POST':
            user_id = user_id
            antrenor_obj.uzmanlikAlani = request.POST.get('uzmanlikAlani')
            antrenor_obj.deneyim = request.POST.get('deneyim')
            antrenor_obj.save()
            return redirect('home')

    if request.method== 'POST':
        user_id = user_id
        uzmanlikAlani = request.POST.get('uzmanlikAlani')
        deneyim = request.POST.get('deneyim')

        my_user=antrenor(user_id=user_id,uzmanlikAlani=uzmanlikAlani,deneyim=deneyim)
        my_user.save()
        return redirect('home')
            
    return render (request,'deneyimBilgileriKaydet.html')

def ilerlemeKayitlari(request):
    user_id = request.user.id

    if request.method== 'POST':
        user_id=user_id
        tarih=request.POST.get('tarih')
        kilo=request.POST.get('kilo')
        vucutyagorani=request.POST.get('vucutyagorani')
        kaskutlesi=request.POST.get('kaskutlesi')
        vucutkitleindeksi=request.POST.get('vucutkitleindeksi')

        my_user=danisan_kayitlari(user_id=user_id,tarih=tarih,kilo=kilo,vucutYagOrani=vucutyagorani,kasKutlesi=kaskutlesi,vucutKitleIndeksi=vucutkitleindeksi)
        my_user.save()

        return redirect('ilerlemeKayitlariGor')

    return render(request, 'ilerlemeKayitlari.html')

def ilerlemeKayitlariGor(request):
    user_id = request.user.id

    rol = userInformation.objects.get(user_id=user_id)
    if rol.rol == "Danışan":
        existing_record = danisan_kayitlari.objects.filter(user_id=user_id).exists()
        if existing_record:
            progress_records = danisan_kayitlari.objects.filter(user_id=user_id).all()
            return render(request, 'ilerlemeKayitlariGor.html', {'progress_records': progress_records})
        else:
            return render(request, 'ilerlemeKayitlari.html', {"error":"Geçmişe ait kayıt bulunamamıştır."})
    else: 
        return render(request, 'ilerlemeKayitlariGor.html')

    return render(request, 'ilerlemeKayitlariGor.html')

def danisanListele(request):
    user_id = request.user.id
    danisan_records = eslesme.objects.filter(antrenor=user_id).all()

    danisan_listesi = []
    liste = []

    for record in danisan_records:
        danisan_user = userInformation.objects.get(user_id=record.danisan)
        danisan_listesi.append(danisan_user)
        x = danisan.objects.get(user_id=record.danisan)
        liste.append(x)

        birlesik_liste = zip_longest(danisan_listesi, liste, fillvalue=None)

    return render(request, 'danisanBilgileri.html', {'birlesik_liste': birlesik_liste})

def planOlusturma(request):
    user_id = request.user.id

    if request.method== 'POST':
        user_id=user_id
        istek=request.POST.get('istek')
        egzersiz_content=request.POST.get('egzersiz_content')
        beslenme_content=request.POST.get('beslenme_content')
        baslik=request.POST.get('baslik')

        my_user=egzersiz_beslenme_planlari(antrenor_id=user_id,istek=istek,egzersiz_content=egzersiz_content,beslenme_content=beslenme_content,baslik=baslik)
        my_user.save()

        return redirect('planOlusturma')

    return render(request, 'planOlusturma.html')

def planAtama(request):
    user_id = request.user.id

    egzersiz_beslenme_listesi = egzersiz_beslenme_planlari.objects.filter(antrenor_id=user_id)

    if request.method== 'POST':
        user_id=user_id
        istek=request.POST.get('istek')
        ad=request.POST.get('ad')
        soyad=request.POST.get('soyad')

        danisan_id = userInformation.objects.get(ad=ad,soyad=soyad)
        plan = egzersiz_beslenme_planlari.objects.get(baslik=istek)

        my_user=plan_eslesme(antrenor_id=user_id,plan_id=plan.id,danisan=danisan_id.user_id)
        my_user.save()

    return render(request, 'planAtama.html', {'egzersiz_beslenme_listesi': egzersiz_beslenme_listesi})

def egzersiz_beslenme_plani_gor(request):
    user_id = request.user.id
    my_user = plan_eslesme.objects.get(danisan=user_id)
    plan = egzersiz_beslenme_planlari.objects.get(id=my_user.plan_id)

    return render(request, 'egzersiz_beslenme_plani.html', {'plan':plan})