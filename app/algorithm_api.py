import json
import requests
import pandas as pd
import sys
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import time

from app.models import Train_model


if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

BASR_URL="http://localhost:5000/api/v1"

def algotrade(machine_learning_type:str,stock:str):
  parameters = {
  "MACHINE_LEARNING_TYPE": machine_learning_type, 
  "STOCK": stock} 
  response = requests.post(BASR_URL+'/algotrade-options', params=parameters)
  return response.json()

def train_model(algorithm_id,train_model_id):
  print("Start train "+algorithm_id)
  time.sleep(10)
  print("Finish train "+algorithm_id)
  train_model=Train_model.objects.get(pk=train_model_id)
  train_model.finish=True
  train_model.save()

def train_modelx():
  parameters = {
  "V": 1.5} 
  response = requests.post(BASR_URL+'/robo-advisor/gini', params=parameters)
  return response.json()
  #return pd.json_normalize(response.json())
  







