# UMPIRE Problem-Solving Worksheet

**Problem Name:** ________________  **Date:** ________________

---

## U - UNDERSTAND

Build a multi-class shopping cart system. The ShoppingCart class takes an instance of the product
class.

Product Class
Attributes
Strings - name, category
float - price

Methods:
- __init__(name, price, category): Constructor
- __str__(): Return string representation

Validation:
- Name cannot be empty
- Price must be positive
- Category cannot be empty

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

---


---

## P - PLAN
[Write pseudocode and create test cases BEFORE coding]

**Pseudocode:**
```
Product()
- __init__(name, price, category): Constructor
```
do data validation in the constructor 


---

## I - IMPLEMENT
[Write your actual Python code with type hints and docstring]

```python
def function_name(param: type) -> return_type:
    """[Description]

    Args:
        param: [description]

    Returns:
        [description]
    """
    pass
```

---

## R - REVIEW
[Test your code, find bugs, verify edge cases]

**Test Results:** [which tests passed/failed?]
**Bugs Fixed:** [what bugs did you find and fix?]
**Quality Check:** [type hints? docstring? clear names? no magic numbers?]

---

## E - EVALUATE
[Analyze time/space complexity and possible improvements]

**Time Complexity:** O(___) because [explanation]
**Space Complexity:** O(___) because [explanation]
**Improvements:** [could you optimize further?]
**Learned:** [what did you learn from this problem?]
