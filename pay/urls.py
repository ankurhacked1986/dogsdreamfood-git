from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.pay, name='pay'),
    #path('success' , views.success , name='success'),
    
]
