"""
Exercise 4: TransferService (Complete Money Transfer System)

INTRODUCTION TO TRANSFER SERVICE:

A TransferService manages multiple accounts and coordinates transfers between them.

Think of it as the "bank" that:
1. Stores all accounts in a registry (dictionary)
2. Looks up accounts by ID (O(1) with dictionary!)
3. Validates transfers
4. Coordinates moving money from A to B

WHY USE A DICTIONARY?

Accounts need to be found by ID quickly:
- List: O(n) - must search through all accounts
- Dictionary: O(1) - instant lookup by key

accounts = {
    'ACC001': Account('ACC001', 'Alice', Decimal('1000.00')),
    'ACC002': Account('ACC002', 'Bob', Decimal('500.00'))
}

account = accounts['ACC001']  # Instant lookup!

TRANSFER LOGIC:

To transfer $100 from Alice to Bob:
1. Validate amount is positive
2. Validate accounts are different
3. Look up Alice's account (raise error if not found)
4. Look up Bob's account (raise error if not found)
5. Withdraw from Alice (this checks sufficient funds)
6. Deposit to Bob

If withdrawal fails, deposit never happens - money is safe!

SEPARATION OF CONCERNS:

- Account: Manages individual account balance
- TransferService: Manages collection of accounts and transfers

This follows Single Responsibility Principle (SRP)!

===================================
EXERCISE 4: TransferService Class
===================================

YOUR TASK:

Implement a TransferService class that manages accounts and transfers.
This is the COMPLETE system for your Gr4vy test!

REQUIREMENTS:

Class: TransferService

Attributes:
- accounts (dict[str, Account]): Dictionary mapping account_id to Account

Methods:
- __init__(): Constructor (initializes empty accounts dict)
- create_account(account_id, owner_name, initial_balance) -> Account:
    Creates and stores a new account
- get_account(account_id) -> Account:
    Retrieves account by ID
- transfer(from_account_id, to_account_id, amount) -> None:
    Transfers money between accounts
- get_total_money() -> Decimal:
    Returns sum of all account balances (for testing)

Validation Rules:
- Cannot create account with duplicate ID
- Transfer amount must be positive Decimal
- Source and destination accounts must exist
- Source and destination must be different
- Source must have sufficient funds

Exceptions to Raise:
- AccountNotFoundError: If account doesn't exist
- InvalidAmountError: For invalid amounts
- SameAccountError: For same source/destination
- InsufficientFundsError: Raised by Account.withdraw()
- ValueError: For duplicate account IDs

EXAMPLES:

# Create service
service = TransferService()

# Create accounts
alice = service.create_account('ACC001', 'Alice', Decimal('1000.00'))
bob = service.create_account('ACC002', 'Bob', Decimal('500.00'))

# Transfer money
service.transfer('ACC001', 'ACC002', Decimal('100.00'))

# Check balances
print(alice.get_balance())  # Decimal('900.00')
print(bob.get_balance())    # Decimal('600.00')

YOUR TASK:
1. Import Account and exceptions
2. Implement the TransferService class
3. Use a dictionary for O(1) account lookup
4. Add comprehensive validation
5. Test with the provided test cases
"""

from decimal import Decimal
from account_class import Account
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

class TransferService:
    """Manages accounts and coordinates money transfers"""

    def __init__(self) -> None:
        """Initialize the transfer service with an empty account registry"""
        self._account_registry = {}

    def create_account(self, account_id: str, owner_name: str,
                    initial_balance: Decimal = Decimal('0.00')) -> Account:
        """
        Create a new account and add it to the registry.

        Args:
            account_id: Unique account identifier
            owner_name: Name of account owner
            initial_balance: Starting balance (default: 0.00)

        Returns:
            The newly created Account

        Raises:
            ValueError: If account_id already exists
        """
        if account_id in self._account_registry:
            raise ValueError("Account already registered")

        new_account = Account(account_id, owner_name, initial_balance)
        self._account_registry[account_id] = new_account
        return new_account

    def get_account(self, account_id: str) -> Account:
        """
        Retrieve an account by ID.

        Args:
            account_id: Account identifier to look up

        Returns:
            The Account object

        Raises:
            AccountNotFoundError: If account doesn't exist
        """
        if account_id not in self._account_registry:
            raise AccountNotFoundError("Account not found")

        found_account = self._account_registry[account_id]
        return found_account

    def transfer(self, from_account_id: str, to_account_id: str,
                amount: Decimal) -> None:
        """
        Transfer money from one account to another.

        Args:
            from_account_id: Source account ID
            to_account_id: Destination account ID
            amount: Amount to transfer

        Raises:
            AccountNotFoundError: If either account doesn't exist
            SameAccountError: If source and destination are the same
            InvalidAmountError: If amount is invalid
            InsufficientFundsError: If source has insufficient funds
        """
        if from_account_id == to_account_id:
            raise SameAccountError("to and from account id's can't be the same")
        
        if from_account_id not in self._account_registry or to_account_id not in self._account_registry:
            raise AccountNotFoundError("Both accounts must be registered")

        source_account = self._account_registry[from_account_id]
        destination_account = self._account_registry[to_account_id]

        source_account.withdraw(amount)
        destination_account.deposit(amount)


    def get_total_money(self) -> Decimal:
        """
        Calculate total money across all accounts.
        Useful for testing that transfers don't create/destroy money!

        Returns:
            Sum of all account balances
        """
        sum_of_account_balances = 0

        for account in self._account_registry.values():
            sum_of_account_balances += account.get_balance()

        return sum_of_account_balances
# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing TransferService Creation ===")
    service = TransferService()
    print("✓ TransferService created")

    print("\n=== Testing Account Creation ===")
    alice = service.create_account('ACC001', 'Alice', Decimal('1000.00'))
    print(f"Created: {alice}")

    bob = service.create_account('ACC002', 'Bob', Decimal('500.00'))
    print(f"Created: {bob}")

    charlie = service.create_account('ACC003', 'Charlie')
    print(f"Created: {charlie}")

    # # Test duplicate account ID
    try:
        service.create_account('ACC001', 'Eve', Decimal('100.00'))
        print("❌ FAIL: Should raise ValueError for duplicate ID")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    print("\n=== Testing Account Lookup ===")
    found_account = service.get_account('ACC001')
    print(f"Found: {found_account}")
    assert found_account.account_id == 'ACC001'

    # Test account not found
    try:
        service.get_account('ACC999')
        print("❌ FAIL: Should raise AccountNotFoundError")
    except AccountNotFoundError as e:
        print(f"✓ AccountNotFoundError: {e}")

    print("\n=== Testing Money Transfer ===")
    print(f"Before transfer:")
    print(f"  Alice: ${alice.get_balance()}")
    print(f"  Bob: ${bob.get_balance()}")

    service.transfer('ACC001', 'ACC002', Decimal('100.00'))
    print(f"\nAfter transferring $100 from Alice to Bob:")
    print(f"  Alice: ${alice.get_balance()}")
    print(f"  Bob: ${bob.get_balance()}")

    assert alice.get_balance() == Decimal('900.00')
    assert bob.get_balance() == Decimal('600.00')

    print("\n=== Testing Transfer Validation ===")

    # Test same account transfer
    try:
        service.transfer('ACC001', 'ACC001', Decimal('50.00'))
        print("❌ FAIL: Should raise SameAccountError")
    except SameAccountError as e:
        print(f"✓ SameAccountError: {e}")

    # Test account not found (source)
    try:
        service.transfer('ACC999', 'ACC002', Decimal('50.00'))
        print("❌ FAIL: Should raise AccountNotFoundError")
    except AccountNotFoundError as e:
        print(f"✓ AccountNotFoundError: {e}")

    # Test account not found (destination)
    try:
        service.transfer('ACC001', 'ACC999', Decimal('50.00'))
        print("❌ FAIL: Should raise AccountNotFoundError")
    except AccountNotFoundError as e:
        print(f"✓ AccountNotFoundError: {e}")

    # Test insufficient funds
    try:
        service.transfer('ACC001', 'ACC002', Decimal('10000.00'))
        print("❌ FAIL: Should raise InsufficientFundsError")
    except InsufficientFundsError as e:
        print(f"✓ InsufficientFundsError: {e}")

    # Test negative amount
    try:
        service.transfer('ACC001', 'ACC002', Decimal('-50.00'))
        print("❌ FAIL: Should raise InvalidAmountError")
    except InvalidAmountError as e:
        print(f"✓ InvalidAmountError: {e}")

    # Test zero amount
    try:
        service.transfer('ACC001', 'ACC002', Decimal('0.00'))
        print("❌ FAIL: Should raise InvalidAmountError")
    except InvalidAmountError as e:
        print(f"✓ InvalidAmountError: {e}")

    print("\n=== Testing Money Conservation ===")
    # Total money should never change during transfers!
    total_before = service.get_total_money()
    print(f"Total money before transfers: ${total_before}")

    service.transfer('ACC002', 'ACC003', Decimal('100.00'))
    service.transfer('ACC001', 'ACC003', Decimal('50.00'))

    total_after = service.get_total_money()
    print(f"Total money after transfers: ${total_after}")

    assert total_before == total_after, \
        "Money was created or destroyed during transfer!"
    print("✓ Money is conserved - no money created or destroyed")

    print("\n=== Final Account Balances ===")
    print(f"Alice (ACC001): ${service.get_account('ACC001').get_balance()}")
    print(f"Bob (ACC002): ${service.get_account('ACC002').get_balance()}")
    print(f"Charlie (ACC003): ${service.get_account('ACC003').get_balance()}")
    print(f"Total: ${service.get_total_money()}")

    print("\n=== Complex Transfer Scenario ===")
    # Create a new service for clean test
    service2 = TransferService()
    acc1 = service2.create_account('A', 'Alice', Decimal('1000.00'))
    acc2 = service2.create_account('B', 'Bob', Decimal('0.00'))

    # Transfer in small increments (tests Decimal precision)
    for i in range(100):
        service2.transfer('A', 'B', Decimal('1.01'))

    print(f"After 100 transfers of $1.01:")
    print(f"  Alice: ${acc1.get_balance()}")
    print(f"  Bob: ${acc2.get_balance()}")

    assert acc1.get_balance() == Decimal('899.00')
    assert acc2.get_balance() == Decimal('101.00')
    print("✓ Decimal precision maintained across many operations")

    print("\n✓ All tests passed!")
    print("\nKEY TAKEAWAYS:")
    print("1. Use dictionary for O(1) account lookup")
    print("2. Validate before performing operations")
    print("3. Let Account class handle balance validation")
    print("4. Separation of concerns: Account vs TransferService")
    print("5. Money should be conserved - never created or destroyed")
    print("6. Decimal maintains precision across many operations")
