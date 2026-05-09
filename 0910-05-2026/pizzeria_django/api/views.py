from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from menu_app.models import Book

class BookSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    price = serializers.FloatField()

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']




@api_view(['GET'])
def book_list_api(request):
    #books = [
    #    {'title': 'Python Crash Course', 'author': 'Eric Matthes', 'price': 49.99},
    #    {'title': 'Fluent Python', 'author': 'Luciano Ramalho', 'price': 59.99},
    #]
    books = Book.objects.all()

    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def book_detail_api(request, title):
    try:
        book = Book.objects.get(title=title)
    except Book.DoesNotExist:
        return Response(
            {"error": f"Ksiazka o tytule {title} nie znaleziona"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookModelSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PATCH':
        serializer = BookModelSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def book_list_api_post(request):
    serializer = BookModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#    curl -X DELETE http://127.0.0.1:8000/api/books/nowy/ \
#      -H "Content-Type: application/json"

