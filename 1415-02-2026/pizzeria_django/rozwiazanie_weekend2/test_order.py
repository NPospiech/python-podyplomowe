# Testy dla klas Order i OrderManager

import pytest
from .pizza import Pizza
from .customer import Customer, VIPCustomer
from .order import Order, OrderItem, OrderManager
from .exceptions import (
    InvalidQuantityError,
    OrderNotFoundError,
    EmptyOrderError
)


class TestOrderItem:
    """Testy dla klasy OrderItem."""

    def test_creation(self, sample_pizza):
        item = OrderItem(sample_pizza, 2)
        assert item.pizza == sample_pizza
        assert item.quantity == 2

    def test_total_price(self, sample_pizza):
        item = OrderItem(sample_pizza, 2)
        assert item.total_price == 50.0

    def test_invalid_quantity_zero_raises(self, sample_pizza):
        with pytest.raises(InvalidQuantityError):
            OrderItem(sample_pizza, 0)

    def test_invalid_quantity_negative_raises(self, sample_pizza):
        with pytest.raises(InvalidQuantityError) as exc_info:
            OrderItem(sample_pizza, -2)
        assert exc_info.value.quantity == -2

    def test_non_pizza_raises(self):
        with pytest.raises(TypeError):
            OrderItem("nie pizza", 1)

    def test_str_representation(self, sample_pizza):
        item = OrderItem(sample_pizza, 2)
        result = str(item)
        assert "2x" in result
        assert "Margherita" in result
        assert "50" in result


class TestOrder:
    """Testy dla klasy Order."""

    def test_creation(self, sample_customer, reset_order_id):
        order = Order(sample_customer)
        assert order.customer == sample_customer
        assert len(order) == 0
        assert order.id == 1

    def test_id_increments(self, sample_customer, reset_order_id):
        o1 = Order(sample_customer)
        o2 = Order(sample_customer)
        assert o1.id == 1
        assert o2.id == 2

    def test_non_customer_raises(self, reset_order_id):
        with pytest.raises(TypeError):
            Order("nie klient")

    def test_add_item(self, sample_customer, sample_pizza, reset_order_id):
        order = Order(sample_customer)
        order.add_item(sample_pizza, 2)
        assert len(order) == 1

    def test_add_multiple_items(self, sample_customer, sample_menu, reset_order_id):
        order = Order(sample_customer)
        order.add_item(sample_menu.find_pizza("Margherita"), 1)
        order.add_item(sample_menu.find_pizza("Pepperoni"), 2)
        assert len(order) == 2

    def test_total_price(self, sample_customer, sample_menu, reset_order_id):
        order = Order(sample_customer)
        order.add_item(sample_menu.find_pizza("Margherita"), 2)
        order.add_item(sample_menu.find_pizza("Pepperoni"), 1)
        assert order.total_price == 80.0

    def test_total_price_with_vip_discount(self, sample_vip, sample_menu, reset_order_id):
        order = Order(sample_vip)
        order.add_item(sample_menu.find_pizza("Margherita"), 2)
        expected = 50 * 0.85
        assert order.total_price == expected

    def test_remove_item(self, sample_customer, sample_menu, reset_order_id):
        order = Order(sample_customer)
        order.add_item(sample_menu.find_pizza("Margherita"), 1)
        order.add_item(sample_menu.find_pizza("Pepperoni"), 1)
        result = order.remove_item("Margherita")
        assert result is True
        assert len(order) == 1

    def test_remove_nonexistent_item(self, sample_customer, reset_order_id):
        order = Order(sample_customer)
        result = order.remove_item("Nieistniejąca")
        assert result is False

    def test_process_with_items(self, sample_order):
        sample_order.process()

    def test_process_empty_raises(self, sample_customer, reset_order_id):
        order = Order(sample_customer)
        with pytest.raises(EmptyOrderError) as exc_info:
            order.process()
        assert exc_info.value.order_id == order.id


class TestOrderManager:
    """Testy dla klasy OrderManager."""

    def test_empty(self):
        manager = OrderManager()
        assert len(manager) == 0

    def test_create_order(self, empty_order_manager, sample_customer):
        order = empty_order_manager.create_order(sample_customer)
        assert order is not None
        assert len(empty_order_manager) == 1

    def test_find_existing(self, sample_order_manager):
        found = sample_order_manager.find_order(1)
        assert found is not None

    def test_find_not_existing_raises(self, sample_order_manager):
        with pytest.raises(OrderNotFoundError) as exc_info:
            sample_order_manager.find_order(999)
        assert exc_info.value.order_id == 999

    def test_cancel_order(self, sample_order_manager):
        initial_count = len(sample_order_manager)
        sample_order_manager.cancel_order(1)
        assert len(sample_order_manager) == initial_count - 1

    def test_cancel_nonexistent_raises(self, sample_order_manager):
        with pytest.raises(OrderNotFoundError):
            sample_order_manager.cancel_order(999)

    def test_get_total_revenue(self, sample_order_manager):
        revenue = sample_order_manager.get_total_revenue()
        expected = 50 + 25.5
        assert revenue == pytest.approx(expected)

    def test_iter(self, sample_order_manager):
        orders = list(sample_order_manager)
        assert len(orders) == 2
