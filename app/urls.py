from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('home',views.home,name="home"),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('create_protfolio',views.create_protfolio,name='create_protfolio'),
    path('protfolio_list',views.protfolio_list,name='protfolio_list'),
    path('logout',views.logout,name='logout'),
]