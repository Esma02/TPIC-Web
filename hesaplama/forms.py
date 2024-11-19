from django import forms
from django.contrib.auth.models import User
from .models import MesaiKaydi

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Şifre (Tekrar)')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if password != password_confirm:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        
        return cleaned_data

class MesaiKaydiForm(forms.ModelForm):
    class Meta:
        model = MesaiKaydi
        fields = ['baslangic_tarihi', 'bitis_tarihi', 'muhendis', 'yapilan_is', 'kule_adi', 'kule_tipi', 'aciklama', 'sonuc']
        widgets = {
            'baslangic_tarihi': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'format': '%Y-%m-%dT%H:%M' 
            }),
            'bitis_tarihi': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'format': '%Y-%m-%dT%H:%M' 
            }),
            'aciklama': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['muhendis'].required = False
        self.fields['yapilan_is'].required = False
        self.fields['kule_adi'].required = False
        self.fields['kule_tipi'].required = False
        self.fields['aciklama'].required = False
        self.fields['sonuc'].required = True 
