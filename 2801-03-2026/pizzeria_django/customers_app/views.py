import os
from django.shortcuts import render, redirect
from django.contrib import messages

from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.customer import Customer, VIPCustomer, CustomerManager
from rozwiazanie_weekend2.exceptions import InvalidDiscountError

CUSTOMERS_FILE = os.path.join(DATA_DIR, 'customers.json')


def _load_customers():
    manager = CustomerManager()
    manager.load_from_file(CUSTOMERS_FILE)
    return manager


def customer_list(request):
    manager = _load_customers()
    context = {
        'customers': list(manager),
        'total': len(manager),
    }
    return render(request, 'customers_app/customer_list.html', context)


def customer_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        customer_type = request.POST.get('type', 'regular')
        discount_str = request.POST.get('discount', '10').strip()

        errors = []
        if not name:
            errors.append("Imie klienta jest wymagane.")
        if not phone:
            errors.append("Numer telefonu jest wymagany.")

        if not errors:
            try:
                manager = _load_customers()

                if customer_type == 'vip':
                    discount = float(discount_str)
                    customer = VIPCustomer(name, phone, discount)
                else:
                    customer = Customer(name, phone)

                manager.add_customer(customer)
                manager.save_to_file(CUSTOMERS_FILE)
                messages.success(request, f"Dodano klienta: {name}")
                return redirect('customer_list')
            except (ValueError, TypeError) as e:
                errors.append(str(e))
            except InvalidDiscountError as e:
                errors.append(str(e))

        return render(request, 'customers_app/customer_form.html', {
            'errors': errors,
            'name': name,
            'phone': phone,
            'customer_type': customer_type,
            'discount': discount_str,
        })

    return render(request, 'customers_app/customer_form.html')
