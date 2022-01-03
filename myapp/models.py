from django.db import models

class SecUser(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    pic = models.FileField(upload_to='profile',default='avatar.jpg')
    
    

    def __str__(self):
        return self.name
      