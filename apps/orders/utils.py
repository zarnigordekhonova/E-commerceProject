import random
import time
from decimal import Decimal


def generate_order_number():
    """Generate a unique order number combining timestamp and random digits."""
    part1 = f"{random.randint(0, 9999):04d}"
    part2 = f"{int(time.time() *1000) % 100000:05d}"
    return f"{part1}_{part2}"
    


def calculate_shipping_cost(shipping_type):
    shipping_costs = {
        "FREE": Decimal("0.00"),
        "EXPRESS": Decimal("15.00"),
        "PICKUP": Decimal("5.00")
    }
    return shipping_costs.get(shipping_type, Decimal("0.00"))
