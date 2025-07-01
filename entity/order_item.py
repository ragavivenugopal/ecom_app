class OrderItem:
    def __init__(self, order_item_id=None, order_id=None, product_id=None, quantity=None):
        self.__order_item_id = order_item_id
        self.__order_id = order_id
        self.__product_id = product_id
        self.__quantity = quantity

    #Getters
    @property
    def order_item_id(self):
        return self.__order_item_id

    @property
    def order_id(self):
        return self.__order_id

    @property
    def product_id(self):
        return self.__product_id

    @property
    def quantity(self):
        return self.__quantity

    #Setters
    @order_item_id.setter
    def order_item_id(self, order_item_id):
        self.__order_item_id = order_item_id

    @order_id.setter
    def order_id(self, order_id):
        self.__order_id = order_id

    @product_id.setter
    def product_id(self, product_id):
        self.__product_id = product_id

    @quantity.setter
    def quantity(self, quantity):
        self.__quantity = quantity

    def __str__(self):
        return f"Order Item ID: {self.__order_item_id}, Order ID: {self.__order_id}, Product ID: {self.__product_id}, Quantity: {self.__quantity}"