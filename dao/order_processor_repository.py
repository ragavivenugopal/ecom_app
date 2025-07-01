from abc import ABC, abstractmethod
from entity.customer import Customer
from entity.product import Product


class OrderProcessorRepository(ABC):
    @abstractmethod
    def create_product(self, product):
        pass

    @abstractmethod
    def create_customer(self, customer):
        pass

    @abstractmethod
    def delete_product(self, product_id):
        pass

    @abstractmethod
    def delete_customer(self, customer_id):
        pass

    @abstractmethod
    def add_to_cart(self, customer, product, quantity):
        pass

    @abstractmethod
    def remove_from_cart(self, customer, product):
        pass

    @abstractmethod
    def get_all_from_cart(self, customer):
        pass

    @abstractmethod
    def place_order(self, customer, products_quantities, shipping_address):
        pass

    @abstractmethod
    def cancel_order(self, order_id):
        pass

    @abstractmethod
    def get_orders_by_customer(self, customer_id):
        pass

    @abstractmethod
    def get_orders_by_date(self, order_date):
        pass