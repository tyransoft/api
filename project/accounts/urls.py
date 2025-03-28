from django.urls import path
from .views import *



urlpatterns = [
    path('register-driver/',register_driver,name='register_driver'),
    path('register-customer/',register_customer,name='register_customer'),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('change-password-driver/',change_password,name='change_password'),
]