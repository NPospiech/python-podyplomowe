# Testy dla klas Pizza i Menu

import pytest
from .pizza import Pizza, Menu
from .exceptions import InvalidPriceError, PizzaNotFoundError, DuplicatePizzaError


class TestPizza:
    """Testy dla klasy Pizza."""

    def test_creation_valid(self):
        pizza = Pizza("Margherita", 25.0)
        assert pizza.name == "Margherita"
        assert pizza.price == 25.0

    def test_creation_int_price(self):
        pizza = Pizza("Test", 25)
        assert pizza.price == 25.0
        assert isinstance(pizza.price, float)

    def test_creation_negative_price_raises(self):
        with pytest.raises(InvalidPriceError) as exc_info:
            Pizza("Test", -10)
        assert exc_info.value.price == -10

    def test_creation_zero_price_raises(self):
        with pytest.raises(InvalidPriceError):
            Pizza("Test", 0)

    def test_creation_empty_name_raises(self):
        with pytest.raises(ValueError):
            Pizza("", 25.0)

    def test_creation_none_name_raises(self):
        with pytest.raises(ValueError):
            Pizza(None, 25.0)

    def test_creation_non_string_name_raises(self):
        with pytest.raises(TypeError):
            Pizza(123, 25.0)

    def test_str_representation(self):
        pizza = Pizza("Margherita", 25.0)
        result = str(pizza)
        assert result == "Margherita: 25.0 zł"

    def test_repr_representation(self):
        pizza = Pizza("Margherita", 25.0)
        result = repr(pizza)
        assert result == "Pizza(name='Margherita', price=25.0)"

    def test_equality_same_pizzas(self):
        pizza1 = Pizza("Margherita", 25.0)
        pizza2 = Pizza("Margherita", 25.0)
        assert pizza1 == pizza2

    def test_equality_different_names(self):
        pizza1 = Pizza("Margherita", 25.0)
        pizza2 = Pizza("Pepperoni", 25.0)
        assert pizza1 != pizza2

    def test_equality_different_prices(self):
        pizza1 = Pizza("Margherita", 25.0)
        pizza2 = Pizza("Margherita", 30.0)
        assert pizza1 != pizza2

    def test_equality_with_non_pizza(self):
        pizza = Pizza("Margherita", 25.0)
        assert pizza != "Margherita"
        assert pizza != 25.0
        assert pizza != None

    def test_update_price_valid(self):
        pizza = Pizza("Margherita", 25.0)
        pizza.update_price(30.0)
        assert pizza.price == 30.0

    def test_update_price_invalid_raises(self):
        pizza = Pizza("Margherita", 25.0)
        with pytest.raises(InvalidPriceError):
            pizza.update_price(-5)

    def test_apply_discount(self):
        pizza = Pizza("Margherita", 100.0)
        result = pizza.apply_discount(10)
        assert result == 90.0

    def test_apply_discount_zero(self):
        pizza = Pizza("Margherita", 100.0)
        result = pizza.apply_discount(0)
        assert result == 100.0

    def test_apply_discount_full(self):
        pizza = Pizza("Margherita", 100.0)
        result = pizza.apply_discount(100)
        assert result == 0.0

    def test_to_dict(self):
        pizza = Pizza("Margherita", 25.0)
        result = pizza.to_dict()
        assert result == {"name": "Margherita", "price": 25.0}

    def test_from_dict(self):
        data = {"name": "Pepperoni", "price": 30.0}
        pizza = Pizza.from_dict(data)
        assert pizza.name == "Pepperoni"
        assert pizza.price == 30.0

    def test_roundtrip_serialization(self):
        original = Pizza("Margherita", 25.0)
        data = original.to_dict()
        restored = Pizza.from_dict(data)
        assert original == restored


class TestMenu:
    """Testy dla klasy Menu."""

    def test_empty_menu(self):
        menu = Menu()
        assert len(menu) == 0

    def test_add_pizza(self, empty_menu, sample_pizza):
        empty_menu.add_pizza(sample_pizza)
        assert len(empty_menu) == 1
        assert sample_pizza in empty_menu.pizzas

    def test_add_multiple_pizzas(self, empty_menu):
        empty_menu.add_pizza(Pizza("Margherita", 25.0))
        empty_menu.add_pizza(Pizza("Pepperoni", 30.0))
        assert len(empty_menu) == 2

    def test_add_non_pizza_raises(self, empty_menu):
        with pytest.raises(TypeError):
            empty_menu.add_pizza("nie pizza")

    def test_add_duplicate_raises(self, sample_menu):
        with pytest.raises((ValueError, DuplicatePizzaError)):
            sample_menu.add_pizza(Pizza("Margherita", 30.0))

    def test_find_existing(self, sample_menu):
        found = sample_menu.find_pizza("Margherita")
        assert found is not None
        assert found.name == "Margherita"

    def test_find_not_existing_raises(self, sample_menu):
        with pytest.raises(PizzaNotFoundError) as exc_info:
            sample_menu.find_pizza("Carbonara")
        assert exc_info.value.pizza_name == "Carbonara"

    def test_remove_existing(self, sample_menu):
        sample_menu.remove_pizza("Margherita")
        assert len(sample_menu) == 2
        with pytest.raises(PizzaNotFoundError):
            sample_menu.find_pizza("Margherita")

    def test_remove_not_existing_raises(self, sample_menu):
        with pytest.raises(PizzaNotFoundError):
            sample_menu.remove_pizza("Carbonara")

    def test_get_cheapest(self, sample_menu):
        cheapest = sample_menu.get_cheapest()
        assert cheapest.name == "Margherita"
        assert cheapest.price == 25.0

    def test_get_cheapest_empty_menu(self, empty_menu):
        assert empty_menu.get_cheapest() is None

    def test_get_most_expensive(self, sample_menu):
        expensive = sample_menu.get_most_expensive()
        assert expensive.name == "Hawajska"
        assert expensive.price == 32.0

    def test_get_average_price(self, sample_menu):
        avg = sample_menu.get_average_price()
        expected = (25.0 + 30.0 + 32.0) / 3
        assert avg == pytest.approx(expected)

    def test_get_average_price_empty(self, empty_menu):
        assert empty_menu.get_average_price() == 0.0

    def test_len(self, sample_menu):
        assert len(sample_menu) == 3

    def test_iter(self, sample_menu):
        names = [pizza.name for pizza in sample_menu]
        assert "Margherita" in names
        assert "Pepperoni" in names
        assert "Hawajska" in names

    def test_save_and_load(self, sample_menu, temp_menu_file):
        sample_menu.save_to_file(str(temp_menu_file))
        loaded_menu = Menu()
        loaded_menu.load_from_file(str(temp_menu_file))
        assert len(loaded_menu) == 3
        assert loaded_menu.find_pizza("Margherita").price == 25.0

    def test_load_nonexistent_file(self, empty_menu, tmp_path):
        empty_menu.load_from_file(str(tmp_path / "nonexistent.json"))
        assert len(empty_menu) == 0
