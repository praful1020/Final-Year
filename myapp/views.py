from asyncio import events
from urllib import request
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail
from userapp.models import *
from datetime import datetime


# Create your views here.
def login(request):
    if request.method == 'POST':
        #  try:
            uid = SecUser.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['email'] = request.POST['email']
                return render(request,'index.html',{'uid':uid})
            else:
                return render(request,'login.html',{'msg':'Wrong Password'})
        #  except:
        #      return render(request,'login.html',{'msg':'Wrong Email'})


    return render(request,'login.html')

def index(request):
    uid = SecUser.objects.get(email=request.session['email'])
    return render(request,'index.html',{'uid':uid})

def register(request):
    if request.method == 'POST':
        try:
            SecUser.objects.get(email=request.POST['email'])
            return render(request,'register.html',{'msg':'Email is already register'})
        except:
            otp = randrange(1111,9999)
            subject = 'Welcome to Soc Management App'
            message = f"""Hello {request.POST['name']}!!
            Your Verification OTP is : {otp}.
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            send_mail( subject, message, email_from, recipient_list )
            global temp
            temp = {
                'name' : request.POST['name'],
                'email' : request.POST['email'],
                'mobile' : request.POST['mobile'],
                'password' : request.POST['password'],
            }
            return render(request,'otp.html',{'otp':otp})

    else:
        return render(request,'register.html')
    
def otp(request):
    if request.method == 'POST':
        if request.POST['otp'] == request.POST['uotp']:
            global temp
            SecUser.objects.create(
                name = temp['name'],
                email = temp['email'],
                mobile = temp['mobile'],
                password = temp['password']
            )
            del temp
            msg = 'User created'
            return render(request,'login.html',{'msg':msg})
        else:
            msg = 'Incorrect OTP'
            return render(request,'otp.html',{'otp':request.POST['otp'],'msg':msg})

def fpassword(request):
    if request.method == 'POST':
        try:
            uid = SecUser.objects.get(email=request.POST['email'])
            s = ''.join(choices('abcqwertyuiioplkjhgfdsazxcvbnm9876543321',k=8))
            subject = 'Password has been reset'
            message = f"""Hello user your new password is : {s}
            """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email']]
            send_mail( subject, message, email_from, recipient_list )
            uid.password = s
            uid.save()
            return render(request,'login.html',{'msg':subject})
        except:
            msg = 'User IS Not Registered'
            return render(request,'login.html',{'msg':msg})
    return render(request,'fpassword.html')    

def profile(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
       uid.name = request.POST['name']
       uid.email = request.POST['email']
       uid.mobile = request.POST['mobile']
       uid.address = request.POST['address']
       uid.city = request.POST['city']
       uid.pincode = request.POST['pincode']
       uid.save()
    
    return render(request,'profile.html',{'uid':uid})


def tables(request):
    uid = SecUser.objects.get(email=request.session['email'])
    return render(request,'tables.html',{'uid':uid})

def logout(request):
    del request.session['email']
    return redirect('login')

def add_event(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if 'pic' in request.FILES: 
            Event.objects.create(
                uid = uid,
                title = request.POST['title'],
                des = request.POST['des'],
                pic = request.FILES['pic'],
                event_at = request.POST['date']
            )
        else:
            Event.objects.create(
                uid = uid,
                title = request.POST['title'],
                des = request.POST['des'],
                event_at = request.POST['date']
            )
        msg = 'Event Created'
        return render(request,'add-event.html',{'uid':uid,'msg':msg})

    return render(request,'add-event.html',{'uid':uid})

def all_event(request):
    uid = SecUser.objects.get(email=request.session['email'])
    events = Event.objects.all()[::-1]
    return render(request,'all-event.html',{'uid':uid,'events':events})

def delete_event(request,pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return redirect('all-event')


def edit_event(request,pk):
    event = Event.objects.get(id=pk)
    event_at = str(event.event_at)
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
        event.uid = uid
        event.title = request.POST['title']
        event.des = request.POST['des']
        event.event_at = request.POST['date'] 
        if 'pic' in request.FILES:
            event.pic = request.FILES['pic']
        event.save()

        return redirect('all-event')
    return render(request,'edit-event.html',{'uid':uid, 'event':event,'event_at':event_at})


def change_password(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if request.POST['oldpassword'] == uid.password:
            if request.POST['newpassword'] == request.POST['cpassword']:
                uid.password = request.POST['newpassword']
                uid.save()

                return render(request,'changepassword.html',{'msg':'Password Has been Changed'})
            return render(request,'changepassword.html',{'Both new passwords are not same'})
        return render(request,'changepassword.html',{'msg':'Old password is wrong'})
    return render(request,'changepassword.html',{'uid':uid})

def view_complain(request):
    uid = SecUser.objects.get(email=request.session['email'])
    complains = Complain.objects.all()[::-1]
    return render(request,'view-complain.html',{'complains':complains,'uid':uid})


def addmember(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
        try:
            if 'pic' in request.FILES: 
                Addmember.objects.create(
                
                    name = request.POST['name'],
                    email = request.POST['email'],
                    mobile = request.POST['mobile no'],
                    password = request.POST['password'],
                    flat= request.POST['flat'],
                    address = request.POST['address'],
                    adharcard = request.POST['adharcard'],
                    pic = request.FILES['pic'],
                )
            else:
                    Addmember.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    mobile = request.POST['mobile no'],
                    password = request.POST['password'],
                    flat= request.POST['flat'],
                    address = request.POST['address'],
                    adharcard = request.POST['adharcard'],
                ) 

            msg = 'Member Added'
        except:
            msg = 'Member is already register this email'
        return render(request,'addmember.html',{'msg':msg,'uid':uid})
    return render(request,'addmember.html',{'uid':uid})


def viewdetails(request,pk):
    uid = SecUser.objects.get(email=request.session['email'])
    complains = Complain.objects.get(id=pk)
    return render(request,'view-details.html',{'uid':uid,'complains':complains})


def delete_complain(request,pk):
    complains = Complain.objects.get(id=pk)
    complains.delete()
    return redirect('view-complain')


def solve(request,pk):
    complain = Complain.objects.get(id=pk)
    uid = SecUser.objects.get(email=request.session['email'])
    complain.status = True
    complain.solveby = uid
    complain.solvetime = datetime.now()
    complain.save()
    return redirect('view-complain')


def eventdetails(request,pk):
    uid = SecUser.objects.get(email=request.session['email'])
    events = Event.objects.get(id=pk)
    return render(request,'event-details.html',{'uid':uid,'event':events})
    
    
def gallery(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
        Gallery.objects.create( 
            gby = uid,
            gtype = request.POST['gtype'],
            gpic = request.FILES['gpic'],
        )
    
        msg = 'Image Added'
        return render(request,'gallery.html',{'msg':msg,'uid':uid})
    return render(request,'gallery.html',{'uid':uid}) 


def addnotice(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
            Notice.objects.create(
                ntype = request.POST['ntype'],
                ntitle = request.POST['ntitle'],
                ndes = request.POST['ndes'],
                nsendby = uid
            )
            msg = 'Notice Created'
            return render(request,'add-notice.html',{'uid':uid,'msg':msg})
    return render(request,'add-notice.html',{'uid':uid})

