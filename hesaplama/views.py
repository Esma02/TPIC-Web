from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import RegisterForm, MesaiKaydiForm
from .models import MesaiKaydi 
from .hesap import MesaiHesaplama 
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.db.models import Sum
from django.views import View


class LoginView(View):
    template_name = 'index.html' 
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

      
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  
            return redirect('mesai_view') 
        else:
            messages.error(request, 'Geçersiz Kullanıcı Adı veya Şifre')
            return render(request, self.template_name, {'error': 'Geçersiz Kullanıcı Adı veya Şifre'})  
        
        
        

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_page')
    
    
    
    


class RegisterView(View):
    template_name = 'kayitol.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Hesap başarıyla oluşturuldu ve giriş yapıldı.')
            return redirect('login_page')
        return render(request, self.template_name, {'form': form})




class MesaiView(View):
    template_name = 'mesai.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('mesai_view')

class MesaiListesiView(View):
    template_name = 'mesaiListesi.html'

    def get(self, request):
        if request.user.is_authenticated:
            mesai_list = MesaiKaydi.objects.filter(kullanici=request.user).order_by('-baslangic_tarihi')
            return render(request, self.template_name, {'mesai_list': mesai_list})
        else:
            return redirect('login_page')

class MesaiKaydiView(View):
    template_name = 'mesaiKaydi.html'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('login_page')

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login_page')

        # Formdan gelen verileri al
        baslangic_tarihi = request.POST.get('baslangic_tarihi')
        bitis_tarihi = request.POST.get('bitis_tarihi')
        muhendis = request.POST.get('muhendis')
        yapilan_is = request.POST.get('yapilan_is')
        kule_adi = request.POST.get('kule_adi')
        kule_tipi = request.POST.get('kule_tipi')
        aciklama = request.POST.get('aciklama')

        try:
            # Tarihleri datetime nesnesine çevir
            baslangic_tarihi_obj = datetime.strptime(baslangic_tarihi, '%Y-%m-%dT%H:%M')
            bitis_tarihi_obj = datetime.strptime(bitis_tarihi, '%Y-%m-%dT%H:%M')

            # Başlangıç tarihi, bitiş tarihinden küçük olmalı
            if baslangic_tarihi_obj >= bitis_tarihi_obj:
                messages.error(request, 'Başlangıç tarihi, bitiş tarihinden daha küçük olmalıdır.')
                return redirect('mesai_kaydi')

            # Fazla mesai hesaplama
            mesai_hesaplama = MesaiHesaplama()
            fazla_mesai_saat = mesai_hesaplama.hesapla_fazla_mesai(baslangic_tarihi_obj, bitis_tarihi_obj)
            saat_degeri = mesai_hesaplama.saat_donusturme(fazla_mesai_saat)

            # Mesai kaydını oluştur
            MesaiKaydi.objects.create(
                kullanici=request.user,
                baslangic_tarihi=baslangic_tarihi_obj,
                bitis_tarihi=bitis_tarihi_obj,
                muhendis=muhendis,
                yapilan_is=yapilan_is,
                kule_adi=kule_adi,
                kule_tipi=kule_tipi,
                aciklama=aciklama,
                sonuc=saat_degeri  # Sayısal değer olarak kaydediliyor
            )

            messages.success(request, 'Mesai kaydı başarıyla oluşturuldu.')
            return redirect('mesai_listesi')

        except ValueError:
            messages.error(request, 'Tarih formatı geçersiz. Lütfen YYYY-MM-DDTHH:MM formatında tarih girin.')
            return redirect('mesai_kaydi')
        except Exception as e:
            messages.error(request, f'Mesai kaydı oluşturulurken bir hata oluştu: {str(e)}')
            return redirect('mesai_kaydi')
        
        
class MesaiSilView(View):
    def post(self, request, mesai_id):
        if request.user.is_authenticated:
            mesai_kaydi = get_object_or_404(MesaiKaydi, id=mesai_id, kullanici=request.user)
            mesai_kaydi.delete()
            messages.success(request, 'Mesai kaydı başarıyla silindi.')
        else:
            messages.error(request, 'Silme işlemi için giriş yapmalısınız.')
        return redirect('mesai_listesi')
    

class FazlaMesaiView(View):
    def get(self, request):
        return render(request, 'filtre.html', {})

    def post(self, request):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            records = MesaiKaydi.objects.filter(
                kullanici=request.user,
                baslangic_tarihi__gte=start_date,
                bitis_tarihi__lte=end_date + timedelta(days=1)
            )

            toplam_saat = 0
            toplam_dakika = 0

            for record in records:
                if isinstance(record.sonuc, str):
                    saat, dakika = map(int, record.sonuc.split(':'))
                    toplam_saat += saat
                    toplam_dakika += dakika
                else:
                    toplam_saat += int(record.sonuc)
                    toplam_dakika += (record.sonuc % 1) * 60  

            toplam_saat += toplam_dakika // 60
            toplam_dakika = toplam_dakika % 60

            if toplam_dakika >= 30:
                toplam_saat += 1
                toplam_dakika -= 60  

            toplam_saat += toplam_dakika / 60.0  

            context = {
                'records': records,
                'start_date': start_date,
                'end_date': end_date,
                'toplamzaman': toplam_saat,
            }
            return render(request, 'filtre.html', context)

        except ValueError:
            messages.error(request, 'Geçersiz tarih formatı. Lütfen YYYY-MM-DD formatında tarih girin.')
            return redirect('filtre')