from email.policy import default
from django.db import models

# Create your models here.
class OurInterFriends(models.Model):
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='images/ourIntFriends',null=True,blank=True)
    itsActive=models.BooleanField(default=True)
    desc=models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return str(self.name) +' -- '+str(self.itsActive)


class AboutQaamuusInfo(models.Model):
    heroImage=models.ImageField(upload_to='images/aboutQaamuus',null=True,blank=True)
    heroTitle =models.CharField(max_length=255)
    authHeroImage=models.ImageField(upload_to='images/aboutQaamuus',null=True,blank=True)
    heroAuthTitle =models.CharField(max_length=255)
    heroDesc =models.CharField(max_length=255)
    heroAuthDesc =models.CharField(max_length=255)
    aboutQaamuusVideo=models.FileField(upload_to='video/videoUploaded')
    aboutQaamuusImage=models.CharField(max_length=255)
    # singUpImage=models.ImageField(default='')
    