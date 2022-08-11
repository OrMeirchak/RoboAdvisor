from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages

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
        if User.objects.filter(email=email).exists():
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
   return render(request,'createPortfolio.html')
 else:
   return redirect('register') 

def protfolio_list(request):
 if request.user.is_authenticated:
   return render(request,'myProtfolios.html')
 else:
   return redirect('register') 
    
