from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
<<<<<<< HEAD
    path ('index',views.index,name='index')
=======
    path('register/',views.register,name='register'),
>>>>>>> 71111026937d10ae570df1b051d88849c2e76326
]