from asyncio.windows_events import NULL
import base64
from io import BytesIO
from multiprocessing import connection
from hashlib import new
from django.shortcuts import render,redirect
from django.db.models import Max,Min
from django.http import QueryDict
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Algorithm,Algotrade_index,Algotrade_type,Answer,Question,Portfolio, Train_model
from . import tools,algorithm_api
from django.http import QueryDict
from django.http import JsonResponse
from django.template.loader import render_to_string
import threading

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
            return redirect('create_portfolio')
     else:
        messages.info(request,'Password Not The Same')
        return redirect('register')
    else:
     if request.user.is_authenticated:
      return redirect('create_portfolio')
     else:
      return render(request,'register.html')

def login(request):
 if request.method == 'POST':
    username=request.POST['username']
    password=request.POST['password']
    user=auth.authenticate(username=username,password=password)
    if user is not None:
      auth.login(request,user)
      return redirect('create_portfolio')
    else:
      messages.info(request,'Credentials Invalid')
      return redirect('login')
      
 if request.method == 'GET':
    if request.user.is_authenticated:
      return redirect('create_portfolio')
    else:
      return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def create_portfolio(request):
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
     user_name=request.user.username
     portfolio_name=request.POST['name']
     if Portfolio.objects.filter(name=portfolio_name,user_id=request.user.id):
        messages.info(request,'Portfolio Name Already used')
        return redirect('create_portfolio')
     algorithm_id=request.POST['algorithm']
     score=0
     for question in Question.objects.all():
        id_values=Answer.objects.filter(question_id=question.id).aggregate(min=Min('id'),max=Max('id'))
        score+=tools._map(int(request.POST[str(question.id)]),int(id_values['min']),int(id_values['max']),1,10)
     score=tools._map(score,10,10*Question.objects.count(),10,100)
     if score < 30:
       debug(user_name,algorithm_id,portfolio_name,score,"Low risk")#debug
       portfolio=Portfolio.objects.create(name=portfolio_name,risk=0,algorithm_id=algorithm_id,user_id=request.user.id)
     elif score > 70:
       debug(user_name,algorithm_id,portfolio_name,score,"High risk")#debug
       portfolio=Portfolio.objects.create(name=portfolio_name,risk=2,algorithm_id=algorithm_id,user_id=request.user.id)
     else:
       debug(user_name,algorithm_id,portfolio_name,score,"Avarage risk")#debug
       portfolio=Portfolio.objects.create(name=portfolio_name,risk=1,algorithm_id=algorithm_id,user_id=request.user.id)
     portfolio.save()
     return redirect('portfolio'+'/'+str(portfolio.id))
 else:
   return redirect('register') 

def portfolio_list(request):
 if request.user.is_authenticated:
   if request.method == 'GET':
     portfolios=[]
     for portfolio in Portfolio.objects.all():
       portfolios.append({
          'name':portfolio.name,
          'algorithm':Algorithm.objects.get(pk=portfolio.algorithm_id).name,
          'risk':portfolio.risk,
          'creation_date':portfolio.creation_date,
          'id':portfolio.id
           })
     return render(request,'myportfolios.html',{'portfolios':portfolios})
 else:
   return redirect('register')

def portfolio(request,portfolio):
  if request.user.is_authenticated:
    if request.method == 'GET':
      try:
        portfolio=Portfolio.objects.get(pk=portfolio)
        if portfolio.user_id==request.user.id:
          return render(request,'portfolio.html',{
          'name':portfolio.name,
          'algorithm':Algorithm.objects.get(pk=portfolio.algorithm_id).name,
          'risk':portfolio.risk,
          'creation_date':portfolio.creation_date.strftime("%d-%m-%Y | %H:%M"),
          'portfolio_id':portfolio.id
           })
      except Portfolio.DoesNotExist:
        return redirect('/home')
    if request.method == 'DELETE':
      portfolio_id = QueryDict(request.body).get('portfolio_id')
      print("portfolio "+portfolio_id+ " deleted")#Debug
      portfolio=Portfolio.objects.get(pk=portfolio_id)
      if portfolio.user_id==request.user.id:
        portfolio.delete() 
      return render(request,'myPortfolios.html')
  return redirect('/home')

def articels(request,article_name):
  if request.method == 'GET':
    if article_name=='gini':
      return render(request,'articels/gini.html')

def train_model(request):
  if request.user.is_authenticated and request.user.username == 'admin':
    #algorithms=Algorithm.objects.all()
    if request.method == 'POST':
      algorithm_id=request.POST['algorithm_id']
      print("train model id : "+algorithm_id)#Debug
      train=Train_model.objects.create(algorithm_id=algorithm_id)
      t = threading.Thread(target=algorithm_api.train_model,args=[train.algorithm_id,train.id])
      t.setDaemon(True)
      t.start()
      #df=algorithm_api.train_model()
      #protofilo=Gini_protofilo.objects.create(df=df)
      #protofilo.save()
      #return render(request,'trainModel.html',{'algorithms':algorithms})
      print("Finish View Method")#Debu
      return redirect('train_model')
    if request.method == 'GET':
      algorithms=[]
      for algorithm in Algorithm.objects.all():
        if Train_model.objects.filter(algorithm_id=algorithm.id).exists():
          latest_train= Train_model.objects.filter(algorithm_id=algorithm.id).latest('creation_date')
          if latest_train.finish==True:
            last_update=latest_train.creation_date
            training_now=0
          elif Train_model.objects.filter(algorithm_id=algorithm.id,finish=False).exists():
             last_update=Train_model.objects.filter(algorithm_id=algorithm.id,finish=False).latest('creation_date').creation_date
             training_now=1
          else:
            last_update="The model is not trained"
            training_now=1
        else:
          last_update="The model is not trained"
          training_now=0
        algorithms.append({
          'id':algorithm.id,
          'name':algorithm.name,
          'last_update':last_update,
          'trainig_now':training_now
        })

      return render(request,'trainModel.html',{'algorithms':algorithms})
  else:
    return redirect('home')

def develop(request):
  json=Gini_protofilo.objects.get(pk=3).df
  df=tools.json_to_df(json)
  plt=tools.df_to_plt_gini(df)
  return render(request,'develop.html')

def algotrade(request):
  if request.user.is_authenticated:
    if request.method == 'GET':
      return render(request,'algotrade.html',{'algotrade_indices':Algotrade_index.objects.all(),'algotrade_types':Algotrade_type.objects.all()})
    if request.method == 'POST':
      response=algorithm_api.algotrade(Algotrade_type.objects.get(pk=request.POST['type']).name,Algotrade_index.objects.get(pk=int(request.POST['index'])).symbol)
      cur_price=response['cur_price']
      exp_price=response['exp_price']
      return render(request,'algotrade.html',{'algotrade_indices':Algotrade_index.objects.all(),'algotrade_types':Algotrade_type.objects.all(),'cur_price':cur_price,'exp_price':exp_price,'type':Algotrade_type.objects.get(pk=request.POST['type']).name,'symbol':Algotrade_index.objects.get(pk=int(request.POST['index'])).symbol})
  else:
    return redirect('register')

def debug(user_name,algorithm,name,score,risk):
  print("__________debug__________")
  print("User Name : "+user_name)
  print("Portfolio Name : "+name)
  print("Algorithm ID : "+algorithm)
  print("Score : "+str(score))
  print(risk)
  print("__________debug__________")

  





    
