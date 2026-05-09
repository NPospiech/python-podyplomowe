# Testy dla klas Customer i CustomerManager

import pytest
from .customer import Customer, VIPCustomer, CustomerManager
from .exceptions import CustomerNotFoundError, InvalidDiscountError


class TestCustomer:
    """Testy dla klasy Customer."""

    def test_creation(self, reset_customer_id):
        customer = Customer("Jan Kowalski", "123-456-789")
        assert customer.name == "Jan Kowalski"
        assert customer.phone == "123-456-789"
        assert customer.id == 1

    def test_id_increments(self, reset_customer_id):
        c1 = Customer("Jan", "111")
        c2 = Customer("Anna", "222")
        c3 = Customer("Piotr", "333")
        assert c1.id == 1
        assert c2.id == 2
        assert c3.id == 3

    def test_empty_name_raises(self, reset_customer_id):
        with pytest.raises(ValueError):
            Customer("", "123")

    def test_str_representation(self, sample_customer):
        result = str(sample_customer)
        assert "Jan Kowalski" in result
        assert "123-456-789" in result

    def test_update_phone(self, sample_customer):
        sample_customer.update_phone("999-888-777")
        assert sample_customer.phone == "999-888-777"

    def test_to_dict(self, sample_customer):
        data = sample_customer.to_dict()
        assert data["type"] == "Customer"
        assert data["name"] == "Jan Kowalski"
        assert data["phone"] == "123-456-789"
        assert "id" in data

    def test_from_dict(self, reset_customer_id):
        data = {
            "type": "Customer",
            "id": 5,
            "name": "Test",
            "phone": "000"
        }
        customer = Customer.from_dict(data)
        assert customer.name == "Test"
        assert customer.id == 5


class TestVIPCustomer:
    """Testy dla klasy VIPCustomer."""

    def test_creation(self, reset_customer_id):
        vip = VIPCustomer("Anna", "123", 15)
        assert vip.name == "Anna"
        assert vip.discount_percent == 15
        assert vip.loyalty_points == 0

    def test_default_discount(self, reset_customer_id):
        vip = VIPCustomer("Anna", "123")
        assert vip.discount_percent == 10

    def test_invalid_discount_negative_raises(self, reset_customer_id):
        with pytest.raises(InvalidDiscountError):
            VIPCustomer("Test", "000", -5)

    def test_invalid_discount_over_100_raises(self, reset_customer_id):
        with pytest.raises(InvalidDiscountError) as exc_info:
            VIPCustomer("Test", "000", 150)
        assert exc_info.value.discount == 150

    def test_apply_discount(self, sample_vip):
        result = sample_vip.apply_discount(100)
        assert result == 85.0

    def test_apply_discount_20_percent(self, vip_20_percent):
        result = vip_20_percent.apply_discount(100)
        assert result == 80.0

    def test_add_loyalty_points(self, sample_vip):
        sample_vip.add_loyalty_points(50)
        assert sample_vip.loyalty_points == 50

    def test_add_loyalty_points_multiple(self, sample_vip):
        sample_vip.add_loyalty_points(30)
        sample_vip.add_loyalty_points(20)
        assert sample_vip.loyalty_points == 50

    def test_add_loyalty_points_negative_raises(self, sample_vip):
        with pytest.raises(ValueError):
            sample_vip.add_loyalty_points(-10)

    def test_inheritance(self, sample_vip):
        assert isinstance(sample_vip, Customer)

    def test_to_dict(self, sample_vip):
        data = sample_vip.to_dict()
        assert data["type"] == "VIPCustomer"
        assert data["discount_percent"] == 15
        assert "loyalty_points" in data


class TestCustomerManager:
    """Testy dla klasy CustomerManager."""

    def test_empty(self):
        manager = CustomerManager()
        assert len(manager) == 0

    def test_add_customer(self, empty_customer_manager, sample_customer):
        empty_customer_manager.add_customer(sample_customer)
        assert len(empty_customer_manager) == 1

    def test_add_non_customer_raises(self, empty_customer_manager):
        with pytest.raises(TypeError):
            empty_customer_manager.add_customer("nie klient")

    def test_find_existing(self, sample_customer_manager, sample_customer):
        found = sample_customer_manager.find_customer(sample_customer.id)
        assert found is not None
        assert found.name == sample_customer.name

    def test_find_not_existing_raises(self, sample_customer_manager):
        with pytest.raises(CustomerNotFoundError) as exc_info:
            sample_customer_manager.find_customer(999)
        assert exc_info.value.customer_id == 999

    def test_len(self, sample_customer_manager):
        assert len(sample_customer_manager) == 2

    def test_iter(self, sample_customer_manager):
        customers = list(sample_customer_manager)
        assert len(customers) == 2

    def test_save_and_load(self, sample_customer_manager, temp_customers_file, reset_customer_id):
        sample_customer_manager.save_to_file(str(temp_customers_file))
        Customer.reset_id_counter()
        loaded = CustomerManager()
        loaded.load_from_file(str(temp_customers_file))
        assert len(loaded) == 2
        vip_found = False
        for c in loaded:
            if isinstance(c, VIPCustomer):
                vip_found = True
                assert c.discount_percent == 15
        assert vip_found
