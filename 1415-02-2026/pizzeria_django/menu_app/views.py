import os
from django.shortcuts import render
from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.pizza import Menu
from django.http import Http404
from rozwiazanie_weekend2.exceptions import PizzaNotFoundError

MENU_FILE = os.path.join(DATA_DIR, 'menu.json')

def pizza_list(request):
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    return render(request, 'menu_app/pizza_list.html', {'pizzas': list(menu)})

#KONTROLERKA: Czy w URL jest nazwa pizzy? Jeśli tak, to wyświetl szczegóły tej pizzy.
#MODEL VIEW CONTROLLER (MVC) - KONTROLERKA: Odpowiada za logikę aplikacji, przetwarzanie danych i komunikację między modelem a widokiem. Kontrolerka odbiera żądania od użytkownika, przetwarza je, korzystając z modelu, i zwraca odpowiednie dane do widoku, który następnie prezentuje je użytkownikowi.
def pizza_detail(request, name):
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    try:
        pizza = menu.find_pizza(name)
    except PizzaNotFoundError:
        raise Http404(f"Pizza '{name}' nie znaleziona")
    return render(request, 'menu_app/pizza_detail.html', {'pizza': pizza})
    
# Create your views here.
