from random import randrange
from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from myapp.models import Addmember, Complain, Gallery, Pay, SecUser
from myapp.models import Event, Notice
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import *


# Create your views here.
def ulogin(request):  
    if request.method == 'POST':
        #   try:
            uid = Addmember.objects.get(email=request.POST['email'])
            if request.POST['password'] == uid.password:
                request.session['uemail'] = request.POST['email']
                return redirect("uindex")
            else:
                return render(request,'ulogin.html',{'msg':'Wrong Password'})
        #   except:
        #       return render(request,'ulogin.html',{'msg':'Wrong Email'})
    return render(request,'ulogin.html')    


def uindex(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    tmember = Addmember.objects.all().count()
    tevent = Event.objects.all().count()
    tcomplain = Complain.objects.all().count()
    tnotice = Notice.objects.all().count()
    notices = Notice.objects.all()[::-1][:4]
    complains = Complain.objects.all()[::-1][:4]
    return render(request,'uindex.html',{'uid':uid,'complains':complains,'notices':notices,'tmember':tmember,'tevent':tevent,'tcomplain':tcomplain,'tnotice':tnotice})


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
    uid = Addmember.objects.get(email=request.session['uemail'])
    events = Event.objects.all()
    return render(request,'View-Events.html',{'uid':uid,'events':events})


def utables(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    return render(request,'utables.html',{'uid':uid})


def add_complain(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    if request.method == 'POST':
        print(request.FILES['cpic'])
        if 'cpic' in request.FILES: 
            Complain.objects.create(
                cby = uid,
                ctitle = request.POST['ctitle'],
                cdes = request.POST['cdes'],
                cpic = request.FILES['cpic'],
                ctypes = request.POST['ctypes'],

            )
        else:
            Complain.objects.create(
                cby = uid,
                ctitle = request.POST['ctitle'],
                cdes = request.POST['cdes'],
                ctypes = request.POST['ctypes'],

                )
        msg = 'Complain Send'
        return render(request,'add_complain.html',{'uid':uid,'msg':msg})
    return render(request,'add_complain.html',{'uid':uid})


def uview_complains(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    complains = Complain.objects.filter(cby=uid)
    return render(request,'uview-complains.html',{'complains':complains,'uid':uid})

def uviewdetails(request,pk):
    uid = Addmember.objects.get(email=request.session['uemail'])
    complains = Complain.objects.get(id=pk)
    return render(request,'uview-details.html',{'uid':uid,'complains':complains})


def image(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    gym = Gallery.objects.filter(gtype='gym')
    garden = Gallery.objects.filter(gtype='garden')
    swimmingpool = Gallery.objects.filter(gtype='swimmingpool')
    indoorstadium = Gallery.objects.filter(gtype='indoorstadium')
    childrenground = Gallery.objects.filter(gtype='childrenground')

    
    return render(request,'image.html',{'uid':uid,'gym':gym,'garden':garden,'swimmingpool':swimmingpool,'indoorstadium':indoorstadium,'childrenground':childrenground})


def notice(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    notices = Notice.objects.all()
    return render(request,'notice.html',{'uid':uid,'notices':notices})

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
# def pay(request):
#     uid = Addmember.objects.get(email=request.session['uemail'])
    
#     return render(request,'pay.html',{'uid':uid})
 
def pay(request):
    uid = Addmember.objects.get(email=request.session['uemail'])
    if request.method == 'POST':
      
        pay_d = Pay.objects.create(
           user = uid,
           pamount = request.POST['pamount'],
           pdate = request.POST['pdate']+'-01',
           
        )
        currency = 'INR'
        amount = 150000  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency,payment_capture='0'))


    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = f'paymenthandler/{pay_d.id}'
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['pay_d'] = pay_d
        context['uid']= uid

        return render(request, 'paydetail.html', context=context)
    return render(request, 'pay.html',{'uid':uid})
        
 
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request,pk):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            # if result is None:
            amount = 150000  # Rs. 200
            try:

                # capture the payemt
                razorpay_client.payment.capture(payment_id, amount)
                payd = Pay.objects.get(id=pk)
                payd.payid= payment_id
                payd.pverifiy = True
                payd.save()
                # render success page on successful caputre of payment
                return render(request, 'successpay.html',{'pay':payd})
            except:

                # if there is an error while capturing payment.
                return render(request, 'failpay.html')
            # else:
 
            #     # if signature verification fails.
            #     return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


