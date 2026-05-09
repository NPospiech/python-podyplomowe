from django.contrib import admin
from .models import Book, Pizza

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price']
    search_fields = ['title', 'author']

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']


