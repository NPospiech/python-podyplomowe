import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

from rozwiazanie_weekend2 import DATA_DIR
#from rozwiazanie_weekend2.pizza import Pizza, Menu
from .models import Pizza
from rozwiazanie_weekend2.exceptions import PizzaNotFoundError, DuplicatePizzaError, InvalidPriceError
from django.core.exceptions import ValidationError
from django.db import IntegrityError

def pizza_list(request):
    pizzas = Pizza.objects.all()
    return render(request, 'menu_app/pizza_list.html', {'pizzas': pizzas})


def pizza_detail(request, name):
    menu = _load_menu()
    try:
        pizza = menu.find_pizza(name)
    except PizzaNotFoundError:
        raise Http404(f"Pizza '{name}' nie została znaleziona")
    return render(request, 'menu_app/pizza_detail.html', {'pizza': pizza})

def pizza_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price_str = request.POST.get('price', '').strip()

        errors = []
        if not name:
            errors.append("Nazwa pizzy jest wymagana.")
        if not price_str:
            errors.append("Cena jest wymagana.")

        if not errors:
            try:
                price = float(price_str)
                Pizza.objects.create(name=name, price=price)
                messages.success(request, f"Dodano pizzę: {name}")
                return redirect('pizza_list')
            except (ValueError, TypeError):
                errors.append("Nieprawidlowa cena.")
            except ValidationError as e:
                errors.extend(e.messages)
            except IntegrityError:
                errors.append(f"Pizza '{name}' juz istnieje!")

        return render(request, 'menu_app/pizza_form.html', {
            'errors': errors,
            'name': name,
            'price': price_str,
        })

    return render(request, 'menu_app/pizza_form.html')

