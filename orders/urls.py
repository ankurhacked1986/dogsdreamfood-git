from django.urls import path,include
from . import views
from .views import OrderCreateView
urlpatterns = [
    path('',views.OrderCreateView.as_view(),name='order'),
    path('success',views.success, name = 'success')
]
