"""
Challenge 2.1: Shopping Cart System
===================================
YOUR TASK
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


class ShoppingCart():
    def __init__(self)->None:
        """Creates products instance variable dictionary"""
        self._products = {}
        self._subtotal = 0
        self._calculated_tax = 0

    def add_product(self, product: object, quantity:int=1)-> None:
        """Adds a project to the products instance var dictionary

        Args: 
            product - an instance of the Product class
            quantity - integer representing the number of products
        """
        if quantity <= 0 :
            raise ValueError("quantity must be positive")

        if product not in self._products:
            self._products[product] = quantity
        else:
            self._products[product] += quantity

    def remove_product(self, product_name_to_be_removed:str)-> None:
        """Removes a product from the shopping cart

        Args:
            product_name - String of product to be removed
        """
        product_names_list = [product.name for product in self._products.keys()]

        if product_name_to_be_removed not in product_names_list:
            raise ValueError("product not in cart")

        for product in self._products.copy():
            if product.name == product_name_to_be_removed:
                del self._products[product]
        
    def get_subtotal(self)-> int:
        """Calculate Shopping basket subtotal

        Returns string including subtotal
        """
        self._subtotal = 0
        for product, quantity in self._products.items():
            self._subtotal += (product.price * quantity)
        
        return self._subtotal

    def get_tax(self):
        """Calculates tax from the subtotal
        
        Returns calculated tax
        """
        self._calculated_tax = DEFAULT_TAX_RATE * self.get_subtotal()
        return self._calculated_tax 

    def get_total(self):
        """Calculates and returns total amount due"""
        return self.get_tax() + self._subtotal

    def __str__(self):
        result = 'Shopping Cart:\n'

        for product, quantity in self._products.items():
            line_total = product.price * quantity
            result += f"- {product.name} x{quantity}: ${line_total}\n"

        result += f"Subtotal: ${self._subtotal}\n"
        result += f"Tax (8%): ${self.get_tax():.2f}\n"
        result += f"Total: ${self.get_total():.2f}"
        return result


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

    # # Test empty name - Expected: ValueError
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

    print(f"Subtotal: ${cart.get_subtotal():.2f}")  # Expected: $9.71
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

    # # Try to remove product not in cart - Expected: ValueError
    try:
        cart.remove_product("Orange")
        print("❌ FAIL: Should raise ValueError for product not in cart")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    print("\n=== Testing Cart Validation ===")

    # # Try to add with negative quantity - Expected: ValueError
    try:
        cart.add_product(apple, -5)
        print("❌ FAIL: Should raise ValueError for negative quantity")
    except ValueError as e:
        print(f"✓ ValueError: {e}")