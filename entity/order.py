from datetime import datetime

class Order:
    def __init__(self, order_id=None, customer_id=None, order_date=None, total_price=None, shipping_address=None):
        self.__order_id = order_id
        self.__customer_id = customer_id
        self.__order_date = order_date if order_date else datetime.now()
        self.__total_price = total_price
        self.__shipping_address = shipping_address

    # Getters
    @property
    def order_id(self):
        return self.__order_id

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def order_date(self):
        return self.__order_date

    @property
    def total_price(self):
        return self.__total_price

    @property
    def shipping_address(self):
        return self.__shipping_address

    # Setters
    @order_id.setter
    def order_id(self, order_id):
        self.__order_id = order_id

    @customer_id.setter
    def customer_id(self, customer_id):
        self.__customer_id = customer_id

    @order_date.setter
    def order_date(self, order_date):
        self.__order_date = order_date

    @total_price.setter
    def total_price(self, total_price):
        self.__total_price = total_price

    @shipping_address.setter
    def shipping_address(self, shipping_address):
        self.__shipping_address = shipping_address

    def __str__(self):
        return f"Order ID: {self.__order_id}, Customer ID: {self.__customer_id}, Date: {self.__order_date}, Total: {self.__total_price}, Address: {self.__shipping_address}"