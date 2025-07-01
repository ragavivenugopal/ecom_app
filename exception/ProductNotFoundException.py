class ProductNotFoundException(Exception):
    def __init__(self, product_id):
        super().__init__(f"Product with ID {product_id} not found")
        self.product_id = product_id