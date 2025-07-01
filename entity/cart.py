class Cart:
    def __init__(self, cart_id=None, customer_id=None, product_id=None, quantity=None):
        self.__cart_id = cart_id
        self.__customer_id = customer_id
        self.__product_id = product_id
        self.__quantity = quantity

    #Getters
    @property
    def cart_id(self):
        return self.__cart_id

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def product_id(self):
        return self.__product_id

    @property
    def quantity(self):
        return self.__quantity

    #Setters
    @cart_id.setter
    def cart_id(self, cart_id):
        self.__cart_id = cart_id

    @customer_id.setter
    def customer_id(self, customer_id):
        self.__customer_id = customer_id

    @product_id.setter
    def product_id(self, product_id):
        self.__product_id = product_id

    @quantity.setter
    def quantity(self, quantity):
        self.__quantity = quantity

    def __str__(self):
        return f"Cart ID: {self.__cart_id}, Customer ID: {self.__customer_id}, Product ID: {self.__product_id}, Quantity: {self.__quantity}"