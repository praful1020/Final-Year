from calendar import month
from django.db import models

class SecUser(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    pic = models.FileField(upload_to='profile',default='avatar.jpg')
    address = models.CharField(max_length=60, null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name


class Event(models.Model):

    uid = models.ForeignKey(SecUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    des = models.TextField()
    event_at = models.DateField(null=True, blank=True)
    edate = models.DateTimeField(auto_now_add=True)
    pic = models.FileField(upload_to='Event',null=True,blank=True)

    def __str__(self):
        return self.title  

class Addmember(models.Model):
    
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=20) 
    flat = models.CharField(max_length=10)
    address = models.CharField(max_length=60)
    adharcard = models.CharField(max_length=12)
    pic = models.FileField(upload_to='Event',null=True,blank=True)


    def __str__(self):
        return self.name


class Complain(models.Model):
    ctitle = models.CharField(max_length=50)
    ctypes = models.CharField(max_length=50)
    cdes = models.TextField()
    ctime = models.DateTimeField(auto_now_add=True)
    cby = models.ForeignKey(Addmember,on_delete=models.CASCADE)
    solvetime = models.DateTimeField(null=True,blank=True)
    solveby = models.ForeignKey(SecUser,on_delete=models.CASCADE,null=True,blank=True)
    cpic = models.FileField(upload_to='Complain',null=True,blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.ctitle


class Gallery(models.Model):
    gby = models.ForeignKey(SecUser,on_delete=models.CASCADE)
    gtype = models.CharField(max_length=50)
    gpic = models.FileField(upload_to='gallery')

    def __str__(self):
        return self.gtype


class Notice(models.Model):
    ntype = models.CharField(max_length=50)
    ntitle = models.CharField(max_length=50)
    ndes = models.TextField()
    nsendby = models.ForeignKey(SecUser,on_delete=models.CASCADE,null=True,blank=True)
    ntime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ntype

class Pay(models.Model):
   
    user = models.ForeignKey(Addmember,on_delete=models.CASCADE,null=True,blank=True)
    pamount = models.CharField(max_length=50)
    ptime = models.DateTimeField(auto_now_add=True)
    pdate = models.DateField()
    pverifiy = models.BooleanField(default=False)
    payid = models.CharField(max_length=50,null=True,blank=True)

    def __user__(self):
        return self.user