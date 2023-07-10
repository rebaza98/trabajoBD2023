#from django.db import models
from djongo import models

# Create your models here.


class Raw_Tweet(models.Model):
    _id = models.ObjectIdField(auto_created=True, unique=True, primary_key=True)
    id_tweet = models.IntegerField()
    tweetText = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
class Analisis(models.Model):
    _id = models.ObjectIdField(auto_created=True, unique=True, primary_key=True)
    idioma = models.CharField(max_length=2)
    rating = models.SmallIntegerField(default=0)
    tipo_opciones = (('E',"Entrada"), ('T', "Tweet"))
    tipo = models.CharField(max_length = 1, blank = False, null=False,choices=tipo_opciones, default = 'E')
    texto = models.TextField()
    label = models.CharField(max_length=30)
    score = models.DecimalField(max_digits=18, decimal_places=15, blank = True, null = True)
    label2 = models.CharField(max_length=30)
    score2 = models.DecimalField(max_digits=18, decimal_places=15, blank = True, null = True)
    label3 = models.CharField(max_length=30)
    score3 = models.DecimalField(max_digits=18, decimal_places=15, blank = True, null = True)
    raw_tweet = models.ForeignKey(Raw_Tweet, blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
