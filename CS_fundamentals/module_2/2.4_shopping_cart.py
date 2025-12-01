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

class Product():
    def __init__(self, name:str, price:float, category:str)->None:
        """Create Product object

        Args:
            name: Name of product
            price: Price in pounds
            category: Category of product

        Raises:
            ValueError if validation fails
        """
        if not name or not category:
            raise ValueError("Name and category cannot be empty")
        if price < 0.00:
            raise ValueError("Price must be above 0")


        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"{self.name} = ${self.price}, ({self.category})"





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