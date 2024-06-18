from django.urls import path
from . import views

urlpatterns = [
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('create_ad/', views.create_ad, name='create_ad'),
    path('list_ads/', views.list_ads, name='list_ads'),
    path('calculate_delivery_fee/', views.calculate_delivery_fee, name='calculate_delivery_fee'),
]
