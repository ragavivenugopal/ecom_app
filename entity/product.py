class Product:
    def __init__(self,product_id=None,name=None,price=0.0,description=None,stock_quantity=0):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price) if price is not None else 0.0
        self.__description = description
        self.__stock_quantity = stock_quantity

    #Getters
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def description(self):
        return self.__description

    @property
    def stock_quantity(self):
        return self.__stock_quantity

    #Setters
    @product_id.setter
    def product_id(self,product_id):
        self.__product_id = product_id

    @name.setter
    def name(self,name):
        self.__name = name

    @price.setter
    def price(self,price):
        self.__price = price

    @description.setter
    def description(self,description):
        self.__description = description

    @stock_quantity.setter
    def stock_quantity(self,stock_quantity):
        self.__stock_quantity = stock_quantity

    def __str__(self):
        return f"Product ID: {self.__product_id},Name: {self.__name},Price: {self.__price},Description: {self.__description},Stock Quantity: {self.__stock_quantity}"