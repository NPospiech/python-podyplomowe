# Klasy Pizza i Menu z pełną obsługą wyjątków i I/O

import json
from .exceptions import InvalidPriceError, PizzaNotFoundError, DuplicatePizzaError


class Pizza:
    """Reprezentuje pojedynczą pizzę w menu."""

    def __init__(self, name, price):
        if not name:
            raise ValueError("Nazwa pizzy nie może być pusta!")
        if not isinstance(name, str):
            raise TypeError("Nazwa pizzy musi być tekstem!")
        if not isinstance(price, (int, float)):
            raise TypeError("Cena musi być liczbą!")
        if price <= 0:
            raise InvalidPriceError(price)

        self.name = name
        self.price = float(price)

    def __str__(self):
        return f"{self.name}: {self.price} zł"

    def __repr__(self):
        return f"Pizza(name='{self.name}', price={self.price})"

    def __eq__(self, other):
        if isinstance(other, Pizza):
            return self.name == other.name and self.price == other.price
        return False

    def update_price(self, new_price):
        if new_price <= 0:
            raise InvalidPriceError(new_price)
        self.price = float(new_price)

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Rabat musi być w zakresie 0-100%")
        return self.price * (1 - percent / 100)

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["price"])


class Menu:
    """Zarządza kolekcją pizz w menu."""

    def __init__(self):
        self.pizzas = []

    def add_pizza(self, pizza):
        if not isinstance(pizza, Pizza):
            raise TypeError("Oczekiwano obiektu Pizza!")
        for p in self.pizzas:
            if p.name == pizza.name:
                raise DuplicatePizzaError(pizza.name)
        self.pizzas.append(pizza)

    def remove_pizza(self, name):
        for pizza in self.pizzas:
            if pizza.name == name:
                self.pizzas.remove(pizza)
                return
        raise PizzaNotFoundError(name)

    def find_pizza(self, name):
        for pizza in self.pizzas:
            if pizza.name == name:
                return pizza
        raise PizzaNotFoundError(name)

    def list_pizzas(self):
        if not self.pizzas:
            print("Menu jest puste.")
            return
        print("\n=== MENU PIZZERII ===")
        for pizza in self.pizzas:
            print(f"  - {pizza}")
        print(f"Razem: {len(self.pizzas)} pizz")

    def get_cheapest(self):
        if not self.pizzas:
            return None
        return min(self.pizzas, key=lambda p: p.price)

    def get_most_expensive(self):
        if not self.pizzas:
            return None
        return max(self.pizzas, key=lambda p: p.price)

    def get_average_price(self):
        if not self.pizzas:
            return 0.0
        return sum(p.price for p in self.pizzas) / len(self.pizzas)

    def __len__(self):
        return len(self.pizzas)

    def __iter__(self):
        return iter(self.pizzas)

    def __contains__(self, pizza):
        return pizza in self.pizzas

    def save_to_file(self, filename):
        try:
            data = [pizza.to_dict() for pizza in self.pizzas]
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Błąd zapisu do pliku: {e}")
            raise

    def load_from_file(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.pizzas = [Pizza.from_dict(item) for item in data]
        except FileNotFoundError:
            self.pizzas = []
        except json.JSONDecodeError:
            self.pizzas = []
