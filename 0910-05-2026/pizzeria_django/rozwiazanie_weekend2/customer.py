# Klasy Customer z pełną obsługą wyjątków i I/O

import json
from .exceptions import CustomerNotFoundError, InvalidDiscountError


class Customer:
    """Reprezentuje klienta pizzerii."""

    _next_id = 1

    def __init__(self, name, phone):
        if not name:
            raise ValueError("Nazwa klienta nie może być pusta!")
        if not isinstance(name, str):
            raise TypeError("Nazwa klienta musi być tekstem!")

        self.name = name
        self.phone = phone
        self.id = Customer._next_id
        Customer._next_id += 1

    def __str__(self):
        return f"Klient {self.id}: {self.name}, tel: {self.phone}"

    def __repr__(self):
        return f"Customer(name='{self.name}', phone='{self.phone}', id={self.id})"

    def update_phone(self, new_phone):
        self.phone = new_phone

    @classmethod
    def reset_id_counter(cls):
        cls._next_id = 1

    def to_dict(self):
        return {
            "type": "Customer",
            "id": self.id,
            "name": self.name,
            "phone": self.phone
        }

    @classmethod
    def from_dict(cls, data):
        customer = cls(data["name"], data["phone"])
        customer.id = data["id"]
        return customer


class VIPCustomer(Customer):
    """Klient VIP z rabatem i punktami lojalnościowymi."""

    def __init__(self, name, phone, discount_percent=10):
        super().__init__(name, phone)
        if not isinstance(discount_percent, (int, float)):
            raise TypeError("Rabat musi być liczbą!")
        if discount_percent < 0 or discount_percent > 100:
            raise InvalidDiscountError(discount_percent)
        self.discount_percent = discount_percent
        self.loyalty_points = 0

    def __str__(self):
        return f"VIP {super().__str__()}, zniżka: {self.discount_percent}%, punkty: {self.loyalty_points}"

    def add_loyalty_points(self, points):
        if points <= 0:
            raise ValueError("Liczba punktów musi być dodatnia!")
        self.loyalty_points += points

    def apply_discount(self, amount):
        return amount * (1 - self.discount_percent / 100)

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "VIPCustomer"
        data["discount_percent"] = self.discount_percent
        data["loyalty_points"] = self.loyalty_points
        return data

    @classmethod
    def from_dict(cls, data):
        vip = cls(data["name"], data["phone"], data["discount_percent"])
        vip.id = data["id"]
        vip.loyalty_points = data.get("loyalty_points", 0)
        return vip


class CustomerManager:
    """Zarządza kolekcją klientów."""

    def __init__(self):
        self.customers = []

    def add_customer(self, customer):
        if not isinstance(customer, Customer):
            raise TypeError("Oczekiwano obiektu Customer lub jego podklasy!")
        self.customers.append(customer)

    def remove_customer(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                self.customers.remove(customer)
                return
        raise CustomerNotFoundError(customer_id)

    def find_customer(self, customer_id):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer
        raise CustomerNotFoundError(customer_id)

    def list_customers(self):
        if not self.customers:
            print("Brak klientów.")
            return
        print("\n=== LISTA KLIENTÓW ===")
        for customer in self.customers:
            print(f"  - {customer}")
        print(f"Razem: {len(self.customers)} klientów")

    def __len__(self):
        return len(self.customers)

    def __iter__(self):
        return iter(self.customers)

    def save_to_file(self, filename):
        try:
            data = [customer.to_dict() for customer in self.customers]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Błąd zapisu: {e}")
            raise

    def load_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.customers = []
            for item in data:
                if item.get("type") == "VIPCustomer":
                    customer = VIPCustomer.from_dict(item)
                else:
                    customer = Customer.from_dict(item)
                self.customers.append(customer)
            if self.customers:
                max_id = max(c.id for c in self.customers)
                Customer._next_id = max_id + 1
        except FileNotFoundError:
            self.customers = []
