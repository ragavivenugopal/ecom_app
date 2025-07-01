import re
from datetime import datetime
from entity.customer import Customer
from entity.product import Product
from entity.cart import Cart
from entity.order import Order
from entity.order_item import OrderItem
from dao.order_processor_repository_impl import OrderProcessorRepositoryImpl
from exception.CustomerNotFoundException import CustomerNotFoundException
from exception.ProductNotFoundException import ProductNotFoundException
from exception.OrderNotFoundException import OrderNotFoundException


class EcomApp:
    def __init__(self):
        self.processor = OrderProcessorRepositoryImpl()

    def display_menu(self):
        print("\n===== E-Commerce Application Menu =====")
        print("1. Register Customer")
        print("2. Create Product")
        print("3. View All Products")
        print("4. View All Customers")
        print("5. Delete Product")
        print("6. Delete Customer")
        print("7. Add to Cart")
        print("8. Remove from Cart")
        print("9. View Cart")
        print("10. Place Order")
        print("11. Cancel Order")
        print("12. View Customer Orders")
        print("13. View Order by ID")
        print("14. Update Customer Information")
        print("15. View Orders by Date")
        print("16. Exit")

    # Validation helper methods
    def validate_name(self, name):
        if not name.strip():
            raise ValueError("Name cannot be empty")
        if len(name) > 100:
            raise ValueError("Name cannot exceed 100 characters")
        if not re.match(r'^[a-zA-Z\s\-\.\']+$', name):
            raise ValueError("Name can only contain letters, spaces, hyphens, apostrophes, and periods")
        return name

    def validate_email(self, email):
        if not email.strip():
            raise ValueError("Email cannot be empty")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Please enter a valid email address (e.g., user@example.com)")
        return email.lower()

    def validate_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one number")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")
        return password

    def validate_price(self, price):
        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than 0")
            return round(price, 2)
        except ValueError:
            raise ValueError("Price must be a valid number")

    def validate_stock(self, stock):
        try:
            stock = int(stock)
            if stock < 0:
                raise ValueError("Stock quantity cannot be negative")
            return stock
        except ValueError:
            raise ValueError("Stock quantity must be a whole number")

    def register_customer(self):
        print("\n--- Register Customer ---")
        while True:
            try:
                name = self.validate_name(input("Enter name: "))
                email = self.validate_email(input("Enter email: "))
                password = self.validate_password(input("Enter password: "))
                break
            except ValueError as e:
                print(f"Validation Error: {e}")
                if input("Try again? (yes/no): ").lower() != 'yes':
                    return

        customer = Customer(name=name, email=email, password=password)
        if self.processor.create_customer(customer):
            print("Customer registered successfully!")
        else:
            print("Failed to register customer.")

    def create_product(self):
        print("\n--- Create Product ---")
        while True:
            try:
                name = input("Enter product name: ").strip()
                if not name:
                    raise ValueError("Product name cannot be empty")

                price = self.validate_price(input("Enter price: "))
                description = input("Enter description: ").strip()
                if not description:
                    raise ValueError("Description cannot be empty")

                stock = self.validate_stock(input("Enter stock quantity: "))
                break
            except ValueError as e:
                print(f"Validation Error: {e}")
                if input("Try again? (yes/no): ").lower() != 'yes':
                    return

        product = Product(name=name, price=price, description=description, stock_quantity=stock)
        if self.processor.create_product(product):
            print("Product created successfully!")
        else:
            print("Failed to create product.")

    def view_all_products(self):
        print("\n--- All Products ---")
        products = self.processor.get_all_products()
        if not products:
            print("No products available.")
            return

        print(f"\n{'ID':<5} {'Name':<20} {'Price':<10} {'Stock':<10} Description")
        print("-" * 70)
        for product in products:
            print(
                f"{product.product_id:<5} {product.name:<20} ${product.price:<9.2f} {product.stock_quantity:<10} {product.description}")

    def view_all_customers(self):
        print("\n--- All Customers ---")
        customers = self.processor.get_all_customers()
        if not customers:
            print("No customers registered.")
            return

        print(f"\n{'ID':<5} {'Name':<20} {'Email':<30}")
        print("-" * 60)
        for customer in customers:
            print(f"{customer.customer_id:<5} {customer.name:<20} {customer.email:<30}")

    def delete_product(self):
        print("\n--- Delete Product ---")
        self.view_all_products()
        product_id = int(input("Enter product ID to delete: "))

        try:
            if self.processor.delete_product(product_id):
                print("Product deleted successfully!")
            else:
                print("Failed to delete product.")
        except ProductNotFoundException as e:
            print(f"Error: {e}")

    def delete_customer(self):
        print("\n--- Delete Customer ---")
        self.view_all_customers()
        customer_id = int(input("Enter customer ID to delete: "))

        try:
            if self.processor.delete_customer(customer_id):
                print("Customer deleted successfully!")
            else:
                print("Failed to delete customer.")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")

    def add_to_cart(self):
        print("\n--- Add to Cart ---")

        # Show available customers
        print("\nAvailable Customers:")
        customers = self.processor.get_all_customers()
        if not customers:
            print("No customers available.")
            return
        for customer in customers:
            print(f"{customer.customer_id}: {customer.name} ({customer.email})")

        # Show available products
        print("\nAvailable Products:")
        products = self.processor.get_all_products()
        if not products:
            print("No products available.")
            return
        for product in products:
            print(f"{product.product_id}: {product.name} (${product.price:.2f}, Stock: {product.stock_quantity})")

        while True:
            try:
                customer_id = int(input("\nEnter customer ID: "))
                product_id = int(input("Enter product ID: "))
                quantity = int(input("Enter quantity: "))

                # Check stock availability
                product = next((p for p in products if p.product_id == product_id), None)
                if not product:
                    raise ProductNotFoundException(product_id)
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")
                if quantity > product.stock_quantity:
                    raise ValueError(f"Only {product.stock_quantity} available in stock")

                break
            except ValueError as e:
                print(f"Error: {e}")
                if input("Try again? (yes/no): ").lower() != 'yes':
                    return
            except ProductNotFoundException as e:
                print(f"Error: {e}")
                if input("Try again? (yes/no): ").lower() != 'yes':
                    return

        customer = Customer(customer_id=customer_id)
        product = Product(product_id=product_id)

        try:
            cart_item = self.processor.add_to_cart(customer, product, quantity)
            if cart_item:
                print(f"Product added to cart successfully! Cart ID: {cart_item.cart_id}")
            else:
                print("Failed to add product to cart.")
        except (CustomerNotFoundException, ProductNotFoundException) as e:
            print(f"Error: {e}")

    def remove_from_cart(self):
        print("\n--- Remove from Cart ---")
        customer_id = int(input("Enter your customer ID: "))

        customer = Customer(customer_id=customer_id)

        try:
            cart_items = self.processor.get_all_from_cart(customer)
            if not cart_items:
                print("Your cart is empty!")
                return

            print("\nYour Cart Items:")
            for i, (cart, product) in enumerate(cart_items, 1):
                print(f"{i}. {product.name} (Qty: {cart.quantity})")

            item_num = int(input("\nEnter item number to remove: ")) - 1
            if 0 <= item_num < len(cart_items):
                cart_item = cart_items[item_num][0]
                product = cart_items[item_num][1]
                if self.processor.remove_from_cart(customer, product):
                    print(f"{product.name} removed from cart successfully!")
                else:
                    print("Failed to remove item from cart.")
            else:
                print("Invalid item number")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")

    def view_cart(self):
        print("\n--- View Cart ---")
        customer_id = int(input("Enter your customer ID: "))

        customer = Customer(customer_id=customer_id)

        try:
            cart_items = self.processor.get_all_from_cart(customer)
            if not cart_items:
                print("Your cart is empty!")
                return

            print("\nYour Cart Items:")
            total = 0
            for cart, product in cart_items:
                item_total = product.price * cart.quantity
                total += item_total
                print(f"Cart ID: {cart.cart_id}")
                print(f"{product.name} - ${product.price:.2f} x {cart.quantity} = ${item_total:.2f}")
                print("-" * 30)
            print(f"\nTotal: ${total:.2f}")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")

    def place_order(self):
        print("\n--- Place Order ---")
        customer_id = int(input("Enter your customer ID: "))
        shipping_address = input("Enter shipping address: ")

        customer = Customer(customer_id=customer_id)

        try:
            cart_items = self.processor.get_all_from_cart(customer)
            if not cart_items:
                print("Your cart is empty!")
                return

            print("\nOrder Summary:")
            total = 0.0
            for cart, product in cart_items:
                item_total = float(product.price) * cart.quantity
                total += item_total
                print(f"{product.name} - ${float(product.price):.2f} x {cart.quantity} = ${item_total:.2f}")
            print(f"\nTotal: ${total:.2f}")
            print(f"Shipping to: {shipping_address}")

            confirm = input("\nConfirm order (yes/no)? ").lower()
            if confirm == 'yes':
                order, order_items = self.processor.place_order(customer, cart_items, shipping_address, total)
                if order:
                    print(f"\nOrder placed successfully! Order ID: {order.order_id}")
                    print("Order Items:")
                    for item in order_items:
                        print(f"- Product ID: {item.product_id}, Quantity: {item.quantity}")
                else:
                    print("Failed to place order.")
            else:
                print("Order cancelled.")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")

    def cancel_order(self):
        print("\n--- Cancel Order ---")
        customer_id = int(input("Enter your customer ID: "))

        try:
            orders = self.processor.get_orders_by_customer(customer_id)
            if not orders:
                print("No orders found for this customer.")
                return

            print("\nYour Orders:")
            for order_id, (order, _) in orders.items():
                print(f"{order_id}. Order #{order.order_id} - ${order.total_price:.2f} - {order.order_date}")

            order_id = int(input("\nEnter order ID to cancel: "))
            if order_id in orders:
                if self.processor.cancel_order(order_id):
                    print("Order cancelled successfully!")
                else:
                    print("Failed to cancel order.")
            else:
                print("Invalid order ID")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")

    def view_customer_orders(self):
        print("\n--- View Customer Orders ---")
        customer_id = int(input("Enter customer ID: "))

        try:
            orders = self.processor.get_orders_by_customer(customer_id)
            if not orders:
                print("No orders found for this customer.")
                return

            for order_id, (order, items) in orders.items():
                print(f"\nOrder ID: {order.order_id}")
                print(f"Date: {order.order_date}")
                print(f"Total: ${order.total_price:.2f}")
                print(f"Shipping Address: {order.shipping_address}")
                print("\nProducts:")
                for item, product in items:
                    print(f"  {product.name} - ${product.price:.2f} x {item.quantity}")
        except CustomerNotFoundException as e:
            print(f"Error: {e}")

    def view_order_by_id(self):
        print("\n--- View Order by ID ---")
        order_id = int(input("Enter order ID: "))

        try:
            order, order_items = self.processor.get_order_by_id(order_id)
            print(f"\nOrder ID: {order.order_id}")
            print(f"Customer ID: {order.customer_id}")
            print(f"Date: {order.order_date}")
            print(f"Total: ${order.total_price:.2f}")
            print(f"Shipping Address: {order.shipping_address}")
            print("\nOrder Items:")
            for item in order_items:
                print(f"- Product ID: {item.product_id}, Quantity: {item.quantity}")
        except OrderNotFoundException as e:
            print(f"Error: {e}")

    def view_orders_by_date(self):
        print("\n--- View Orders by Date ---")
        while True:
            try:
                date_str = input("Enter date (YYYY-MM-DD): ")
                # Validate date format
                datetime.strptime(date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")
                if input("Try again? (yes/no): ").lower() != 'yes':
                    return

        orders = self.processor.get_orders_by_date(date_str)
        if not orders:
            print(f"No orders found for date {date_str}")
            return

        print(f"\nOrders for {date_str}:")
        for order_id, order_data in orders.items():
            order = order_data['order']
            customer = order_data['customer']
            items = order_data['items']

            print("\n" + "=" * 50)
            print(f"Order ID: {order.order_id}")
            print(f"Customer: {customer.name} ({customer.email})")
            print(f"Order Date: {order.order_date}")
            print(f"Total: ${order.total_price:.2f}")
            print(f"Shipping Address: {order.shipping_address}")
            print("\nOrder Items:")
            for item, product in items:
                print(f"  - {product.name} (Qty: {item.quantity}, Price: ${product.price:.2f} each)")
            print("=" * 50)

    def update_customer_information(self):
        print("\n--- Update Customer Information ---")

        # Show available customers
        customers = self.processor.get_all_customers()
        if not customers:
            print("No customers available to update.")
            return

        print("\nAvailable Customers:")
        for customer in customers:
            print(f"{customer.customer_id}: {customer.name} ({customer.email})")

        while True:
            try:
                customer_id = int(input("\nEnter customer ID to update: "))
                customer = next((c for c in customers if c.customer_id == customer_id), None)
                if not customer:
                    raise CustomerNotFoundException(customer_id)

                print("\nCurrent Information:")
                print(f"1. Name: {customer.name}")
                print(f"2. Email: {customer.email}")
                print(f"3. Password: ********")

                field = input("\nEnter field number to update (1-3) or 'cancel' to abort: ")
                if field.lower() == 'cancel':
                    return

                if field == '1':
                    new_name = self.validate_name(input("Enter new name: "))
                    customer.name = new_name
                elif field == '2':
                    new_email = self.validate_email(input("Enter new email: "))
                    customer.email = new_email
                elif field == '3':
                    new_password = self.validate_password(input("Enter new password: "))
                    customer.password = new_password
                else:
                    print("Invalid field selection")
                    continue

                if self.processor.update_customer(customer):
                    print("Customer information updated successfully!")
                else:
                    print("Failed to update customer information")
                break

            except ValueError as e:
                print(f"Error: {e}")
            except CustomerNotFoundException as e:
                print(f"Error: {e}")
                if input("Try again? (yes/no): ").lower() != 'yes':
                    return

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-15): ")

            try:
                if choice == '1':
                    self.register_customer()
                elif choice == '2':
                    self.create_product()
                elif choice == '3':
                    self.view_all_products()
                elif choice == '4':
                    self.view_all_customers()
                elif choice == '5':
                    self.delete_product()
                elif choice == '6':
                    self.delete_customer()
                elif choice == '7':
                    self.add_to_cart()
                elif choice == '8':
                    self.remove_from_cart()
                elif choice == '9':
                    self.view_cart()
                elif choice == '10':
                    self.place_order()
                elif choice == '11':
                    self.cancel_order()
                elif choice == '12':
                    self.view_customer_orders()
                elif choice == '13':
                    self.view_order_by_id()
                elif choice == '14':
                    self.update_customer_information()
                elif choice == '15':
                    self.view_orders_by_date()
                elif choice == '16':
                    print("Thank you for using our E-Commerce Application. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 15.")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    app = EcomApp()
    app.run()