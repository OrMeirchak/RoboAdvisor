from asyncio.windows_events import NULL
from hashlib import new
from django.shortcuts import render,redirect
from django.db.models import Max,Min
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Algorithm, Answer,Question
from . import tools

def index(request):  
    return render(request,'index.html')

def home(request):
    return index(request)

def register(request):
    if request.method=="POST":
     username=request.POST['username']
     email=request.POST['email']
     password1=request.POST['password1']
     password2=request.POST['password2']

     if password1==password2:
        if len(password1)<5:
          messages.info(request,'Password Too Short - The length of the password is at least 5 characters')
          return redirect('register')
        elif tools.validate_email(email)==False:
           messages.info(request,'Invalid Email')
           return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email Already Used')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'Username Already used')
            return redirect('register')
        else:
            user=User.objects.create_user(username=username,email=email,password=password1)
            user.save()
            auth.login(request,user)
            return redirect('create_protfolio')
     else:
        messages.info(request,'Password Not The Same')
        return redirect('register')
    else:
     if request.user.is_authenticated:
      return redirect('create_protfolio')
     else:
      return render(request,'register.html')

def login(request):
 if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']

    user=auth.authenticate(username=username,password=password)

    if user is not None:
      auth.login(request,user)
      return redirect('create_protfolio')
    else:
      messages.info(request,'Credentials Invalid')
      return redirect('login')
      
 if request.method == 'GET':
    if request.user.is_authenticated:
      return redirect('create_protfolio')
    else:
      return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


def create_protfolio(request):
 if request.user.is_authenticated:

   if request.method == 'GET':
     questions=[]
     for question in Question.objects.all():
        questions.append({
         "text":question.text,
         "answers":list(Answer.objects.filter(question_id=question.id)),
        })
     algorithms=Algorithm.objects.all()
     return render(request,'createPortfolio.html',{'questions':questions,'algorithms':algorithms})

   if request.method == 'POST':
     protofilo_name=request.POST['name']
     if(protofilo_name=="yossi"):
        messages.info(request,'Protofilo Name Already used')
        return redirect('create_protfolio')
     algorithm_id=request.POST['algorithm']
     score=0
     for question in Question.objects.all():
        id_values=Answer.objects.filter(question_id=question.id).aggregate(min=Min('id'),max=Max('id'))
        score+=tools._map(int(request.POST[str(question.id)]),int(id_values['min']),int(id_values['max']),1,10)
     if score < 10*Question.objects.count()/3:
       debug(algorithm_id,protofilo_name,"Low risk")
     elif score > 10*Question.objects.count()/3*2:
       debug(algorithm_id,protofilo_name,"High risk")
     else:
       debug(algorithm_id,protofilo_name,"Avarage risk")
     return redirect('protfolio_list')
 else:
   return redirect('register') 


def debug(algorithm,name,risk):
  print("__________debug__________")
  print("Protofile Name : "+name)
  print("Algorithm ID : "+algorithm)
  print(risk)
  print("__________debug__________")


def protfolio_list(request):
 if request.user.is_authenticated:
   if request.method == 'GET':
     return render(request,'myProtfolios.html')
   if request.method == 'DELETE':
     print("delete "+request.DELETE['id'])
 else:
   return redirect('register')

def articels(request):
  if request.method == 'GET':
    if request.GET['article_name']=='gini':
      return render(request,'articels/gini.html')




    
