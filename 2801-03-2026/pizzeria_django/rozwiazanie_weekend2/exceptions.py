# Własne wyjątki dla aplikacji pizzerii
# Kompletna hierarchia wyjątków


class PizzeriaError(Exception):
    """Bazowy wyjątek dla wszystkich błędów pizzerii."""
    pass


# === Błędy walidacji ===

class ValidationError(PizzeriaError):
    """Błędy związane z walidacją danych."""
    pass


class InvalidPriceError(ValidationError):
    """Wyjątek rzucany gdy cena jest nieprawidłowa."""

    def __init__(self, price, message=None):
        self.price = price
        if message is None:
            message = f"Nieprawidłowa cena: {price} (musi być > 0)"
        super().__init__(message)


class InvalidQuantityError(ValidationError):
    """Wyjątek rzucany gdy ilość jest nieprawidłowa."""

    def __init__(self, quantity, message=None):
        self.quantity = quantity
        if message is None:
            message = f"Nieprawidłowa ilość: {quantity} (musi być > 0)"
        super().__init__(message)


class InvalidDiscountError(ValidationError):
    """Wyjątek rzucany gdy rabat jest nieprawidłowy."""

    def __init__(self, discount, message=None):
        self.discount = discount
        if message is None:
            message = f"Nieprawidłowy rabat: {discount}% (musi być 0-100)"
        super().__init__(message)


# === Błędy wyszukiwania ===

class NotFoundError(PizzeriaError):
    """Błędy gdy element nie został znaleziony."""
    pass


class PizzaNotFoundError(NotFoundError):
    """Wyjątek rzucany gdy pizza nie została znaleziona."""

    def __init__(self, pizza_name):
        self.pizza_name = pizza_name
        super().__init__(f"Pizza '{pizza_name}' nie została znaleziona w menu")


class CustomerNotFoundError(NotFoundError):
    """Wyjątek rzucany gdy klient nie został znaleziony."""

    def __init__(self, customer_id):
        self.customer_id = customer_id
        super().__init__(f"Klient o ID {customer_id} nie został znaleziony")


class OrderNotFoundError(NotFoundError):
    """Wyjątek rzucany gdy zamówienie nie zostało znalezione."""

    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Zamówienie o ID {order_id} nie zostało znalezione")


# === Błędy operacji ===

class OperationError(PizzeriaError):
    """Błędy podczas wykonywania operacji."""
    pass


class DuplicatePizzaError(OperationError):
    """Wyjątek rzucany gdy pizza już istnieje w menu."""

    def __init__(self, pizza_name):
        self.pizza_name = pizza_name
        super().__init__(f"Pizza '{pizza_name}' już istnieje w menu")


class EmptyOrderError(OperationError):
    """Wyjątek rzucany gdy zamówienie jest puste."""

    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Zamówienie #{order_id} jest puste - nie można go przetworzyć")
