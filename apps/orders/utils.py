import random, string, uuid
from decimal import Decimal


def generate_order_number():
    """Generate a unique order number combining timestamp and random digits."""
    random_part = ''.join(random.choices(string.digits, k=3))
    unique_part = str(uuid.uuid4().int)[:5]
    return f"{unique_part}{random_part}"


def calculate_shipping_cost(shipping_type):
    shipping_costs = {
        "FREE": Decimal("0.00"),
        "EXPRESS": Decimal("15.00"),
        "PICKUP": Decimal("5.00")
    }
    return shipping_costs.get(shipping_type, Decimal("0.00"))
