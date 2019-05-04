
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class User(models.Model):
    '''User form'''

    gender = (
        ('male', 'M'),
        ('female', 'F'),
    )
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='F')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = 'User'
        verbose_name_plural = 'User'

class Acquisition(models.Model):
    "Acquisition Form"
    id = models.IntegerField(primary_key=True)
    acq_date = models.CharField(max_length=50)
    experimenter = models.CharField(max_length=250)
    img_method = models.CharField(max_length=250)
    microscope = models.CharField(max_length=250)
    camera = models.CharField(max_length=250)
    scope_website = models.CharField(max_length=2083)
    magnification = models.CharField(max_length=250)
    num_ap = models.CharField(max_length=250)
    rfp_time = models.CharField(max_length=250)
    rfp_power = models.CharField(max_length=250)
    gfp_time = models.CharField(max_length=250)
    gfp_power = models.CharField(max_length=250)
    worm_stage = models.CharField(max_length=250)
    sex = models.CharField(max_length=250)
    strain_genotype = models.CharField(max_length=50)


class Image(models.Model):
    "Image Form"
    acquisition = models.ForeignKey(Acquisition, on_delete=models.CASCADE)
    green_id = models.IntegerField()
    red_id = models.IntegerField()
    merged_id = models.IntegerField(primary_key=True)
    worm_stage = models.CharField(max_length=250)
    orientation = models.CharField(max_length=250)
    img_date = models.CharField(max_length=50)
    sex = models.CharField(max_length=250)


class ImageOptional(models.Model):
    "Image optional form"
    id_image = models.ForeignKey(Image, on_delete=models.CASCADE)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=2048)

    class Meta:
        unique_together = ("id_image", "key")

class AcqOptional(models.Model):
    id_acq = models.ForeignKey(Acquisition, on_delete=models.CASCADE)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=2048)

    class Meta:
        unique_together = ("id_acq", "key")

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    img_date = models.CharField(max_length=250)
    sex = models.CharField(max_length=250)
    acquisition = models.ForeignKey(Acquisition, on_delete=models.CASCADE)
    worm_stage = models.CharField(max_length=250)
    name = models.CharField(max_length=20)




