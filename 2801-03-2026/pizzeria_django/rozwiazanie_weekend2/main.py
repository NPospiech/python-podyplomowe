# Główny plik aplikacji pizzerii - rozwiązanie Weekend 1+2
# Pełna wersja z obsługą wyjątków i I/O
#
# Uruchamianie:
#   python3 main.py                          (z wnętrza rozwiazanie_weekend2/)
#   python3 -m rozwiazanie_weekend2.main     (z katalogu nadrzędnego)

import os
import sys

# Dodaj katalog nadrzędny do sys.path, żeby importy działały
# niezależnie od tego skąd uruchamiamy skrypt
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rozwiazanie_weekend2 import DATA_DIR
from rozwiazanie_weekend2.pizza import Pizza, Menu
from rozwiazanie_weekend2.customer import Customer, VIPCustomer, CustomerManager
from rozwiazanie_weekend2.order import Order, OrderManager
from rozwiazanie_weekend2.exceptions import (
    PizzeriaError,
    InvalidPriceError,
    PizzaNotFoundError,
    CustomerNotFoundError,
    EmptyOrderError
)


def main():
    """Główna funkcja aplikacji."""
    print("=" * 60)
    print("APLIKACJA PIZZERII - Weekend 2 (Wyjątki + I/O)")
    print("=" * 60)

    Customer.reset_id_counter()
    Order.reset_id_counter()

    menu_file = os.path.join(DATA_DIR, "menu.json")
    customers_file = os.path.join(DATA_DIR, "customers.json")

    # === WCZYTYWANIE DANYCH ===
    print("\n--- Wczytywanie danych ---")

    menu = Menu()
    menu.load_from_file(menu_file)

    customer_manager = CustomerManager()
    customer_manager.load_from_file(customers_file)

    if len(menu) == 0:
        print("\nTworzę przykładowe menu...")
        menu.add_pizza(Pizza("Margherita", 25.0))
        menu.add_pizza(Pizza("Pepperoni", 30.0))
        menu.add_pizza(Pizza("Hawajska", 32.0))
        menu.add_pizza(Pizza("Quattro Formaggi", 35.0))

    if len(customer_manager) == 0:
        print("\nTworzę przykładowych klientów...")
        customer_manager.add_customer(Customer("Jan Kowalski", "123-456-789"))
        customer_manager.add_customer(VIPCustomer("Anna Nowak", "987-654-321", 15))
        customer_manager.add_customer(VIPCustomer("Piotr Wiśniewski", "555-123-456", 20))

    # === WYŚWIETLANIE DANYCH ===
    menu.list_pizzas()
    customer_manager.list_customers()

    # === TWORZENIE ZAMÓWIEŃ ===
    print("\n--- Tworzenie zamówień ---")
    order_manager = OrderManager()

    try:
        customer1 = customer_manager.find_customer(1)
        order1 = order_manager.create_order(customer1)
        order1.add_item(menu.find_pizza("Margherita"), 2)
        order1.add_item(menu.find_pizza("Pepperoni"), 1)
    except (CustomerNotFoundError, PizzaNotFoundError) as e:
        print(f"Błąd tworzenia zamówienia: {e}")

    try:
        vip = customer_manager.find_customer(2)
        order2 = order_manager.create_order(vip)
        order2.add_item(menu.find_pizza("Quattro Formaggi"), 2)
        if hasattr(vip, 'add_loyalty_points'):
            vip.add_loyalty_points(10)
    except (CustomerNotFoundError, PizzaNotFoundError) as e:
        print(f"Błąd tworzenia zamówienia: {e}")

    # === WYŚWIETLANIE ZAMÓWIEŃ ===
    print("\n--- Szczegóły zamówień ---")
    for order in order_manager:
        print()
        print(order)

    order_manager.list_orders()
    print(f"\nŁączny przychód: {order_manager.get_total_revenue():.2f} zł")

    # === DEMONSTRACJA OBSŁUGI BŁĘDÓW ===
    print("\n" + "=" * 60)
    print("DEMONSTRACJA OBSŁUGI WYJĄTKÓW")
    print("=" * 60)

    print("\n1. Próba utworzenia pizzy z ujemną ceną:")
    try:
        Pizza("Test", -10)
    except InvalidPriceError as e:
        print(f"   Przechwycono: {e}")

    print("\n2. Próba znalezienia nieistniejącej pizzy:")
    try:
        menu.find_pizza("Carbonara")
    except PizzaNotFoundError as e:
        print(f"   Przechwycono: {e}")

    print("\n3. Próba znalezienia nieistniejącego klienta:")
    try:
        customer_manager.find_customer(999)
    except CustomerNotFoundError as e:
        print(f"   Przechwycono: {e}")

    print("\n4. Próba przetworzenia pustego zamówienia:")
    try:
        empty_order = order_manager.create_order(customer1)
        empty_order.process()
    except EmptyOrderError as e:
        print(f"   Przechwycono: {e}")

    # === ZAPISYWANIE DANYCH ===
    print("\n" + "=" * 60)
    print("ZAPISYWANIE DANYCH")
    print("=" * 60)

    menu.save_to_file(menu_file)
    customer_manager.save_to_file(customers_file)

    print("\nDane zostały zapisane.")


if __name__ == "__main__":
    main()
