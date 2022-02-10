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
    path('logout/',views.logout,name='logout'),
    path('add-event/',views.add_event,name='add-event'),
    path('all-event/',views.all_event,name='all-event'),
    path('edit-event/<int:pk>',views.edit_event,name='edit-event'),
    path('delete-event/<int:pk>',views.delete_event,name='delete-event'),
    path('change-password/',views.change_password,name='change-password'),
    path('view-complain/',views.view_complain,name='view-complain'),
    path('addmember/',views.addmember,name='addmember'),
    path('view-details/<int:pk>',views.viewdetails,name='view-details'),
    path('delete-complain/<int:pk>',views.delete_complain,name='delete-complain'),
    path('solve/<int:pk>',views.solve,name='solve'),
    path('event-details/<int:pk>',views.eventdetails,name='event-details'),
    path('gallery/',views.gallery,name='gallery'),



    


     
]