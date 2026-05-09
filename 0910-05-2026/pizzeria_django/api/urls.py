from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list_api),
    path('books/post', views.book_list_api_post),
    path('books/<str:title>/', views.book_detail_api),
]


