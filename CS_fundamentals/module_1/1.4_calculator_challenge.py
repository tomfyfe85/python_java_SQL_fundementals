"""
Challenge 1.1: Calculator with Error Handling

Build a calculator that performs basic arithmetic operations with comprehensive error handling.

REQUIREMENTS:
Create a function: calculate(operation: str, a: float, b: float) -> float

Supported Operations:
- "add" - Addition
- "subtract" - Subtraction
- "multiply" - Multiplication
- "divide" - Division

Error Handling:
- Raise TypeError if inputs are not numbers
- Raise ValueError if operation is not supported
- Raise ZeroDivisionError if dividing by zero

Examples:
- calculate("add", 5, 3)        → 8.0
- calculate("subtract", 10, 4)  → 6.0
- calculate("multiply", 6, 7)   → 42.0
- calculate("divide", 15, 3)    → 5.0
- calculate("divide", 10, 0)    → ZeroDivisionError
- calculate("power", 2, 3)      → ValueError (unsupported operation)
- calculate("add", "5", 3)      → TypeError

BONUS CHALLENGE (Optional):
Extend the calculator to support:
- "power" - Exponentiation (a^b)
- "modulo" - Remainder (a % b)
- Handle negative numbers correctly

YOUR TASK:
1. Use the UMPIRE method to solve this problem
2. Write your understanding of the problem first
3. Plan your approach with test cases
4. Implement the function with type hints and docstring
5. Test thoroughly with all examples above
"""

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================


# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("Testing basic operations:")
    print(f"5 + 3 = {calculate('add', 5, 3)}")          # Should be 8.0
    print(f"10 - 4 = {calculate('subtract', 10, 4)}")   # Should be 6.0
    print(f"6 × 7 = {calculate('multiply', 6, 7)}")     # Should be 42.0
    print(f"15 ÷ 3 = {calculate('divide', 15, 3)}")     # Should be 5.0

    print("\nTesting error handling:")

    # Test division by zero
    try:
        calculate("divide", 10, 0)
        print("❌ FAIL: Should raise ZeroDivisionError")
    except ZeroDivisionError as e:
        print(f"✓ ZeroDivisionError: {e}")

    # Test unsupported operation
    try:
        calculate("power", 2, 3)
        print("❌ FAIL: Should raise ValueError")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test type error
    try:
        calculate("add", "5", 3)
        print("❌ FAIL: Should raise TypeError")
    except TypeError as e:
        print(f"✓ TypeError: {e}")

    # Test negative numbers
    print("\nTesting with negative numbers:")
    print(f"-5 + 3 = {calculate('add', -5, 3)}")       # Should be -2.0
    print(f"10 - (-4) = {calculate('subtract', 10, -4)}")  # Should be 14.0

    print("\n=== BONUS CHALLENGE ===")
    print("Uncomment these tests if you implement the bonus features:")
    # print(f"2 ^ 3 = {calculate('power', 2, 3)}")      # Should be 8.0
    # print(f"10 % 3 = {calculate('modulo', 10, 3)}")   # Should be 1.0
