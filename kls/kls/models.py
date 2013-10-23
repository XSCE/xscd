from django.db import models

class PNR(models.Model):
    last = models.CharField(max_length=200)
    first = models.CharField(max_length=200)
    role = models.CharField(max_length=5)
    xo = models.CharField(max_length=6)

class XO(models.Model):
    xo_id = models.CharField(max_length=13, primary_key=True)
    serial_number = models.CharField(max_length=11, unique=True)
    version = models.CharField(max_length=10,blank=True)
    backup = models.DateField(null=True)
    status = models.TextField(blank=True)

