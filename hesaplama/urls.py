from django.urls import path
from .views import LoginView, LogoutView, RegisterView, MesaiView,MesaiSilView,MesaiListesiView,MesaiKaydiView,FazlaMesaiView

urlpatterns = [
    path('', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('mesai/', MesaiView.as_view(), name='mesai_view'),
    path('mesai_listesi/', MesaiListesiView.as_view(), name='mesai_listesi'),
    path('mesai_kaydi/', MesaiKaydiView.as_view(), name='mesai_kaydi'),
    path('mesai/sil/<int:mesai_id>/', MesaiSilView.as_view(), name='mesai_sil'), 
    path('filtre/', FazlaMesaiView.as_view(), name='filtre'),
   



]
