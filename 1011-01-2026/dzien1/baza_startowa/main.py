# Główny plik aplikacji pizzerii OOP
# Baza startowa dla Weekendu 2
#
# Ten kod pochodzi z rozwiązania Weekendu 1 (programowanie obiektowe).
# W tym weekendzie rozbudujemy go o:
# - Obsługę wyjątków (własne klasy wyjątków)
# - Operacje I/O (zapis/odczyt do plików JSON)
# - Testy jednostkowe z pytest

from pizza import Pizza, Menu
from customer import Customer, VIPCustomer, CustomerManager
from order import Order, OrderManager
from exceptions import PizzeriaError


def main():
    print("=" * 50)
    print("APLIKACJA PIZZERII - Weekend 2")
    print("=" * 50)

    # === MENU ===
    print("\n--- Tworzenie menu ---")
    menu = Menu()

    pizza1 = Pizza("Margherita", 25.0)
    pizza2 = Pizza("Pepperoni", 30.0)
    pizza3 = Pizza("Hawajska", 32.0)

    menu.add_pizza(pizza1)
    menu.add_pizza(pizza2)
    menu.add_pizza(pizza3)

    print(f"\nMenu zawiera {len(menu)} pizz:")
    menu.list_pizzas()

    # === KLIENCI ===
    print("\n--- Dodawanie klientów ---")
    customer_manager = CustomerManager()

    customer1 = Customer("Jan Kowalski", "123-456-789")
    vip_customer = VIPCustomer("Anna Nowak", "987-654-321", 15)

    customer_manager.add_customer(customer1)
    customer_manager.add_customer(vip_customer)

    print(f"\nLista klientów ({len(customer_manager)}):")
    customer_manager.list_customers()

    # === ZAMÓWIENIA ===
    print("\n--- Tworzenie zamówień ---")
    order_manager = OrderManager()

    # Zamówienie dla zwykłego klienta
    order1 = order_manager.create_order(customer1)
    order1.add_item(pizza1, 2)  # 2x Margherita
    order1.add_item(pizza2, 1)  # 1x Pepperoni

    # Zamówienie dla VIP klienta (ze zniżką!)
    order2 = order_manager.create_order(vip_customer)
    order2.add_item(pizza3, 1)  # 1x Hawajska
    vip_customer.add_loyalty_points(10)

    print(f"\n--- Szczegóły zamówienia 1 ---")
    print(order1)

    print(f"\n--- Szczegóły zamówienia 2 (VIP ze zniżką {vip_customer.discount_percent}%) ---")
    print(order2)

    print(f"\n--- Podsumowanie ---")
    order_manager.list_orders()

    # === DEMONSTRACJA PROBLEMÓW (do naprawienia w tym weekendzie!) ===
    print("\n" + "=" * 50)
    print("PROBLEMY DO ROZWIĄZANIA W TYM WEEKENDZIE:")
    print("=" * 50)

    try:
        pizza_invalid = Pizza("Pizza z ujemną ceną", -10)
    except PizzeriaError as e:
        print('Wyjątek przy tworzeniu pizzy:', e)

    try:
        pizza1.update_price(-10)
    except PizzeriaError as e:
        print('Wyjątek przy aktualizacji ceny pizzy:', e)

    try:
        result = menu.find_pizza("Nieistniejąca Pizza")
    except PizzeriaError as e:
        print('Wyjątek przy szukaniu pizzy:', e)

    print("\n3. Brak persystencji danych:")
    print("   Po zamknięciu programu wszystkie dane są tracone!")
    print("   Potrzebujemy zapisu/odczytu do pliku.")

    print("\n" + "=" * 50)
    print("Dzisiaj nauczymy się rozwiązywać te problemy!")
    print("=" * 50)


if __name__ == "__main__":
    main()
