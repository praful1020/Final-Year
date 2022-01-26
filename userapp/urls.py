from django.urls import path
from . import views

urlpatterns = [
    path('',views.ulogin,name='ulogin'),
    path('ulogout',views.ulogin,name='ulogout'),
    path ('uindex',views.uindex,name='uindex'),
    path ('uprofile',views.uprofile,name='uprofile'),
    path('uchange-password/',views.uchange_password,name='uchange-password'),
    path ('view-event',views.view_event,name='view-event'),
    path ('utables',views.utables,name='utables'),




    

]