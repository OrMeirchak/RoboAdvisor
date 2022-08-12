from xmlrpc.client import boolean
import re

def _map(x:int, in_min:int, in_max:int, out_min:int, out_max:int)->int:
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def validate_email(email:str)->bool:
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,email):
      return True
   return False