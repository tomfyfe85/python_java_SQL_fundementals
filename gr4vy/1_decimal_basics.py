"""
Exercise 1: Decimal for Currency (Fintech Fundamentals)

INTRODUCTION TO DECIMAL:

When working with MONEY in programming, NEVER use float!

WHY FLOAT IS DANGEROUS FOR MONEY:
>>> 0.1 + 0.2
0.30000000000000004  # WRONG! Should be 0.3

>>> price = 10.10
>>> price * 3
30.299999999999997  # WRONG! Should be 30.30

These errors happen because computers store floats in binary, which can't
represent decimal fractions precisely. This is CATASTROPHIC for finance!

THE DECIMAL SOLUTION:

The Decimal type stores numbers in base-10 (just like humans write them),
so there are no rounding errors.

>>> from decimal import Decimal
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')  # CORRECT!

CRITICAL RULES FOR DECIMAL:

1. ALWAYS create Decimal from STRING, never from float:
    ✓ Decimal('10.50')     # CORRECT
    ✗ Decimal(10.50)       # WRONG - still has float precision errors

2. Use QUANTIZE for rounding to cents:
    >>> from decimal import Decimal, ROUND_HALF_UP
    >>> amount = Decimal('10.567')
    >>> amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    Decimal('10.57')

3. Type hints use Decimal from typing:
    from decimal import Decimal
    def transfer(amount: Decimal) -> None:
        ...

===================================
EXERCISE 1: Decimal Basics
===================================

YOUR TASK:

Implement these functions to practice working with Decimal for currency.
This is ESSENTIAL for your Gr4vy test!

REQUIREMENTS:

1. add_amounts(amount1: Decimal, amount2: Decimal) -> Decimal
    - Add two currency amounts
    - Round result to 2 decimal places

2. multiply_amount(amount: Decimal, multiplier: Decimal) -> Decimal
    - Multiply amount by multiplier
    - Round result to 2 decimal places

3. validate_currency_amount(amount: Decimal) -> None
    - Raise ValueError if amount is negative
    - Raise ValueError if amount has more than 2 decimal places
    - Raise TypeError if amount is not a Decimal

EXAMPLES:

>>> add_amounts(Decimal('10.50'), Decimal('5.25'))
Decimal('15.75')

>>> multiply_amount(Decimal('10.00'), Decimal('1.5'))
Decimal('15.00')

>>> validate_currency_amount(Decimal('-5.00'))
ValueError: Amount cannot be negative

>>> validate_currency_amount(Decimal('10.567'))
ValueError: Amount cannot have more than 2 decimal places
"""

from decimal import Decimal, ROUND_HALF_UP

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================

def add_amounts(amount1: Decimal, amount2: Decimal) -> Decimal:
    """
    Add two currency amounts and round to 2 decimal places.

    Args:
        amount1: First amount
        amount2: Second amount

    Returns:
        Sum rounded to 2 decimal places
    """
    final = amount1 + amount2
    return final.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def multiply_amount(amount: Decimal, multiplier: Decimal) -> Decimal:
    """
    Multiply amount by multiplier and round to 2 decimal places.

    Args:
        amount: The base amount
        multiplier: The multiplier

    Returns:
        Product rounded to 2 decimal places
    """
    final = amount * multiplier
    return final.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def validate_currency_amount(amount: Decimal) -> None:
    """
    Validate that an amount is valid for currency operations.

    Args:
        amount: The amount to validate
s
    Raises:
        TypeError: If amount is not a Decimal
        ValueError: If amount is negative or has more than 2 decimal places
    """
    if not isinstance(amount, Decimal):
        raise TypeError("must be type decimal")
    
    if amount < Decimal('0.00'):
        raise ValueError("amount is negative")
    
    if amount.as_tuple().exponent < -2:
        raise ValueError("amount has more than 2 decimal places")




# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing Decimal Addition ===")
    result1 = add_amounts(Decimal('10.50'), Decimal('5.25'))
    print(f"10.50 + 5.25 = {result1}")
    assert result1 == Decimal('15.75'), f"Expected 15.75, got {result1}"

    result2 = add_amounts(Decimal('100.00'), Decimal('0.01'))
    print(f"100.00 + 0.01 = {result2}")
    assert result2 == Decimal('100.01'), f"Expected 100.01, got {result2}"

    print("\n=== Testing Decimal Multiplication ===")
    result3 = multiply_amount(Decimal('10.00'), Decimal('1.5'))
    print(f"10.00 * 1.5 = {result3}")
    assert result3 == Decimal('15.00'), f"Expected 15.00, got {result3}"

    result4 = multiply_amount(Decimal('7.77'), Decimal('3'))
    print(f"7.77 * 3 = {result4}")
    assert result4 == Decimal('23.31'), f"Expected 23.31, got {result4}"

    # # Test rounding
    result5 = multiply_amount(Decimal('10.00'), Decimal('0.333'))
    print(f"10.00 * 0.333 = {result5} (should round to 2 decimal places)")
    assert result5 == Decimal('3.33'), f"Expected 3.33, got {result5}"

    # print("\n=== Testing Validation ===")

    # # Test negative amount
    try:
        validate_currency_amount(Decimal('-5.00'))
        print("❌ FAIL: Should raise ValueError for negative amount")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test too many decimal places
    try:
        validate_currency_amount(Decimal('10.567'))
        print("❌ FAIL: Should raise ValueError for > 2 decimal places")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test wrong type
    try:
        validate_currency_amount(10.50)  # float, not Decimal
        print("❌ FAIL: Should raise TypeError for non-Decimal")
    except TypeError as e:
        print(f"✓ TypeError: {e}")

    # # Test valid amounts
    try:
        validate_currency_amount(Decimal('10.50'))
        print("✓ Valid: 10.50")

        validate_currency_amount(Decimal('0.00'))
        print("✓ Valid: 0.00")

        validate_currency_amount(Decimal('999999.99'))
        print("✓ Valid: 999999.99")
    except (ValueError, TypeError) as e:
        print(f"❌ FAIL: Should not raise exception for valid amounts: {e}")

    print("\n=== Why Decimal Matters (Demo) ===")
    print("Using float (WRONG):")
    float_result = 10.10 + 20.20 + 30.30
    print(f"  10.10 + 20.20 + 30.30 = {float_result}")
    print(f"  Expected: 60.60, Got: {float_result} ❌")

    print("\nUsing Decimal (CORRECT):")
    decimal_result = Decimal('10.10') + Decimal('20.20') + Decimal('30.30')
    print(f"  10.10 + 20.20 + 30.30 = {decimal_result}")
    print(f"  Expected: 60.60, Got: {decimal_result} ✓")

    print("\n✓ All tests passed!")
    print("\nKEY TAKEAWAYS:")
    print("1. ALWAYS use Decimal for money, never float")
    print("2. Create Decimal from string: Decimal('10.50')")
    print("3. Use quantize() to round to 2 decimal places")
    print("4. Validate amounts are non-negative and have max 2 decimal places")
