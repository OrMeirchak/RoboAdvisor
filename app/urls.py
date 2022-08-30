from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('home',views.home,name="home"),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('create_portfolio',views.create_portfolio,name='create_portfolio'),
    path('portfolio_list',views.portfolio_list,name='portfolio_list'),
    path('portfolio/<str:portfolio>/',views.portfolio,name='portfolio'),
    path('logout',views.logout,name='logout'),
    path('train_model',views.train_model,name='train_model'),
    path('algotrade',views.algotrade,name='algotrade'),
    path('develop',views.develop,name='develop'),
    path('articels/<str:article_name>/', views.articels, name='articels')
]