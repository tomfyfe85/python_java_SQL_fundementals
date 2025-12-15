"""
Exercise 3: Account Class (Fintech Money Management)

INTRODUCTION TO ACCOUNT CLASS:

An Account represents a financial account that holds money.
Think of it like a digital wallet or bank account.

CORE RESPONSIBILITIES:
1. Store account information (ID, owner, balance)
2. Accept deposits (add money)
3. Process withdrawals (remove money)
4. Track balance accurately using Decimal

ENCAPSULATION:

We want to protect the balance from invalid modifications:
- Can't set balance to negative
- Can't withdraw more than available
- Can't deposit negative amounts

We use METHODS to control access to the balance:
- deposit() method validates and adds money
- withdraw() method validates and removes money
- get_balance() method safely returns current balance

USING DECIMAL FOR BALANCE:

CRITICAL: Always use Decimal for money, never float!

class Account:
    def __init__(self, account_id: str, owner: str, initial_balance: Decimal):
        self.balance = initial_balance  # Decimal type

===================================
EXERCISE 3: Account Class
===================================

YOUR TASK:

Implement an Account class for a money transfer system.
This is ESSENTIAL for your Gr4vy test!

REQUIREMENTS:

Class: Account

Attributes:
- account_id (str): Unique account identifier
- owner_name (str): Name of account owner
- balance (Decimal): Current balance (private - use _balance)

Methods:
- __init__(account_id, owner_name, initial_balance=Decimal('0.00')): Constructor
- deposit(amount: Decimal) -> None: Add money to account
- withdraw(amount: Decimal) -> None: Remove money from account
- get_balance() -> Decimal: Return current balance
- __str__() -> str: Return string representation

Validation Rules:
- account_id cannot be empty
- owner_name cannot be empty
- initial_balance cannot be negative
- initial_balance must be Decimal type
- deposit amount must be positive Decimal
- withdraw amount must be positive Decimal
- Cannot withdraw more than current balance

Exceptions to Raise:
- Use the custom exceptions from Exercise 2!
- InvalidAmountError: For invalid amounts
- InsufficientFundsError: For overdraft attempts
- ValueError: For empty strings
- TypeError: For wrong types

EXAMPLES:

# Create account
account = Account('ACC001', 'Alice', Decimal('1000.00'))
print(account)  # Account ACC001 (Alice): $1000.00

# Deposit money
account.deposit(Decimal('500.00'))
print(account.get_balance())  # Decimal('1500.00')

# Withdraw money
account.withdraw(Decimal('200.00'))
print(account.get_balance())  # Decimal('1300.00')

# Error handling
account.withdraw(Decimal('2000.00'))  # InsufficientFundsError
account.deposit(Decimal('-100.00'))   # InvalidAmountError

YOUR TASK:
1. Import the custom exceptions from Exercise 2
2. Implement the Account class with all required methods
3. Add comprehensive validation and error handling
4. Use Decimal for all money operations
5. Test with the provided test cases
"""

from decimal import Decimal
# Import your custom exceptions from exercise 2
from custom_exceptions import (
    TransferError,
    InsufficientFundsError,
    InvalidAmountError,
    AccountNotFoundError,
    SameAccountError
)

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================

class Account:
    """Represents a financial account with deposit and withdrawal capabilities"""

    def __init__(self, account_id: str, owner_name: str,
                initial_balance: Decimal = Decimal('0.00')) -> None:
        """
        Initialize a new account.

        Args:
            account_id: Unique account identifier
            owner_name: Name of account owner
            initial_balance: Starting balance (default: 0.00)

        Raises:
            ValueError: If account_id or owner_name is empty
            TypeError: If initial_balance is not Decimal
            InvalidAmountError: If initial_balance is negative
        """

        if account_id == "" or owner_name == "":
            raise ValueError("account and owner name must be present")

        if initial_balance < 0:
            raise InvalidAmountError("Initial balance cannot be negative")
        
        if type(initial_balance) is not Decimal:
            raise TypeError("Initial balance must be type decimal")


        self.account_id = account_id
        self.owner_name = owner_name
        self._balance = initial_balance

    def deposit(self, amount: Decimal) -> None:
        """
        Deposit money into the account.

        Args:
            amount: Amount to deposit

        Raises:
            TypeError: If amount is not Decimal
            InvalidAmountError: If amount is not positive
        """
        if amount <= 0:
            raise InvalidAmountError("amount must be positive")
        
        if type(amount) is not Decimal:
            raise TypeError("Amount must be type decimal")
        

        self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        """
        Withdraw money from the account.

        Args:
            amount: Amount to withdraw

        Raises:
            TypeError: If amount is not Decimal
            InvalidAmountError: If amount is not positive
            InsufficientFundsError: If balance is insufficient
        """
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds")
        
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        
        if type(amount) is not Decimal:
            raise TypeError("Amount must be type decimal")

        self._balance -= amount

    def get_balance(self) -> Decimal:
        """
        Get the current account balance.

        Returns:
            Current balance as Decimal
        """
        return self._balance

    def __str__(self) -> str:
        """
        Return string representation of account.

        Returns:
            Formatted string with account details
        """
        return f"Account {self.account_id} ({self.owner_name}): ${self._balance}"


# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing Account Creation ===")

    # # Test 1: Create account with initial balance
    account1 = Account('ACC001', 'Alice Smith', Decimal('1000.00'))
    print(account1)  # Account ACC001 (Alice Smith): $1000.00
    assert account1.get_balance() == Decimal('1000.00')

    # # Test 2: Create account with default balance
    account2 = Account('ACC002', 'Bob Jones')
    print(account2)  # Account ACC002 (Bob Jones): $0.00
    assert account2.get_balance() == Decimal('0.00')

    # print("\n=== Testing Deposits ===")
    account1.deposit(Decimal('500.00'))
    print(f"After $500 deposit: {account1}")
    assert account1.get_balance() == Decimal('1500.00')

    account2.deposit(Decimal('250.50'))
    print(f"After $250.50 deposit: {account2}")
    assert account2.get_balance() == Decimal('250.50')

    print("\n=== Testing Withdrawals ===")
    account1.withdraw(Decimal('200.00'))
    print(f"After $200 withdrawal: {account1}")
    assert account1.get_balance() == Decimal('1300.00')

    account2.withdraw(Decimal('50.25'))
    print(f"After $50.25 withdrawal: {account2}")
    assert account2.get_balance() == Decimal('200.25')

    print("\n=== Testing Error Handling ===")

    # Test empty account_id
    try:
        bad_account = Account('', 'Charlie', Decimal('100.00'))
        print("❌ FAIL: Should raise ValueError for empty account_id")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test empty owner_name
    try:
        bad_account = Account('ACC003', '', Decimal('100.00'))
        print("❌ FAIL: Should raise ValueError for empty owner_name")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # Test negative initial balance
    try:
        bad_account = Account('ACC003', 'Charlie', Decimal('-100.00'))
        print("❌ FAIL: Should raise InvalidAmountError for negative balance")
    except InvalidAmountError as e:
        print(f"✓ InvalidAmountError: {e}")

    # Test non-Decimal initial balance
    try:
        bad_account = Account('ACC003', 'Charlie', 100.00)  # float!
        print("❌ FAIL: Should raise TypeError for non-Decimal balance")
    except TypeError as e:
        print(f"✓ TypeError: {e}")

    # Test negative deposit
    try:
        account1.deposit(Decimal('-50.00'))
        print("❌ FAIL: Should raise InvalidAmountError for negative deposit")
    except InvalidAmountError as e:
        print(f"✓ InvalidAmountError: {e}")

    # Test zero deposit
    try:
        account1.deposit(Decimal('0.00'))
        print("❌ FAIL: Should raise InvalidAmountError for zero deposit")
    except InvalidAmountError as e:
        print(f"✓ InvalidAmountError: {e}")

    # Test non-Decimal deposit
    try:
        account1.deposit(50.00)  # float!
        print("❌ FAIL: Should raise TypeError for non-Decimal deposit")
    except TypeError as e:
        print(f"✓ TypeError: {e}")

    # Test insufficient funds
    try:
        account1.withdraw(Decimal('10000.00'))
        print("❌ FAIL: Should raise InsufficientFundsError")
    except InsufficientFundsError as e:
        print(f"✓ InsufficientFundsError: {e}")

    # # Test negative withdrawal
    try:
        account1.withdraw(Decimal('-50.00'))
        print("❌ FAIL: Should raise InvalidAmountError for negative withdrawal")
    except InvalidAmountError as e:
        print(f"✓ InvalidAmountError: {e}")

    print("\n=== Testing Decimal Precision ===")
    account3 = Account('ACC003', 'Charlie', Decimal('100.00'))

    # Multiple operations should maintain precision
    account3.deposit(Decimal('0.01'))
    account3.deposit(Decimal('0.01'))
    account3.deposit(Decimal('0.01'))
    print(f"After three $0.01 deposits: {account3}")
    assert account3.get_balance() == Decimal('100.03'), \
        "Decimal precision error!"

    print("\n=== Final Balances ===")
    print(f"Account 1: {account1.get_balance()}")
    print(f"Account 2: {account2.get_balance()}")
    print(f"Account 3: {account3.get_balance()}")

    print("\n✓ All tests passed!")
    print("\nKEY TAKEAWAYS:")
    print("1. Use Decimal for all money operations")
    print("2. Validate inputs in constructor and methods")
    print("3. Use custom exceptions for domain-specific errors")
    print("4. Encapsulate balance - only modify through methods")
    print("5. Provide clear error messages")
