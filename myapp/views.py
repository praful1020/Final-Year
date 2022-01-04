from django.shortcuts import render,redirect
from .models import *
from random import choices, randrange
from django.conf import settings
from django.core.mail import send_mail


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

    