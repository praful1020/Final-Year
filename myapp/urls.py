from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path ('index',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('otp/',views.otp,name='otp'),
    path('fpassword/',views.fpassword,name='fpassword'),
    path('profile/',views.profile,name='profile'),
    path('tables/',views.tables,name='tables'),

]