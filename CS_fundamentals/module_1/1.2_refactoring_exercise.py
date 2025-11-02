"""
Exercise 1.2: Refactoring Practice

Your task: Refactor the code below to follow clean code principles.

Requirements:
1. Meaningful function and variable names
2. Type hints on all functions
3. Docstrings for all functions
4. Replace magic numbers with named constants
5. Clear, readable logic

Run the original code first to understand what it does, then refactor!
"""

# ==========================================
# BAD CODE - DO NOT MODIFY THIS SECTION
# ==========================================

def f(x, y, z):
    a = x + y
    b = a * z
    if b > 100:
        return b - 10
    else:
        return b

def proc(data):
    r = []
    for d in data:
        if d > 0:
            r.append(d * 2)
    return r

x = 50
y = 30
result = x * 0.15
print(result)


# ==========================================
# YOUR REFACTORED CODE GOES BELOW
# ==========================================
MINIMUM_COST_FOR_DISCOUNT = 100
DISCOUNT = 10
UNITS_PER_CASE = 2
TAX_RATE = 0.15

def calculate_order_total(base_price: float, shipping_cost: float, quantity:int) -> float:
    """
    Calculate the total cost for an order with discount if applicable.
    
    Args:
        base_price: Base price of the item
        shipping_cost: Cost of shipping per item
        quantity: Number of items ordered

    Returns:
        Total order cost with discount applied if order exceeds $100
    """
    
    cost_per_unit = base_price + shipping_cost
    total_cost = cost_per_unit * quantity
    if total_cost > MINIMUM_COST_FOR_DISCOUNT:
        return total_cost - DISCOUNT
    else:
        return total_cost
    

def filter_and_convert_inventory(inventory: list[int]) -> list[int]:
    """
    Filter inventory for positive items and convert each case to total number of units

    Args:
        inventory: List of inventory changes (positive=added cases, negative=removed cases)

    Returns:
        List of individual units added (positive values only, converted from cases)
        """
    return [item * UNITS_PER_CASE for item in inventory if item > 0 ]


def calculate_sales_tax(purchase_amount: float) -> float:
    """Calculate sales tax on a purchase.

    Args:
        purchase_amount: The purchase amount before tax

    Returns:
        The tax amount 
    """
    tax_amount = purchase_amount * TAX_RATE
    return tax_amount


# ==========================================
# TESTS FOR YOUR REFACTORED CODE
# ==========================================

print("\n" + "="*50)
print("TESTING YOUR REFACTORED CODE")
print("="*50)

# Test calculate_order_total
print("\nTesting calculate_order_total():")
print(f"Order: $10 base + $5 shipping × 3 qty = ${calculate_order_total(10, 5, 3)}")  # Should be 45.0
print(f"Order: $20 base + $15 shipping × 4 qty = ${calculate_order_total(20, 15, 4)}")  # Should be 130.0 (140 - 10 discount)
print(f"Order: $50 base + $50 shipping × 1 qty = ${calculate_order_total(50, 50, 1)}")  # Should be 100.0 (no discount, exactly 100)
print(f"Order: $50 base + $51 shipping × 1 qty = ${calculate_order_total(50, 51, 1)}")  # Should be 91.0 (101 - 10 discount)

# # Test filter_and_convert_inventory
print("\nTesting filter_and_convert_inventory():")
print(f"Changes [1, -2, 3, -4, 5] → {filter_and_convert_inventory([1, -2, 3, -4, 5])}")  # Should be [2, 6, 10]
print(f"Changes [-1, -2, -3] → {filter_and_convert_inventory([-1, -2, -3])}")  # Should be []
print(f"Changes [10, 20, 30] → {filter_and_convert_inventory([10, 20, 30])}")  # Should be [20, 40, 60]

# # Test tax calculation
print("\nTesting calculate_sales_tax():")
purchase = 50
tax = calculate_sales_tax(purchase)
print(f"Tax on ${purchase} = ${tax}")  # Should be 7.5

