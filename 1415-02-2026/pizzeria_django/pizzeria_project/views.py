from django.http import HttpResponse
from django.shortcuts import render

def witaj(request):
    return HttpResponse("<h1>Witaj w pizzerii!</h1>")

def book_list(request):
    books = [
        {'title': 'Python Crash Course', 'author': 'Eric Matthes'},
        {'title': 'Fluent Python', 'author': 'Luciano Ramalho'},
    ]
    return render(request, 'books/book_list.html', {'books': books})



