def calculate_discount(price, is_member):
    discount = 0
    if is_member:
        discount = 0.10
    if price > 100:
        discount += 0.05
    return price * (1 - discount)
