"""
Exercise 2.1: Bank Account Class

INTRODUCTION TO OBJECT-ORIENTED PROGRAMMING:

A CLASS is a blueprint/template for creating objects.
An OBJECT is a specific instance created from that class.

Think of it like a cookie cutter (class) and cookies (objects):
- The cookie cutter defines the shape
- Each cookie is a separate object made from that cutter
- You can make many cookies from one cutter

ANATOMY OF A CLASS:

class ClassName:
    def __init__(self, param1, param2):  # Constructor - runs when object is created
        self.attribute1 = param1          # Instance variable (data)
        self.attribute2 = param2          # Instance variable (data)

    def method_name(self):                # Method (behavior)
        return self.attribute1            # Access instance data with self

THE 'self' PARAMETER:
- Represents the specific instance of the class
- Always the first parameter in methods
- Python passes it automatically - you don't include it when calling methods

EXAMPLE:
    account1 = BankAccount("ACC001", "Alice", 1000.0)  # Creates first object
    account2 = BankAccount("ACC002", "Bob", 500.0)     # Creates second object

    account1.deposit(100)  # Only affects account1's balance
    account2.deposit(200)  # Only affects account2's balance

===================================
EXERCISE 2.1: Bank Account Class
===================================

Create a BankAccount class that manages a simple bank account with deposits,
withdrawals, and balance tracking.

REQUIREMENTS:

Class: BankAccount

Attributes (Instance Variables):
- account_number (str): Unique account identifier
- owner_name (str): Name of account owner
- balance (float): Current balance

Methods:
- __init__(account_number, owner_name, initial_balance=0.0): Constructor
- deposit(amount): Add money to account
- withdraw(amount): Remove money from account
- get_balance(): Return current balance
- __str__(): Return string representation

Validation Rules:
- Account number cannot be empty
- Owner name cannot be empty
- Initial balance cannot be negative
- Deposit amount must be positive
- Withdrawal amount must be positive
- Cannot withdraw more than current balance

Exceptions to Raise:
- TypeError: For wrong types
- ValueError: For invalid values

EXAMPLES:

# Create account
account = BankAccount("ACC001", "Alice Smith", 1000.0)
print(account)  # Account ACC001 (Alice Smith): Balance $1000.00

# Deposit money
account.deposit(500.0)
print(account.get_balance())  # 1500.0

# Withdraw money
account.withdraw(200.0)
print(account.get_balance())  # 1300.0

# Error handling
account.withdraw(2000.0)  # ValueError: Insufficient funds
account.deposit(-100.0)   # ValueError: Deposit amount must be positive

YOUR TASK:
1. Use UMPIRE to plan your approach
2. Implement the BankAccount class with all required methods
3. Add comprehensive validation and error handling
4. Test with the provided test cases
"""

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================


# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing BankAccount Creation ===")

    # Test 1: Create account with initial balance
    account1 = BankAccount("ACC001", "Alice Smith", 1000.0)
    print(account1)  # Should print: Account ACC001 (Alice Smith): Balance $1000.00

    # Test 2: Create account with default balance (0.0)
    account2 = BankAccount("ACC002", "Bob Jones")
    print(account2)  # Should print: Account ACC002 (Bob Jones): Balance $0.00

    print("\n=== Testing Deposits ===")
    account1.deposit(500.0)
    print(f"Balance after $500 deposit: ${account1.get_balance()}")  # Should be 1500.0

    account2.deposit(250.0)
    print(f"Balance after $250 deposit: ${account2.get_balance()}")  # Should be 250.0

    print("\n=== Testing Withdrawals ===")
    account1.withdraw(200.0)
    print(f"Balance after $200 withdrawal: ${account1.get_balance()}")  # Should be 1300.0

    print("\n=== Testing Error Handling ===")

    # Test negative initial balance
    try:
        bad_account = BankAccount("ACC003", "Charlie", -100.0)
        print("❌ FAIL: Should raise ValueError for negative initial balance")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test empty account number
    try:
        bad_account = BankAccount("", "Dave", 100.0)
        print("❌ FAIL: Should raise ValueError for empty account number")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test empty owner name
    try:
        bad_account = BankAccount("ACC004", "", 100.0)
        print("❌ FAIL: Should raise ValueError for empty owner name")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test negative deposit
    try:
        account1.deposit(-50.0)
        print("❌ FAIL: Should raise ValueError for negative deposit")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test negative withdrawal
    try:
        account1.withdraw(-50.0)
        print("❌ FAIL: Should raise ValueError for negative withdrawal")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test insufficient funds
    try:
        account1.withdraw(10000.0)
        print("❌ FAIL: Should raise ValueError for insufficient funds")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test type errors
    try:
        account1.deposit("100")
        print("❌ FAIL: Should raise TypeError for string deposit")
    except TypeError as e:
        print(f"✓ TypeError: {e}")

    print("\n=== Final Balances ===")
    print(f"Account 1: ${account1.get_balance()}")
    print(f"Account 2: ${account2.get_balance()}")
