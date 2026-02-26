# Klasa Pizza - reprezentuje pizzę w menu
# Baza startowa dla Weekendu 2 (bez obsługi wyjątków - to będzie temat tego weekendu!)
from exceptions import InvalidPriceError, PizzaNotFoundError

class Pizza:
    """Reprezentuje pojedynczą pizzę w menu."""

    def __init__(self, name, price):
        if price < 0:
            raise InvalidPriceError(price)
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.price} zł"

    def __repr__(self):
        return f"Pizza(name='{self.name}', price={self.price})"

    def __eq__(self, other):
        if isinstance(other, Pizza):
            return self.name == other.name and self.price == other.price
        return False

    def update_price(self, new_price):
        """Aktualizuje cenę pizzy."""
        if new_price < 0:
            raise InvalidPriceError(new_price)

        self.price = new_price

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        #pizza = Pizza('Margherita', 10)
        return cls(data['name'], data['price'])


class Menu:
    """Zarządza kolekcją pizz w menu."""

    def __init__(self):
        self.pizzas = []

    def add_pizza(self, pizza):
        """Dodaje pizzę do menu."""
        # TODO: Dodamy sprawdzenie typu i duplikatów z wyjątkami
        self.pizzas.append(pizza)
        print(f"Dodano pizzę: {pizza}")

    def remove_pizza(self, name):
        """Usuwa pizzę z menu po nazwie."""
        for pizza in self.pizzas:
            if pizza.name == name:
                self.pizzas.remove(pizza)
                print(f"Usunięto pizzę: {name}")
                return True
        print(f"Nie znaleziono pizzy: {name}")
        return False

    def find_pizza(self, name):
        """Znajduje pizzę po nazwie."""
        for pizza in self.pizzas:
            if pizza.name == name:
                return pizza

        raise PizzaNotFoundError(name)

    def list_pizzas(self):
        """Wyświetla wszystkie pizze w menu."""
        if not self.pizzas:
            print("Menu jest puste.")
            return
        print("Menu pizzerii:")
        for pizza in self.pizzas:
            print(f"  - {pizza}")

    def __len__(self):
        return len(self.pizzas)

    def __iter__(self):
        return iter(self.pizzas)

    def to_dict(self):
        return {
            'pizzas': [pizza.to_dict() for pizza in self.pizzas]
            #'pizzas': self.pizzas
        }

    @classmethod
    def from_dict(cls, data):
        #cls = Menu
        #menu = Menu()
        menu = cls()
        pizzas = data['pizzas']
        for pizza in pizzas:
            menu.add_pizza(Pizza.from_dict(pizza))
        return menu


