# Testy integracyjne i E2E

import pytest
from .pizza import Pizza, Menu
from .customer import Customer, VIPCustomer, CustomerManager
from .order import Order, OrderManager
from .exceptions import PizzaNotFoundError, EmptyOrderError


class TestMenuCustomerIntegration:

    def test_vip_gets_discount_on_pizza(self, sample_menu, sample_vip):
        pizza = sample_menu.find_pizza("Margherita")
        original_price = pizza.price
        discounted = sample_vip.apply_discount(original_price)
        assert discounted < original_price
        assert discounted == original_price * 0.85


class TestOrderIntegration:

    def test_order_with_menu_and_customer(self, sample_menu, sample_customer, reset_order_id):
        order = Order(sample_customer)
        pizza1 = sample_menu.find_pizza("Margherita")
        pizza2 = sample_menu.find_pizza("Pepperoni")
        order.add_item(pizza1, 1)
        order.add_item(pizza2, 2)
        assert len(order) == 2
        assert order.total_price == 25 + 60

    def test_vip_order_discount_calculation(self, sample_menu, sample_vip, reset_order_id):
        order = Order(sample_vip)
        order.add_item(sample_menu.find_pizza("Margherita"), 4)
        expected = 100 * 0.85
        assert order.total_price == expected


class TestPersistenceIntegration:

    def test_menu_roundtrip(self, sample_menu, temp_menu_file):
        sample_menu.save_to_file(str(temp_menu_file))
        loaded = Menu()
        loaded.load_from_file(str(temp_menu_file))
        assert len(loaded) == len(sample_menu)
        for pizza in sample_menu:
            found = loaded.find_pizza(pizza.name)
            assert found.price == pizza.price

    def test_customers_roundtrip(self, sample_customer_manager, temp_customers_file, reset_customer_id):
        sample_customer_manager.save_to_file(str(temp_customers_file))
        Customer.reset_id_counter()
        loaded = CustomerManager()
        loaded.load_from_file(str(temp_customers_file))
        assert len(loaded) == len(sample_customer_manager)
        has_vip = any(isinstance(c, VIPCustomer) for c in loaded)
        assert has_vip


class TestE2E:

    def test_complete_application_flow(self, tmp_path):
        menu_file = tmp_path / "menu.json"
        customers_file = tmp_path / "customers.json"

        Customer.reset_id_counter()
        Order.reset_id_counter()

        menu = Menu()
        menu.add_pizza(Pizza("Margherita", 25.0))
        menu.add_pizza(Pizza("Pepperoni", 30.0))
        menu.add_pizza(Pizza("Hawajska", 32.0))
        menu.save_to_file(str(menu_file))

        customer_manager = CustomerManager()
        customer_manager.add_customer(Customer("Jan Kowalski", "123"))
        customer_manager.add_customer(VIPCustomer("Anna Nowak", "456", 15))
        customer_manager.save_to_file(str(customers_file))

        order_manager = OrderManager()
        customer = customer_manager.find_customer(1)
        order1 = order_manager.create_order(customer)
        order1.add_item(menu.find_pizza("Margherita"), 2)

        vip = customer_manager.find_customer(2)
        order2 = order_manager.create_order(vip)
        order2.add_item(menu.find_pizza("Pepperoni"), 1)

        # Session 2: load and continue
        Customer.reset_id_counter()
        Order.reset_id_counter()

        menu2 = Menu()
        menu2.load_from_file(str(menu_file))
        cm2 = CustomerManager()
        cm2.load_from_file(str(customers_file))

        assert len(menu2) == 3
        assert len(cm2) == 2

        om2 = OrderManager()
        new_customer = cm2.find_customer(1)
        new_order = om2.create_order(new_customer)
        new_order.add_item(menu2.find_pizza("Hawajska"), 1)

        assert new_order.total_price == 32.0
        assert new_order.customer.name == "Jan Kowalski"

    def test_error_handling_in_flow(self, sample_menu, sample_customer, reset_order_id):
        order_manager = OrderManager()
        order = order_manager.create_order(sample_customer)

        with pytest.raises(PizzaNotFoundError):
            pizza = sample_menu.find_pizza("Nieistniejąca")
            order.add_item(pizza, 1)

        with pytest.raises(EmptyOrderError):
            order.process()

        pizza = sample_menu.find_pizza("Margherita")
        order.add_item(pizza, 1)
        order.process()

    def test_statistics_calculation(self, sample_menu, reset_customer_id, reset_order_id):
        customer1 = Customer("Jan", "111")
        vip = VIPCustomer("Anna", "222", 20)

        order_manager = OrderManager()
        o1 = order_manager.create_order(customer1)
        o1.add_item(sample_menu.find_pizza("Margherita"), 2)

        o2 = order_manager.create_order(vip)
        o2.add_item(sample_menu.find_pizza("Pepperoni"), 1)

        o3 = order_manager.create_order(customer1)
        o3.add_item(sample_menu.find_pizza("Hawajska"), 1)

        total_revenue = order_manager.get_total_revenue()
        expected = 50 + 24 + 32
        assert total_revenue == expected
        assert len(order_manager) == 3

        assert sample_menu.get_cheapest().name == "Margherita"
        assert sample_menu.get_most_expensive().name == "Hawajska"
        assert sample_menu.get_average_price() == pytest.approx(29.0)
