# Klasy Order z pełną obsługą wyjątków

import json
from .pizza import Pizza
from .customer import Customer
from .exceptions import (
    InvalidQuantityError,
    OrderNotFoundError,
    EmptyOrderError
)


class OrderItem:
    """Reprezentuje pojedynczą pozycję w zamówieniu."""

    def __init__(self, pizza, quantity):
        if not isinstance(pizza, Pizza):
            raise TypeError("Oczekiwano obiektu Pizza!")
        if not isinstance(quantity, int):
            raise TypeError("Ilość musi być liczbą całkowitą!")
        if quantity <= 0:
            raise InvalidQuantityError(quantity)

        self.pizza = pizza
        self.quantity = quantity

    @property
    def total_price(self):
        return self.pizza.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.pizza.name} ({self.total_price} zł)"

    def to_dict(self):
        return {
            "pizza": self.pizza.to_dict(),
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        pizza = Pizza.from_dict(data["pizza"])
        return cls(pizza, data["quantity"])


class Order:
    """Reprezentuje zamówienie klienta."""

    _next_id = 1

    def __init__(self, customer):
        if not isinstance(customer, Customer):
            raise TypeError("Oczekiwano obiektu Customer!")
        self.customer = customer
        self.items = []
        self.id = Order._next_id
        Order._next_id += 1

    def add_item(self, pizza, quantity):
        item = OrderItem(pizza, quantity)
        self.items.append(item)

    def remove_item(self, pizza_name):
        for item in self.items:
            if item.pizza.name == pizza_name:
                self.items.remove(item)
                return True
        return False

    @property
    def total_price(self):
        total = sum(item.total_price for item in self.items)
        if hasattr(self.customer, 'apply_discount'):
            total = self.customer.apply_discount(total)
        return total

    def process(self):
        if not self.items:
            raise EmptyOrderError(self.id)

    def __str__(self):
        items_str = "\n".join(f"  - {item}" for item in self.items)
        discount_info = ""
        if hasattr(self.customer, 'discount_percent'):
            discount_info = f" (po rabacie VIP {self.customer.discount_percent}%)"
        return (f"Zamówienie #{self.id}\n"
                f"Klient: {self.customer.name}\n"
                f"Pozycje:\n{items_str}\n"
                f"Łącznie: {self.total_price} zł{discount_info}")

    def __len__(self):
        return len(self.items)

    @classmethod
    def reset_id_counter(cls):
        cls._next_id = 1


class OrderManager:
    """Zarządza kolekcją zamówień."""

    def __init__(self):
        self.orders = []

    def create_order(self, customer):
        order = Order(customer)
        self.orders.append(order)
        return order

    def cancel_order(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                self.orders.remove(order)
                return
        raise OrderNotFoundError(order_id)

    def find_order(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                return order
        raise OrderNotFoundError(order_id)

    def list_orders(self):
        if not self.orders:
            print("Brak zamówień.")
            return
        print("\n=== WSZYSTKIE ZAMÓWIENIA ===")
        for order in self.orders:
            status = "puste" if len(order) == 0 else f"{len(order)} poz."
            print(f"  - #{order.id}: {order.customer.name} - {order.total_price} zł ({status})")

    def get_total_revenue(self):
        return sum(order.total_price for order in self.orders)

    def __len__(self):
        return len(self.orders)

    def __iter__(self):
        return iter(self.orders)
