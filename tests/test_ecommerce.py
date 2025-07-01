import unittest
from datetime import datetime

from dao.order_processor_repository_impl import OrderProcessorRepositoryImpl
from entity.customer import Customer
from entity.product import Product
from entity.order import Order
from entity.order_item import OrderItem
from entity.cart import Cart
from exception.CustomerNotFoundException import CustomerNotFoundException
from exception.ProductNotFoundException import ProductNotFoundException
from exception.OrderNotFoundException import OrderNotFoundException
from util.db_conn_util import DBConnUtil


class TestEcommerceSystem(unittest.TestCase):
    def setUp(self):
        self.processor = OrderProcessorRepositoryImpl()

        # Create fresh test data
        self.test_customer = Customer(name="Test User", email="test@unittest.com", password="test123")
        self.test_product = Product(name="Test Product", price=10.99, description="Unit Test Item", stock_quantity=100)

        # Create test records
        self.processor.create_customer(self.test_customer)
        self.processor.create_product(self.test_product)

        # Get generated IDs
        self.test_customer.customer_id = self._get_customer_id()
        self.test_product.product_id = self._get_product_id()

    def tearDown(self):
        self._delete_test_data()

    def _delete_test_data(self):
        """Cleanup test data from database"""
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor()

            # Delete in proper order to respect foreign keys
            cursor.execute(
                "DELETE FROM cart WHERE customer_id IN (SELECT customer_id FROM customers WHERE email = 'test@unittest.com')")
            cursor.execute(
                "DELETE FROM order_items WHERE product_id IN (SELECT product_id FROM products WHERE name = 'Test Product')")
            cursor.execute(
                "DELETE FROM orders WHERE customer_id IN (SELECT customer_id FROM customers WHERE email = 'test@unittest.com')")
            cursor.execute("DELETE FROM customers WHERE email = 'test@unittest.com'")
            cursor.execute("DELETE FROM products WHERE name = 'Test Product'")

            connection.commit()
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def _get_customer_id(self):
        """Get the auto-generated customer ID"""
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT customer_id FROM customers WHERE email = 'test@unittest.com'")
            return cursor.fetchone()['customer_id']
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def _get_product_id(self):
        """Get the auto-generated product ID"""
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT product_id FROM products WHERE name = 'Test Product'")
            return cursor.fetchone()['product_id']
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()

    def test_create_product(self):
        """Test Case 1: Product creation"""
        new_product = Product(name="New Test Product", price=19.99, description="New Item", stock_quantity=50)
        result = self.processor.create_product(new_product)
        self.assertTrue(result)

        # Verify in database
        product_id = self._get_product_id_by_name("New Test Product")
        self.assertIsNotNone(product_id)

        # Cleanup
        self.processor.delete_product(product_id)

    def test_add_to_cart(self):
        """Test Case 2: Add product to cart"""
        result = self.processor.add_to_cart(self.test_customer, self.test_product, 2)
        self.assertTrue(result)

        # Verify cart contents
        cart_items = self.processor.get_all_from_cart(self.test_customer)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0][1].name, "Test Product")  # [0][1] is the product tuple

    def test_place_order(self):
        """Test Case 3: Place order successfully"""
        # First add to cart
        self.processor.add_to_cart(self.test_customer, self.test_product, 1)

        # Place order
        cart_items = self.processor.get_all_from_cart(self.test_customer)
        result = self.processor.place_order(self.test_customer, cart_items, "123 Test St")
        self.assertTrue(result)

        # Verify order exists
        orders = self.processor.get_orders_by_customer(self.test_customer.customer_id)
        self.assertTrue(len(orders) > 0)

    def test_customer_not_found_exception(self):
        """Test Case 4: Invalid customer ID"""
        invalid_customer = Customer(customer_id=999)
        with self.assertRaises(CustomerNotFoundException):
            self.processor.add_to_cart(invalid_customer, self.test_product, 1)

    def test_product_not_found_exception(self):
        """Test Case 5: Invalid product ID"""
        invalid_product = Product(product_id=999)
        with self.assertRaises(ProductNotFoundException):
            self.processor.add_to_cart(self.test_customer, invalid_product, 1)

    def test_order_not_found_exception(self):
        """Test Case 6: Invalid order ID"""
        invalid_order_id = 999
        with self.assertRaises(OrderNotFoundException):
            self.processor.get_order_by_id(invalid_order_id)

    def test_get_all_from_cart(self):
        """Test Case 7: Verify cart returns correct structure"""
        self.processor.add_to_cart(self.test_customer, self.test_product, 1)
        cart_items = self.processor.get_all_from_cart(self.test_customer)

        # Should return list of (Cart, Product) tuples
        self.assertIsInstance(cart_items, list)
        self.assertIsInstance(cart_items[0][0], Cart)  # First item is Cart object
        self.assertIsInstance(cart_items[0][1], Product)  # Second is Product

    def test_get_orders_by_date(self):
        """Test Case: Get orders by date"""
        # First create an order
        self.processor.add_to_cart(self.test_customer, self.test_product, 1)
        cart_items = self.processor.get_all_from_cart(self.test_customer)
        self.processor.place_order(self.test_customer, cart_items, "123 Test St")

        # Get today's date
        today = datetime.now().date().isoformat()

        # Test getting orders by date
        orders = self.processor.get_orders_by_date(today)
        self.assertTrue(len(orders) > 0)

        # Verify structure
        order_id = next(iter(orders))
        self.assertIn('order', orders[order_id])
        self.assertIn('customer', orders[order_id])
        self.assertIn('items', orders[order_id])
        self.assertIsInstance(orders[order_id]['order'], Order)
        self.assertIsInstance(orders[order_id]['customer'], Customer)
        self.assertIsInstance(orders[order_id]['items'], list)

    def _get_product_id_by_name(self, name):
        """Helper to get product ID by name"""
        connection = None
        try:
            connection = DBConnUtil.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT product_id FROM products WHERE name = %s", (name,))
            result = cursor.fetchone()
            return result['product_id'] if result else None
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()


if __name__ == "__main__":
    unittest.main()