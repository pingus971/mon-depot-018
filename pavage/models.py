# Create your models here.

from django.db import models

#class ImageBrute(models.Model):
#    photo = models.ImageField(upload_to='images')

class ChargerImage(models.Model):
    photo = models.ImageField(upload_to='images_de_base')
