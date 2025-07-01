class OrderNotFoundException(Exception):
    def __init__(self, order_id):
        super().__init__(f"Order with ID {order_id} not found or already canceled")
        self.order_id = order_id