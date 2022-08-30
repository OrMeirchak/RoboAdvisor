from django.db import models
from jsonfield import JSONField
from datetime import date, datetime

# Create your models here.
class Question(models.Model):
   text=models.CharField(max_length=200)

class Answer(models.Model):
   text=models.CharField(max_length=200)
   question_id=models.IntegerField()

class Algorithm(models.Model):
   name=models.CharField(max_length=50)

class Algotrade_type(models.Model):
   name=models.CharField(max_length=50)

class Algotrade_index(models.Model):
   symbol=models.CharField(max_length=50)

class Portfolio(models.Model):
   name=models.CharField(max_length=50)
   risk=models.IntegerField()
   algorithm_id=models.IntegerField()
   user_id=models.IntegerField()
   creation_date=models.DateTimeField(default=datetime.now,blank=True)



   
   

