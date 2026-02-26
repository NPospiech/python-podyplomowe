# conftest.py - Współdzielone fixtures dla testów

import pytest
from .pizza import Pizza, Menu
from .customer import Customer, VIPCustomer, CustomerManager
from .order import Order, OrderManager


# === Fixtures dla Pizza ===

@pytest.fixture
def sample_pizza():
    return Pizza("Margherita", 25.0)


@pytest.fixture
def pizza_pepperoni():
    return Pizza("Pepperoni", 30.0)


@pytest.fixture
def pizza_hawajska():
    return Pizza("Hawajska", 32.0)


# === Fixtures dla Menu ===

@pytest.fixture
def empty_menu():
    return Menu()


@pytest.fixture
def sample_menu():
    menu = Menu()
    menu.add_pizza(Pizza("Margherita", 25.0))
    menu.add_pizza(Pizza("Pepperoni", 30.0))
    menu.add_pizza(Pizza("Hawajska", 32.0))
    return menu


# === Fixtures dla Customer ===

@pytest.fixture(autouse=False)
def reset_customer_id():
    Customer.reset_id_counter()
    yield
    Customer.reset_id_counter()


@pytest.fixture
def sample_customer(reset_customer_id):
    return Customer("Jan Kowalski", "123-456-789")


@pytest.fixture
def sample_vip(reset_customer_id):
    return VIPCustomer("Anna Nowak", "987-654-321", 15)


@pytest.fixture
def vip_20_percent(reset_customer_id):
    return VIPCustomer("Piotr Wiśniewski", "555-123-456", 20)


# === Fixtures dla CustomerManager ===

@pytest.fixture
def empty_customer_manager():
    return CustomerManager()


@pytest.fixture
def sample_customer_manager(sample_customer, sample_vip):
    manager = CustomerManager()
    manager.add_customer(sample_customer)
    manager.add_customer(sample_vip)
    return manager


# === Fixtures dla Order ===

@pytest.fixture(autouse=False)
def reset_order_id():
    Order.reset_id_counter()
    yield
    Order.reset_id_counter()


@pytest.fixture
def sample_order(sample_customer, sample_pizza, reset_order_id):
    order = Order(sample_customer)
    order.add_item(sample_pizza, 2)
    return order


@pytest.fixture
def vip_order(sample_vip, sample_menu, reset_order_id):
    order = Order(sample_vip)
    pizza = sample_menu.find_pizza("Margherita")
    order.add_item(pizza, 1)
    return order


# === Fixtures dla OrderManager ===

@pytest.fixture
def empty_order_manager():
    return OrderManager()


@pytest.fixture
def sample_order_manager(sample_customer, sample_vip, sample_menu, reset_order_id):
    manager = OrderManager()
    order1 = manager.create_order(sample_customer)
    order1.add_item(sample_menu.find_pizza("Margherita"), 2)
    order2 = manager.create_order(sample_vip)
    order2.add_item(sample_menu.find_pizza("Pepperoni"), 1)
    return manager


# === Fixtures dla plików tymczasowych ===

@pytest.fixture
def temp_menu_file(tmp_path):
    return tmp_path / "menu.json"


@pytest.fixture
def temp_customers_file(tmp_path):
    return tmp_path / "customers.json"
