# Gr4vy Interview Prep - Money Transfer System

## Overview

This folder contains progressive exercises to prepare you for your 40-minute **Gr4vy Python Backend Junior Software Engineer** coding test.

**About Gr4vy:** "No-code" cloud payments orchestration platform. Former PayPal fintech leaders. $27.2M funding. They process money transfers globally - so getting Decimal right is CRITICAL!

**Their Tech Stack:**
- Python ✅
- FastAPI (modern web framework)
- pytest (testing framework)
- SQLAlchemy (database ORM)
- Unit, integration, and acceptance testing

The exercises follow the same teaching style as your CS fundamentals course - each file contains:
- Clear explanations of concepts
- Step-by-step requirements
- Starter code with TODOs
- Comprehensive test cases
- Real-world examples

## What You'll Learn

1. **Decimal for Currency** - Why float fails for money, how to use Decimal correctly
2. **Custom Exceptions** - Creating domain-specific errors for fintech
3. **Account Class** - OOP design for financial accounts
4. **TransferService** - Managing multiple accounts with O(1) lookup
5. **Complete System** - Integration exercise simulating the real test

## Exercise Sequence

### Exercise 1: Decimal Basics (`1_decimal_basics.py`)
**Time: 15-20 minutes**

Learn why `float` is dangerous for money and how to use `Decimal` correctly.

Key concepts:
- Creating Decimal from strings
- Rounding to 2 decimal places with `quantize()`
- Validating currency amounts

```python
from decimal import Decimal, ROUND_HALF_UP

# CORRECT way to handle money
amount = Decimal('10.50')
result = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
```

### Exercise 2: Custom Exceptions (`2_custom_exceptions.py`)
**Time: 20-25 minutes**

Create custom exception classes for a payment system.

Key concepts:
- Exception hierarchy
- Inheriting from `Exception`
- Clear error messages
- Exception handling patterns

```python
class TransferError(Exception):
    """Base exception for all transfer errors"""
    pass

class InsufficientFundsError(TransferError):
    """Raised when account lacks funds"""
    pass
```

### Exercise 3: Account Class (`3_account_class.py`)
**Time: 30-40 minutes**

Build a financial account class with deposits, withdrawals, and validation.

Key concepts:
- Class design with `__init__`
- Instance methods and attributes
- Encapsulation (private `_balance`)
- Using custom exceptions
- Type hints with Decimal

```python
class Account:
    def __init__(self, account_id: str, owner_name: str,
                 initial_balance: Decimal = Decimal('0.00')):
        self._balance = initial_balance

    def deposit(self, amount: Decimal) -> None:
        # Validate and add to balance
```

### Exercise 4: TransferService (`4_transfer_service.py`)
**Time: 40-50 minutes**

Create a service that manages multiple accounts and transfers money between them.

Key concepts:
- Dictionary for O(1) account lookup
- Coordinating operations between objects
- Separation of concerns (SRP)
- Money conservation principle

```python
class TransferService:
    def __init__(self):
        self.accounts: dict[str, Account] = {}

    def transfer(self, from_id: str, to_id: str, amount: Decimal):
        # Lookup accounts, validate, and transfer
```

### Exercise 5: Complete System (`5_complete_system.py`)
**Time: 40 minutes (FULL TEST SIMULATION)**

Put everything together in a working system. Two options:

1. **CLI Version**: Build a command-line interface
2. **Test Suite**: Run automated test scenarios

This simulates the actual test environment!

### Exercise 6: pytest Examples (`6_pytest_examples.py`) ⭐ OPTIONAL
**Time: Study only - for understanding**

Since Gr4vy uses pytest, this file shows you:
- How to write proper pytest tests
- How to test exceptions with `pytest.raises()`
- Best practices for testing

**NOTE:** You probably won't write pytest tests during the 40-min test, but understanding how to write testable code will impress them!

## Recommended Study Path

### Day 1-2: Foundations
1. Complete Exercise 1 (Decimal)
2. Complete Exercise 2 (Exceptions)
3. Review and understand key concepts

### Day 3-4: Core Classes
1. Complete Exercise 3 (Account)
2. Start Exercise 4 (TransferService)
3. Practice until comfortable

### Day 5: Integration & Practice
1. Finish Exercise 4
2. Complete Exercise 5 (40-minute simulation)
3. Time yourself - can you do it in 40 minutes?

### Day 6: Test Day Prep
1. Re-do Exercise 5 from scratch in 40 minutes
2. Review common errors and edge cases
3. Practice explaining your code out loud

## Key Concepts for the Test

### 1. Always Use Decimal for Money
```python
# WRONG
balance = 10.50  # float
total = balance * 3  # 31.49999999999997

# CORRECT
balance = Decimal('10.50')  # Decimal
total = balance * 3  # Decimal('31.50')
```

### 2. Dictionary for O(1) Lookup
```python
# O(1) - Instant lookup
accounts = {'ACC001': account1, 'ACC002': account2}
account = accounts['ACC001']
```

### 3. Custom Exceptions for Clarity
```python
# Instead of generic ValueError
raise InsufficientFundsError(
    f"Account {id} has ${balance} but needs ${amount}"
)
```

### 4. Validation in Constructor and Methods
```python
def __init__(self, account_id: str, balance: Decimal):
    if not account_id:
        raise ValueError("Account ID cannot be empty")
    if balance < Decimal('0.00'):
        raise InvalidAmountError("Balance cannot be negative")
```

### 5. Separation of Concerns
- **Account**: Manages individual account (deposit, withdraw, balance)
- **TransferService**: Manages collection of accounts (lookup, transfer)

## Test Day Strategy

### Time Allocation (40 minutes total)
1. **Read requirements** (3 min)
2. **Plan approach** (2 min)
3. **Implement core classes** (20 min)
   - Account class (10 min)
   - TransferService class (10 min)
4. **Add validation & exceptions** (10 min)
5. **Test and debug** (5 min)

### What to Prioritize
1. ✅ **Must Have**:
   - Account class with deposit/withdraw
   - TransferService with transfer method
   - Decimal for all money
   - Basic validation (no negatives, sufficient funds)

2. ⭐ **Should Have**:
   - Custom exceptions
   - Type hints
   - Good error messages

3. 💡 **Nice to Have**:
   - Docstrings
   - Edge case handling
   - Clean code style

### Common Mistakes to Avoid
❌ Using `float` instead of `Decimal`
❌ Forgetting to validate inputs
❌ Not handling account not found errors
❌ Allowing transfers to the same account
❌ Not checking for sufficient funds before withdrawal

## Quick Reference

### Decimal Operations
```python
from decimal import Decimal, ROUND_HALF_UP

# Create from string (ALWAYS)
amount = Decimal('10.50')

# Round to 2 decimal places
rounded = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Check decimal places
has_two_places = (amount == amount.quantize(Decimal('0.01')))
```

### Exception Pattern
```python
# Define
class MyError(Exception):
    pass

# Raise
raise MyError("Clear error message")

# Catch
try:
    risky_operation()
except MyError as e:
    print(f"Error: {e}")
```

### Type Hints
```python
from decimal import Decimal

def transfer(amount: Decimal) -> None:
    pass

class Account:
    balance: Decimal
```

## Practice Problems

After completing the exercises, try these:

1. **Add transaction history** - Store list of all transactions in Account
2. **Add transaction IDs** - Generate unique ID for each transfer
3. **Add account types** - Different rules for Savings vs Checking
4. **Add transfer limits** - Max amount per transaction
5. **Add daily limits** - Max total transfers per day

## Final Checklist

Before the test, make sure you can:
- [ ] Create Account class with Decimal balance
- [ ] Implement deposit/withdraw with validation
- [ ] Create TransferService with dictionary storage
- [ ] Implement transfer method with all validations
- [ ] Raise custom exceptions for errors
- [ ] Use type hints correctly
- [ ] Write clean, readable code
- [ ] Complete everything in 40 minutes

## Good Luck!

You've got this! The key is:
1. **Use Decimal** - Never float for money
2. **Validate inputs** - Check everything
3. **Clear errors** - Custom exceptions with good messages
4. **Simple OOP** - Account + TransferService
5. **Dictionary lookup** - O(1) performance

Remember: They're testing **fundamentals**, not advanced patterns.
Keep it clean and simple!
