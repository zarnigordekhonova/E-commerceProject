import random, string, uuid


def generate_order_number():
    """Generate a unique order number combining timestamp and random digits."""
    random_part = ''.join(random.choices(string.digits, k=3))
    unique_part = str(uuid.uuid4().int)[:5]
    return f"{unique_part}{random_part}"