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