class Customer:
    def __init__(self, customer_id=None, name=None, email=None, password=None):
        self.__customer_id = customer_id
        self.__name = name
        self.__email = email
        self.__password = password

    # Getters
    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    # Setters
    @customer_id.setter
    def customer_id(self, customer_id):
        self.__customer_id = customer_id

    @name.setter
    def name(self, name):
        self.__name = name

    @email.setter
    def email(self, email):
        self.__email = email

    @password.setter
    def password(self, password):
        self.__password = password

    def __str__(self):
        return f"Customer ID: {self.__customer_id}, Name: {self.__name}, Email: {self.__email}"