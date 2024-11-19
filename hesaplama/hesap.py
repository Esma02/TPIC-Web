from datetime import datetime, timedelta

class MesaiHesaplama:
    
    def hesapla_fazla_mesai(self, baslangic: datetime, bitis: datetime) -> float:
        toplam_fazla_mesai = 0
        current_day_start = baslangic
        
        while current_day_start < bitis:
            if current_day_start.date() == bitis.date():
                current_day_end = bitis
            else:
                current_day_end = datetime.combine(current_day_start.date() + timedelta(days=1), datetime.min.time()) - timedelta(seconds=1)
            
            toplam_fazla_mesai += self.hesapla_gunluk_fazla_mesai(current_day_start, current_day_end)
            
            current_day_start = current_day_end + timedelta(seconds=1)
        
        return toplam_fazla_mesai

    def hesapla_gunluk_fazla_mesai(self, baslangic: datetime, bitis: datetime) -> float:
        gunluk_fazla_mesai = 0
        
        # Hafta içi
        if baslangic.weekday() >= 0 and baslangic.weekday() <= 4:  # Pazartesi - Cuma
            calisma_baslangici = datetime.combine(baslangic.date(), datetime.min.time()) + timedelta(hours=8)
            calisma_bitisi = datetime.combine(baslangic.date(), datetime.min.time()) + timedelta(hours=17)
            
            if baslangic < calisma_baslangici:
                if bitis <= calisma_baslangici:
                    gunluk_fazla_mesai += (bitis - baslangic).total_seconds() / 3600
                elif bitis > calisma_bitisi:
                    gunluk_fazla_mesai += ((calisma_baslangici - baslangic) + (bitis - calisma_bitisi)).total_seconds() / 3600
                else:
                    gunluk_fazla_mesai += (calisma_baslangici - baslangic).total_seconds() / 3600
            else:
                if baslangic > calisma_bitisi:
                    gunluk_fazla_mesai += (bitis - baslangic).total_seconds() / 3600
                elif bitis > calisma_bitisi:
                    gunluk_fazla_mesai += (bitis - calisma_bitisi).total_seconds() / 3600

            if baslangic.time() < datetime.strptime("13:00", "%H:%M").time() and bitis.time() > datetime.strptime("12:00", "%H:%M").time():
                if bitis.time() < datetime.strptime("12:30", "%H:%M").time():
                    gunluk_fazla_mesai += 0.5
                else:
                    gunluk_fazla_mesai += 1
                    
            if gunluk_fazla_mesai >= 6:
                gunluk_fazla_mesai = 6
        
        # Cumartesi
        elif baslangic.weekday() == 5: 
            calisma_baslangici = datetime.combine(baslangic.date(), datetime.min.time()) + timedelta(hours=8)
            calisma_bitisi = datetime.combine(baslangic.date(), datetime.min.time()) + timedelta(hours=12)
            
            if baslangic < calisma_baslangici:
                if bitis <= calisma_baslangici:
                    gunluk_fazla_mesai += (bitis - baslangic).total_seconds() / 3600
                elif bitis > calisma_bitisi:
                    gunluk_fazla_mesai += ((calisma_baslangici - baslangic) + (bitis - calisma_bitisi)).total_seconds() / 3600
                else:
                    gunluk_fazla_mesai += (calisma_baslangici - baslangic).total_seconds() / 3600
            else:
                if baslangic > calisma_bitisi:
                    gunluk_fazla_mesai += (bitis - baslangic).total_seconds() / 3600
                elif bitis > calisma_bitisi:
                    gunluk_fazla_mesai += (bitis - calisma_bitisi).total_seconds() / 3600
            
            if gunluk_fazla_mesai > 7.5:
                gunluk_fazla_mesai = 7.5
        
        # Pazar
        elif baslangic.weekday() == 6: 
            gunluk_fazla_mesai += (bitis - baslangic).total_seconds() / 3600
            if gunluk_fazla_mesai >= 10.5:
                gunluk_fazla_mesai = 10.5
                
        return gunluk_fazla_mesai

    def saat_donusturme(self, decimal_saat: float) -> str:
        saat = int(decimal_saat)
        decimal_dakika = (decimal_saat - saat) * 60
        dakika = int(round(decimal_dakika))
        
        if 0 < dakika <= 30:
            dakika = 30
        elif dakika > 30:
            dakika = 60
            
        if dakika == 60:
            saat += 1
            dakika = 0
            
        return f"{saat:02d}:{dakika:02d}"
    
    
    
    
    # def tarih_saat_donusturme(self, tarih: datetime, format_tipi: str = 'default') -> str:
    #    if format_tipi == 'default':
    #         return tarih.strftime('%d %B %Y %H:%M')  # "24 Ekim 2024 09:30" formatı
    #    elif format_tipi == 'alternative':
    #         return tarih.strftime('%d.%m.%Y %H:%M')  # "24.10.2024 09:30" formatı
    #    else:
    #         raise ValueError("Geçersiz format tipi.")
    
    
    

# a=datetime(2024,10,24,2,36,00)
# b=datetime(2024,10,24,7,36,00)
# x=Mesaima.hesapla_fazla_mesai(a,b)
# y=int(datetime.fromtimestamp(x))
# print(y)