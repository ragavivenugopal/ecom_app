from datetime import datetime
import mysql.connector
from dao.order_processor_repository import OrderProcessorRepository
from entity.cart import Cart
from entity.customer import Customer
from entity.order import Order
from entity.order_item import OrderItem
from entity.product import Product
from exception.CustomerNotFoundException import CustomerNotFoundException
from exception.OrderNotFoundException import OrderNotFoundException
from exception.ProductNotFoundException import ProductNotFoundException
from util.db_conn_util import DBConnUtil


class OrderProcessorRepositoryImpl(OrderProcessorRepository):
    def create_product(self, product):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM products WHERE name = %s", (product.name,))
            if cursor.fetchone():
                print("Product already exists!")
                return False

            cursor.execute(
                "INSERT INTO products (name, price, description, stock_quantity) VALUES (%s, %s, %s, %s)",
                (product.name, product.price, product.description, product.stock_quantity)
            )
            connection.commit()
            return True

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def create_customer(self, customer):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM customers WHERE email = %s", (customer.email,))
            if cursor.fetchone():
                print("Customer already exists!")
                return False

            cursor.execute(
                "INSERT INTO customers (name, email, password) VALUES (%s, %s, %s)",
                (customer.name, customer.email, customer.password)
            )
            connection.commit()
            return True

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return False

        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def delete_product(self, product_id):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            if not cursor.fetchone():
                raise ProductNotFoundException(product_id)

            cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            connection.commit()
            return True

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def delete_customer(self, customer_id):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if not cursor.fetchone():
                raise CustomerNotFoundException(customer_id)

            cursor.execute("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
            connection.commit()
            return True

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def add_to_cart(self, customer, product, quantity):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer.customer_id,))
            if not cursor.fetchone():
                raise CustomerNotFoundException(customer.customer_id)

            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product.product_id,))
            if not cursor.fetchone():
                raise ProductNotFoundException(product.product_id)

            cursor.execute(
                "SELECT * FROM cart WHERE customer_id = %s AND product_id = %s",
                (customer.customer_id, product.product_id)
            )
            existing_item = cursor.fetchone()

            if existing_item:
                new_quantity = existing_item[3] + quantity
                cursor.execute(
                    "UPDATE cart SET quantity = %s WHERE cart_id = %s",
                    (new_quantity, existing_item[0])
                )
                cart_id = existing_item[0]
            else:
                cursor.execute(
                    "INSERT INTO cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)",
                    (customer.customer_id, product.product_id, quantity)
                )
                cart_id = cursor.lastrowid

            connection.commit()
            return Cart(cart_id=cart_id, customer_id=customer.customer_id,
                        product_id=product.product_id, quantity=quantity)

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def remove_from_cart(self, customer, product):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer.customer_id,))
            if not cursor.fetchone():
                raise CustomerNotFoundException(customer.customer_id)

            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product.product_id,))
            if not cursor.fetchone():
                raise ProductNotFoundException(product.product_id)

            cursor.execute(
                "SELECT * FROM cart WHERE customer_id = %s AND product_id = %s",
                (customer.customer_id, product.product_id)
            )
            cart_item = cursor.fetchone()

            if not cart_item:
                print("Product not found in cart!")
                return False

            cursor.execute(
                "DELETE FROM cart WHERE customer_id = %s AND product_id = %s",
                (customer.customer_id, product.product_id)
            )

            connection.commit()
            return Cart(cart_id=cart_item[0], customer_id=cart_item[1],
                        product_id=cart_item[2], quantity=cart_item[3])

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_from_cart(self, customer):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer.customer_id,))
            if not cursor.fetchone():
                raise CustomerNotFoundException(customer.customer_id)

            cursor.execute("""
                           SELECT c.cart_id,
                                  c.customer_id,
                                  c.product_id,
                                  c.quantity,
                                  p.name,
                                  p.price,
                                  p.description,
                                  p.stock_quantity
                           FROM cart c
                                    JOIN products p ON c.product_id = p.product_id
                           WHERE c.customer_id = %s
                           """, (customer.customer_id,))

            cart_items = []
            for item in cursor.fetchall():
                product = Product(
                    product_id=item['product_id'],
                    name=item['name'],
                    price=item['price'],
                    description=item['description'],
                    stock_quantity=item['stock_quantity']
                )
                cart = Cart(
                    cart_id=item['cart_id'],
                    customer_id=item['customer_id'],
                    product_id=item['product_id'],
                    quantity=item['quantity']
                )
                cart_items.append((cart, product))

            return cart_items

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def place_order(self, customer, cart_items, shipping_address, total_price=None):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            # Validate customer exists
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer.customer_id,))
            if not cursor.fetchone():
                raise CustomerNotFoundException(customer.customer_id)

            # Calculate total price if not provided
            if total_price is None:
                total_price = 0.0
                for cart_item in cart_items:
                    cart, product = cart_item
                    quantity = cart.quantity
                    stock = product.stock_quantity

                    if stock < quantity:
                        print(f"Not enough stock for {product.name}. Available: {stock}, Requested: {quantity}")
                        return None, []

                    # Convert Decimal to float for consistent calculations
                    total_price += float(product.price) * quantity

            # Convert total_price to string to avoid DECIMAL type issues
            total_price_str = "{:.2f}".format(float(total_price))

            # Create order
            cursor.execute(
                """INSERT INTO orders
                       (customer_id, order_date, total_price, shipping_address)
                   VALUES (%s, %s, %s, %s)""",
                (customer.customer_id, datetime.now(), total_price_str, shipping_address)
            )
            order_id = cursor.lastrowid

            # Process order items
            order_items = []
            for cart_item in cart_items:
                cart, product = cart_item
                # Create order item
                cursor.execute(
                    """INSERT INTO order_items
                           (order_id, product_id, quantity)
                       VALUES (%s, %s, %s)""",
                    (order_id, product.product_id, cart.quantity)
                )

                # Update product stock
                cursor.execute(
                    """UPDATE products
                       SET stock_quantity = stock_quantity - %s
                       WHERE product_id = %s""",
                    (cart.quantity, product.product_id)
                )

                order_items.append(OrderItem(
                    order_item_id=cursor.lastrowid,
                    order_id=order_id,
                    product_id=product.product_id,
                    quantity=cart.quantity
                ))

            # Clear cart
            cursor.execute("DELETE FROM cart WHERE customer_id = %s", (customer.customer_id,))

            connection.commit()

            return Order(
                order_id=order_id,
                customer_id=customer.customer_id,
                order_date=datetime.now(),
                total_price=float(total_price_str),  # Return as float
                shipping_address=shipping_address
            ), order_items

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return None, []
        except Exception as e:
            print(f"Error placing order: {e}")
            if connection:
                connection.rollback()
            return None, []
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def cancel_order(self, order_id):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)

            # 1. Verify order exists and get details
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()
            if not order:
                raise OrderNotFoundException(order_id)

            # 2. Get all order items to restore stock
            cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
            order_items = cursor.fetchall()

            # 3. Restore product quantities
            for item in order_items:
                cursor.execute(
                    "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                    (item['quantity'], item['product_id'])
                )

            # 4. Delete order items
            cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))

            # 5. Delete the order
            cursor.execute("DELETE FROM orders WHERE order_id = %s", (order_id,))

            connection.commit()
            return True

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.rollback()
            return False
        except Exception as e:
            print(f"Error canceling order: {e}")
            if connection:
                connection.rollback()
            return False
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()


    def get_orders_by_customer(self, customer_id):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            if not cursor.fetchone():
                raise CustomerNotFoundException(customer_id)

            cursor.execute("""
                           SELECT o.order_id,
                                  o.customer_id,
                                  o.order_date,
                                  o.total_price,
                                  o.shipping_address,
                                  oi.order_item_id,
                                  oi.product_id,
                                  oi.quantity,
                                  p.name,
                                  p.price,
                                  p.description,
                                  p.stock_quantity
                           FROM orders o
                                    JOIN order_items oi ON o.order_id = oi.order_id
                                    JOIN products p ON oi.product_id = p.product_id
                           WHERE o.customer_id = %s
                           ORDER BY o.order_date DESC
                           """, (customer_id,))

            orders = {}
            for row in cursor.fetchall():
                order_id = row['order_id']
                if order_id not in orders:
                    orders[order_id] = (
                        Order(
                            order_id=order_id,
                            customer_id=row['customer_id'],
                            order_date=row['order_date'],
                            total_price=row['total_price'],
                            shipping_address=row['shipping_address']
                        ),
                        []
                    )

                order_item = OrderItem(
                    order_item_id=row['order_item_id'],
                    order_id=order_id,
                    product_id=row['product_id'],
                    quantity=row['quantity']
                )
                product = Product(
                    product_id=row['product_id'],
                    name=row['name'],
                    price=row['price'],
                    description=row['description'],
                    stock_quantity=row['stock_quantity']
                )
                orders[order_id][1].append((order_item, product))

            return orders

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return {}
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def get_order_by_id(self, order_id):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("""
                           SELECT o.*,
                                  oi.order_item_id,
                                  oi.product_id,
                                  oi.quantity,
                                  p.name,
                                  p.price,
                                  p.description,
                                  p.stock_quantity
                           FROM orders o
                                    LEFT JOIN order_items oi ON o.order_id = oi.order_id
                                    LEFT JOIN products p ON oi.product_id = p.product_id
                           WHERE o.order_id = %s
                           """, (order_id,))

            rows = cursor.fetchall()
            if not rows:
                raise OrderNotFoundException(order_id)

            order_data = rows[0]
            order = Order(
                order_id=order_data['order_id'],
                customer_id=order_data['customer_id'],
                order_date=order_data['order_date'],
                total_price=order_data['total_price'],
                shipping_address=order_data['shipping_address']
            )

            order_items = []
            for row in rows:
                if row['order_item_id']:
                    order_items.append(OrderItem(
                        order_item_id=row['order_item_id'],
                        order_id=row['order_id'],
                        product_id=row['product_id'],
                        quantity=row['quantity']
                    ))

            return order, order_items

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_products(self):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM products")
            products = []
            for row in cursor.fetchall():
                products.append(Product(
                    product_id=row['product_id'],
                    name=row['name'],
                    price=row['price'],
                    description=row['description'],
                    stock_quantity=row['stock_quantity']
                ))
            return products
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_customers(self):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT customer_id, name, email FROM customers")  # Don't select password
            customers = []
            for row in cursor.fetchall():
                customers.append(Customer(
                    customer_id=row['customer_id'],
                    name=row['name'],
                    email=row['email'],
                    password="********"  # Mask password
                ))
            return customers
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def update_customer(self, customer):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "UPDATE customers SET name = %s, email = %s, password = %s WHERE customer_id = %s",
                (customer.name, customer.email, customer.password, customer.customer_id)
            )
            connection.commit()
            return cursor.rowcount > 0
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def get_orders_by_date(self, order_date):
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)

            # Query to get orders for a specific date
            cursor.execute("""
                           SELECT o.order_id, o.customer_id, o.order_date, o.total_price, o.shipping_address,
                                  oi.order_item_id, oi.product_id, oi.quantity,
                                  p.name, p.price, p.description, p.stock_quantity,
                                  c.name  as customer_name, c.email as customer_email
                           FROM orders o
                                    JOIN order_items oi ON o.order_id = oi.order_id
                                    JOIN products p ON oi.product_id = p.product_id
                                    JOIN customers c ON o.customer_id = c.customer_id
                           WHERE DATE (o.order_date) = %s
                           ORDER BY o.order_date DESC
                           """, (order_date,))

            orders = {}
            for row in cursor.fetchall():
                order_id = row['order_id']
                if order_id not in orders:
                    orders[order_id] = {
                        'order': Order(
                            order_id=order_id,
                            customer_id=row['customer_id'],
                            order_date=row['order_date'],
                            total_price=row['total_price'],
                            shipping_address=row['shipping_address']
                        ),
                        'customer': Customer(
                            customer_id=row['customer_id'],
                            name=row['customer_name'],
                            email=row['customer_email'],
                            password="********"  # Masked for security
                        ),
                        'items': []
                    }

                order_item = OrderItem(
                    order_item_id=row['order_item_id'],
                    order_id=order_id,
                    product_id=row['product_id'],
                    quantity=row['quantity']
                )
                product = Product(
                    product_id=row['product_id'],
                    name=row['name'],
                    price=row['price'],
                    description=row['description'],
                    stock_quantity=row['stock_quantity']
                )
                orders[order_id]['items'].append((order_item, product))

            return orders

        except mysql.connector.Error as e:
            print(f"Database error: {e}")
            return {}
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()