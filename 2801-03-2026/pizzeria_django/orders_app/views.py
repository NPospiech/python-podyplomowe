import os
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.pizza import Menu
from rozwiazanie_weekend2.customer import CustomerManager
from rozwiazanie_weekend2.exceptions import (
    PizzaNotFoundError,
    CustomerNotFoundError,
)

MENU_FILE = os.path.join(DATA_DIR, 'menu.json')
CUSTOMERS_FILE = os.path.join(DATA_DIR, 'customers.json')
ORDERS_FILE = os.path.join(DATA_DIR, 'orders.json')


def _load_menu():
    menu = Menu()
    menu.load_from_file(MENU_FILE)
    return menu


def _load_customers():
    manager = CustomerManager()
    manager.load_from_file(CUSTOMERS_FILE)
    return manager


def _load_orders():
    """Wczytuje zamowienia z pliku JSON."""
    try:
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return data


def _save_orders(orders_data):
    """Zapisuje zamowienia do pliku JSON."""
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders_data, f, indent=2, ensure_ascii=False)


def _get_next_order_id(orders_data):
    if not orders_data:
        return 1
    return max(o['id'] for o in orders_data) + 1


def order_list(request):
    orders_data = _load_orders()
    customer_mgr = _load_customers()

    orders_display = []
    for order_data in orders_data:
        customer_name = f"Klient #{order_data['customer_id']}"
        try:
            customer = customer_mgr.find_customer(order_data['customer_id'])
            customer_name = customer.name
        except CustomerNotFoundError:
            pass

        total = sum(item['pizza_price'] * item['quantity'] for item in order_data['items'])
        if order_data.get('discount_percent'):
            total = total * (1 - order_data['discount_percent'] / 100)

        orders_display.append({
            'id': order_data['id'],
            'customer_name': customer_name,
            'items_count': len(order_data['items']),
            'total': round(total, 2),
            'is_vip': order_data.get('discount_percent') is not None,
            'discount_percent': order_data.get('discount_percent'),
        })

    return render(request, 'orders_app/order_list.html', {
        'orders': orders_display,
        'total_revenue': sum(o['total'] for o in orders_display),
    })


def order_detail(request, order_id):
    orders_data = _load_orders()
    customer_mgr = _load_customers()

    order_data = None
    for o in orders_data:
        if o['id'] == order_id:
            order_data = o
            break

    if order_data is None:
        raise Http404(f"Zamowienie #{order_id} nie zostalo znalezione")

    customer_name = f"Klient #{order_data['customer_id']}"
    try:
        customer = customer_mgr.find_customer(order_data['customer_id'])
        customer_name = customer.name
    except CustomerNotFoundError:
        pass

    items = []
    subtotal = 0
    for item in order_data['items']:
        item_total = item['pizza_price'] * item['quantity']
        subtotal += item_total
        items.append({
            'pizza_name': item['pizza_name'],
            'pizza_price': item['pizza_price'],
            'quantity': item['quantity'],
            'total': item_total,
        })

    discount_percent = order_data.get('discount_percent')
    discount_amount = 0
    total = subtotal
    if discount_percent:
        discount_amount = round(subtotal * discount_percent / 100, 2)
        total = round(subtotal - discount_amount, 2)

    return render(request, 'orders_app/order_detail.html', {
        'order_id': order_data['id'],
        'customer_name': customer_name,
        'items': items,
        'subtotal': subtotal,
        'discount_percent': discount_percent,
        'discount_amount': discount_amount,
        'total': total,
    })


def order_create(request):
    menu = _load_menu()
    customer_mgr = _load_customers()

    if request.method == 'POST':
        customer_id_str = request.POST.get('customer_id', '')
        pizza_names = request.POST.getlist('pizza_name')
        quantities = request.POST.getlist('quantity')

        errors = []
        if not customer_id_str:
            errors.append("Wybierz klienta.")

        order_items = []
        for pizza_name, qty_str in zip(pizza_names, quantities):
            if pizza_name and qty_str:
                try:
                    qty = int(qty_str)
                    if qty <= 0:
                        errors.append(f"Ilosc musi byc > 0 (pizza: {pizza_name})")
                        continue
                    pizza = menu.find_pizza(pizza_name)
                    order_items.append({
                        'pizza_name': pizza.name,
                        'pizza_price': pizza.price,
                        'quantity': qty,
                    })
                except PizzaNotFoundError:
                    errors.append(f"Pizza '{pizza_name}' nie istnieje.")
                except ValueError:
                    errors.append(f"Nieprawidlowa ilosc: {qty_str}")

        if not order_items:
            errors.append("Zamowienie musi zawierac przynajmniej jedna pozycje.")

        if not errors:
            try:
                customer_id = int(customer_id_str)
                customer = customer_mgr.find_customer(customer_id)

                discount_percent = None
                if hasattr(customer, 'discount_percent'):
                    discount_percent = customer.discount_percent

                orders_data = _load_orders()
                new_order = {
                    'id': _get_next_order_id(orders_data),
                    'customer_id': customer.id,
                    'items': order_items,
                    'discount_percent': discount_percent,
                }
                orders_data.append(new_order)
                _save_orders(orders_data)

                messages.success(request, f"Utworzono zamowienie #{new_order['id']} dla {customer.name}")
                return redirect('order_detail', order_id=new_order['id'])
            except CustomerNotFoundError:
                errors.append("Wybrany klient nie istnieje.")
            except ValueError:
                errors.append("Nieprawidlowe ID klienta.")

        return render(request, 'orders_app/order_form.html', {
            'errors': errors,
            'pizzas': list(menu),
            'customers': list(customer_mgr),
        })

    return render(request, 'orders_app/order_form.html', {
        'pizzas': list(menu),
        'customers': list(customer_mgr),
    })
