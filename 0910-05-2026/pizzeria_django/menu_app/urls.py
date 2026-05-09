from django.urls import path
from . import views

urlpatterns = [
    path('', views.pizza_list, name='pizza_list'),
    path('dodaj/', views.pizza_add, name='pizza_add'),
    path('<str:name>/', views.pizza_detail, name='pizza_detail'),
]
