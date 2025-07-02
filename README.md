# Ecommerce App

##  Introduction

This is a simple console-based Ecommerce Application built using **Python** and **MySQL**. It follows object-oriented principles and demonstrates database interaction, exception handling, and unit testing.

The project is structured into different layers like entity, DAO, utility, and main application to keep the code clean and organized.

---

## Features

- **Customer Management**
  - Register a new customer
  - Delete a customer
  - View all customers

- **Product Management**
  - Add a new product
  - Delete a product
  - View all products

- **Cart Management**
  - Add product to cart
  - Remove product from cart
  - View items in cart

- **Order Management**
  - Place an order
  - Cancel an order
  - View orders by customer
  - View orders by ID
  - View orders by date


- **Exception Handling**
  
| Exception | Description |
|-----------|-------------|
| `CustomerNotFoundException` | Raised when customer ID doesn't exist |
| `ProductNotFoundException` | Raised when product ID doesn't exist |
| `OrderNotFoundException` | Raised when order ID doesn't exist |


- **General Validations**
  - Customer Name Validation 
     - Name cannot be empty or just whitespace
  - Email ID Validation 
    - Must contain @ and . 
    - Must not be empty or invalid format
  - Password Validation 
    - Must not be empty. 
    - Should be at least 6 characters long. 
  - Product Name & Description Validation 
    - Cannot be empty or null. 
  - Product Price Validation 
    - Must be a positive number. 
  - Stock Quantity Validation 
    - Must be a non-negative integer. 
  - Add to Cart Validation 
    - Quantity to add must be less than or equal to available stock. 
  - Shipping Address Validation (During Order)
    - Must not be empty.


- **Unit Testing**
  - Test cases to check if product creation, cart addition, and order placement work correctly

---

##  How the Project Works

1. Run the main file `EcomApp.py`
2. You'll see a menu with options like:
   - Register customer
   - Create Product
   - View All Products
   - View All Customers
   - Delete Product
   - Delete Customer
   - Add to Cart
   - Remove from Cart
   - View Cart
   - Place Order
   - Cancel Order
   - View Customer Orders
   - View Order by ID
   - Update Customer Information
   - View Orders by Date
   - Exit
3. Select an option by typing the corresponding number
4. Enter required details when prompted (like name, product ID, etc.)
5. Data is stored and managed using MySQL database
6. Custom error messages will be shown if something goes wrong (like invalid IDs)

---

##  Technologies Used

- Python 3
- MySQL
- MySQL Connector
- UnitTest (Python)




