from django.db import models

# Create your models here.
class Question(models.Model):
   text=models.CharField(max_length=200)

class Answer(models.Model):
   text=models.CharField(max_length=200)
   question_id=models.IntegerField()

class Algorithm(models.Model):
   name=models.CharField(max_length=50)

