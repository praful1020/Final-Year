from random import randrange
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from myapp.models import Addmember
from myapp.models import Event

import userapp
from .models import *

# Create your views here.
def ulogin(request):  
    if request.method == 'POST':
        #  try:
            uid = Addmember.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['uemail'] = request.POST['email']
                return render(request,'uindex.html',{'uid':uid})
            else:
                return render(request,'ulogin.html',{'msg':'Wrong Password'})
        #  except:
        #      return render(request,'login.html',{'msg':'Wrong Email'})
    return render(request,'ulogin.html')    


def uindex(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    return render(request,'uindex.html',{'uid':uid})

def ulogout(request):
    del request.session['uemail']
    return redirect('ulogin')


def uprofile(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    if request.method == 'POST':
       uid.name = request.POST['name']
       uid.email = request.POST['email']
       uid.mobile = request.POST['mobile']
       uid.address = request.POST['address']
       uid.city = request.POST['city']
       uid.pincode = request.POST['pincode']
       uid.save()
    
    return render(request,'uprofile.html',{'uid':uid})


def uchange_password(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    if request.method == 'POST':
        if request.POST['oldpassword'] == uid.password:
            if request.POST['newpassword'] == request.POST['cpassword']:
                uid.password = request.POST['newpassword']
                uid.save()

                return render(request,'uchangepassword.html',{'msg':'Password Has been Changed'})
            return render(request,'uchangepassword.html',{'Both new passwords are not same'})
        return render(request,'uchangepassword.html',{'msg':'Old password is wrong'})
    return render(request,'uchangepassword.html',{'uid':uid})



def view_event(request):
    uid = Addmember.objects.get(email=request.session['email'])
    events = Event.objects.all()
    return render(request,'View-Events.html',{'uid':uid,'events':events})


def utables(request):
    uid = Addmember.objects.get(email=request.session['email'])
    return render(request,'utables.html',{'uid':uid})