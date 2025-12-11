"""
Exercise 6: Writing Tests with pytest (Optional but Impressive!)

INTRODUCTION TO PYTEST:

Gr4vy uses "unit, integration and acceptance tests to drive design."
They specifically list "pytest" as a required skill.

While you might not need to write tests during the 40-minute coding test,
knowing HOW to write testable code is important, and adding a few basic
tests will make your submission stand out!

WHAT IS PYTEST?

pytest is Python's most popular testing framework. It makes writing tests easy:

1. Name test files: test_*.py or *_test.py
2. Name test functions: test_*
3. Use simple assert statements
4. Run with: pytest

BASIC PYTEST EXAMPLE:

# In test_account.py
from decimal import Decimal
from account_class import Account

def test_account_creation():
    account = Account('ACC001', 'Alice', Decimal('100.00'))
    assert account.get_balance() == Decimal('100.00')

def test_deposit():
    account = Account('ACC001', 'Alice', Decimal('100.00'))
    account.deposit(Decimal('50.00'))
    assert account.get_balance() == Decimal('150.00')

TESTING EXCEPTIONS WITH PYTEST:

import pytest

def test_insufficient_funds():
    account = Account('ACC001', 'Alice', Decimal('100.00'))

    # This is how pytest tests exceptions
    with pytest.raises(InsufficientFundsError):
        account.withdraw(Decimal('200.00'))

WHY THIS MATTERS FOR GR4VY:

Gr4vy is a payments platform - bugs cost money (literally!).
They need developers who:
- Write code that's easy to test
- Think about edge cases
- Can verify their code works

Showing you can write basic tests demonstrates:
1. Professional coding habits
2. Understanding of best practices
3. Ability to think about edge cases
4. Familiarity with their tech stack (pytest)

===================================
EXERCISE 6: Writing Basic Tests
===================================

Below are example tests for the Account and TransferService classes.
Study these to understand the pattern.

For the 40-minute test, you probably WON'T write separate test files.
But you SHOULD:
1. Include test code at the bottom of your file (like exercises 1-4)
2. Use clear assertions to verify behavior
3. Test at least one error case

This shows you write testable, professional code!
"""

import pytest
from decimal import Decimal
from account_class import Account
from transfer_service import TransferService
from custom_exceptions import (
    InsufficientFundsError,
    InvalidAmountError,
    AccountNotFoundError,
    SameAccountError
)

# ==========================================
# UNIT TESTS FOR ACCOUNT CLASS
# ==========================================

class TestAccountCreation:
    """Tests for creating accounts"""

    def test_create_account_with_balance(self):
        account = Account('ACC001', 'Alice', Decimal('1000.00'))
        assert account.account_id == 'ACC001'
        assert account.owner_name == 'Alice'
        assert account.get_balance() == Decimal('1000.00')

    def test_create_account_default_balance(self):
        account = Account('ACC002', 'Bob')
        assert account.get_balance() == Decimal('0.00')

    def test_create_account_empty_id_raises_error(self):
        with pytest.raises(ValueError):
            Account('', 'Alice', Decimal('100.00'))

    def test_create_account_negative_balance_raises_error(self):
        with pytest.raises(InvalidAmountError):
            Account('ACC001', 'Alice', Decimal('-100.00'))


class TestAccountDeposit:
    """Tests for deposit functionality"""

    def test_deposit_positive_amount(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        account.deposit(Decimal('50.00'))
        assert account.get_balance() == Decimal('150.00')

    def test_deposit_maintains_decimal_precision(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        account.deposit(Decimal('0.01'))
        account.deposit(Decimal('0.01'))
        assert account.get_balance() == Decimal('100.02')

    def test_deposit_negative_amount_raises_error(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        with pytest.raises(InvalidAmountError):
            account.deposit(Decimal('-50.00'))

    def test_deposit_zero_raises_error(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        with pytest.raises(InvalidAmountError):
            account.deposit(Decimal('0.00'))


class TestAccountWithdraw:
    """Tests for withdrawal functionality"""

    def test_withdraw_positive_amount(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        account.withdraw(Decimal('50.00'))
        assert account.get_balance() == Decimal('50.00')

    def test_withdraw_entire_balance(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        account.withdraw(Decimal('100.00'))
        assert account.get_balance() == Decimal('0.00')

    def test_withdraw_insufficient_funds_raises_error(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        with pytest.raises(InsufficientFundsError):
            account.withdraw(Decimal('200.00'))

    def test_withdraw_negative_amount_raises_error(self):
        account = Account('ACC001', 'Alice', Decimal('100.00'))
        with pytest.raises(InvalidAmountError):
            account.withdraw(Decimal('-50.00'))


# ==========================================
# INTEGRATION TESTS FOR TRANSFER SERVICE
# ==========================================

class TestTransferService:
    """Tests for the complete transfer service"""

    def test_create_and_retrieve_account(self):
        service = TransferService()
        service.create_account('ACC001', 'Alice', Decimal('100.00'))

        account = service.get_account('ACC001')
        assert account.account_id == 'ACC001'
        assert account.get_balance() == Decimal('100.00')

    def test_transfer_between_accounts(self):
        service = TransferService()
        service.create_account('ACC001', 'Alice', Decimal('100.00'))
        service.create_account('ACC002', 'Bob', Decimal('50.00'))

        service.transfer('ACC001', 'ACC002', Decimal('30.00'))

        assert service.get_account('ACC001').get_balance() == Decimal('70.00')
        assert service.get_account('ACC002').get_balance() == Decimal('80.00')

    def test_transfer_conserves_money(self):
        service = TransferService()
        service.create_account('ACC001', 'Alice', Decimal('100.00'))
        service.create_account('ACC002', 'Bob', Decimal('50.00'))

        total_before = service.get_total_money()
        service.transfer('ACC001', 'ACC002', Decimal('30.00'))
        total_after = service.get_total_money()

        assert total_before == total_after

    def test_transfer_to_nonexistent_account_raises_error(self):
        service = TransferService()
        service.create_account('ACC001', 'Alice', Decimal('100.00'))

        with pytest.raises(AccountNotFoundError):
            service.transfer('ACC001', 'ACC999', Decimal('30.00'))

    def test_transfer_to_same_account_raises_error(self):
        service = TransferService()
        service.create_account('ACC001', 'Alice', Decimal('100.00'))

        with pytest.raises(SameAccountError):
            service.transfer('ACC001', 'ACC001', Decimal('30.00'))

    def test_transfer_insufficient_funds_raises_error(self):
        service = TransferService()
        service.create_account('ACC001', 'Alice', Decimal('100.00'))
        service.create_account('ACC002', 'Bob', Decimal('50.00'))

        with pytest.raises(InsufficientFundsError):
            service.transfer('ACC001', 'ACC002', Decimal('200.00'))


# ==========================================
# EDGE CASE TESTS
# ==========================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_transfer_with_decimal_precision(self):
        service = TransferService()
        service.create_account('ACC001', 'Alice', Decimal('100.00'))
        service.create_account('ACC002', 'Bob', Decimal('0.00'))

        # Transfer 100 times 1 cent
        for _ in range(100):
            service.transfer('ACC001', 'ACC002', Decimal('0.01'))

        assert service.get_account('ACC001').get_balance() == Decimal('99.00')
        assert service.get_account('ACC002').get_balance() == Decimal('1.00')

    def test_large_amounts(self):
        service = TransferService()
        large_amount = Decimal('999999999.99')
        service.create_account('ACC001', 'Alice', large_amount)
        service.create_account('ACC002', 'Bob', Decimal('0.00'))

        service.transfer('ACC001', 'ACC002', Decimal('0.01'))

        assert service.get_account('ACC001').get_balance() == \
               Decimal('999999999.98')


# ==========================================
# HOW TO RUN THESE TESTS
# ==========================================

"""
To run these tests:

1. Install pytest:
   pip install pytest

2. Run all tests:
   pytest 6_pytest_examples.py

3. Run with verbose output:
   pytest 6_pytest_examples.py -v

4. Run specific test class:
   pytest 6_pytest_examples.py::TestAccountDeposit

5. Run specific test:
   pytest 6_pytest_examples.py::TestAccountDeposit::test_deposit_positive_amount

EXPECTED OUTPUT:
==================== test session starts ====================
collected 20 items

6_pytest_examples.py::TestAccountCreation::test_create_account_with_balance PASSED
6_pytest_examples.py::TestAccountCreation::test_create_account_default_balance PASSED
...
==================== 20 passed in 0.05s ====================
"""

# ==========================================
# SIMPLIFIED TEST STYLE FOR 40-MIN TEST
# ==========================================

"""
During your 40-minute test, you probably won't use pytest.
Instead, write simple test code at the bottom of your file:

if __name__ == "__main__":
    print("Testing Account Creation...")
    account = Account('ACC001', 'Alice', Decimal('100.00'))
    assert account.get_balance() == Decimal('100.00')
    print("✓ Account created correctly")

    print("Testing Deposit...")
    account.deposit(Decimal('50.00'))
    assert account.get_balance() == Decimal('150.00')
    print("✓ Deposit works correctly")

    print("Testing Withdrawal...")
    account.withdraw(Decimal('30.00'))
    assert account.get_balance() == Decimal('120.00')
    print("✓ Withdrawal works correctly")

    print("Testing Error Handling...")
    try:
        account.withdraw(Decimal('200.00'))
        print("❌ Should have raised InsufficientFundsError")
    except InsufficientFundsError:
        print("✓ Correctly raises InsufficientFundsError")

    print("\nAll tests passed!")

This is simpler, doesn't require pytest, and still shows you test your code!
"""

# ==========================================
# KEY TAKEAWAYS
# ==========================================

"""
1. Gr4vy values testing - show you think about it
2. During 40-min test: simple assertions at bottom of file
3. After getting hired: learn pytest properly
4. Always test:
   - Happy path (normal usage)
   - Error cases (invalid input)
   - Edge cases (boundary conditions)
5. Write code that's EASY to test:
   - Small, focused functions
   - Clear inputs and outputs
   - Avoid hidden state
"""
