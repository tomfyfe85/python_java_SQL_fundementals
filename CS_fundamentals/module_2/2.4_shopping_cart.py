"""
Challenge 2.1: Shopping Cart System

===================================
OBJECTIVE
===================================

Build a shopping cart system with products and a cart that calculates totals.
This challenge integrates everything you've learned in Module 2:
- Creating multiple classes
- Encapsulation
- Properties
- Input validation
- Working with collections

===================================
REQUIREMENTS
===================================

CLASS 1: Product
----------------
Attributes:
- name (str): Product name
- price (float): Product price
- category (str): Product category

Methods:
- __init__(name, price, category): Constructor
- __str__(): Return string representation

Validation:
- Name cannot be empty
- Price must be positive
- Category cannot be empty

===================================

CLASS 2: ShoppingCart
---------------------
Attributes:
- items (dict or list): Store products and quantities

Methods:
- add_product(product, quantity=1): Add product to cart
- remove_product(product_name): Remove product from cart
- get_subtotal(): Calculate total before tax
- get_tax(tax_rate=0.08): Calculate tax (default 8%)
- get_total(tax_rate=0.08): Calculate total with tax
- __str__(): Display cart contents

Validation:
- Quantity must be positive
- Can't remove product that isn't in cart

===================================
EXAMPLES
===================================

# Create products
apple = Product("Apple", 0.99, "Fruit")
banana = Product("Banana", 0.59, "Fruit")
bread = Product("Bread", 2.99, "Bakery")

# Create cart
cart = ShoppingCart()
cart.add_product(apple, quantity=5)
cart.add_product(banana, quantity=3)
cart.add_product(bread, quantity=1)

print(cart.get_subtotal())  # 7.69
print(cart.get_tax())       # 0.62 (8% of 7.69)
print(cart.get_total())     # 8.31

print(cart)
# Output:
# Shopping Cart:
# - Apple x5: $4.95
# - Banana x3: $1.77
# - Bread x1: $2.99
# Subtotal: $7.69
# Tax (8%): $0.62
# Total: $8.31

===================================
YOUR TASK
===================================

1. Start with UMPIRE planning
2. Implement the Product class first (simpler)
3. Test the Product class
4. Implement the ShoppingCart class
5. Test the complete system
6. Add docstrings and type hints

===================================
HINTS
===================================

For ShoppingCart.items, you could use:
- Dictionary: {product_name: {"product": Product, "quantity": int}}
- List of tuples: [(Product, quantity), ...]

Think about which would make it easier to:
- Find a product by name
- Update quantities
- Calculate totals

===================================
"""

# Constants
DEFAULT_TAX_RATE = 0.08

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================


# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing Product Class ===")

    # Create products
    apple = Product("Apple", 0.99, "Fruit")
    banana = Product("Banana", 0.59, "Fruit")
    bread = Product("Bread", 2.99, "Bakery")

    print(apple)    # Expected: Apple - $0.99 (Fruit)
    print(banana)   # Expected: Banana - $0.59 (Fruit)
    print(bread)    # Expected: Bread - $2.99 (Bakery)

    print("\n=== Testing Product Validation ===")

    # Test negative price - Expected: ValueError
    try:
        invalid = Product("Test", -5.00, "Test")
        print("❌ FAIL: Should raise ValueError for negative price")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test empty name - Expected: ValueError
    try:
        invalid = Product("", 5.00, "Test")
        print("❌ FAIL: Should raise ValueError for empty name")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    print("\n=== Testing ShoppingCart ===")

    # Create cart
    cart = ShoppingCart()

    # Add products
    cart.add_product(apple, 5)
    cart.add_product(banana, 3)
    cart.add_product(bread, 1)

    print(f"Subtotal: ${cart.get_subtotal():.2f}")  # Expected: $7.69
    print(f"Tax (8%): ${cart.get_tax():.2f}")       # Expected: $0.62
    print(f"Total: ${cart.get_total():.2f}")        # Expected: $8.31

    print("\n=== Full Cart Display ===")
    print(cart)
    # Expected:
    # Shopping Cart:
    # - Apple x5: $4.95
    # - Banana x3: $1.77
    # - Bread x1: $2.99
    # Subtotal: $7.69
    # Tax (8%): $0.62
    # Total: $8.31

    print("\n=== Testing Remove Product ===")

    cart.remove_product("Banana")
    print(f"After removing bananas:")
    print(f"Subtotal: ${cart.get_subtotal():.2f}")  # Expected: $7.94

    # Try to remove product not in cart - Expected: ValueError
    try:
        cart.remove_product("Orange")
        print("❌ FAIL: Should raise ValueError for product not in cart")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    print("\n=== Testing Cart Validation ===")

    # Try to add with negative quantity - Expected: ValueError
    try:
        cart.add_product(apple, -5)
        print("❌ FAIL: Should raise ValueError for negative quantity")
    except ValueError as e:
        print(f"✓ ValueError: {e}")