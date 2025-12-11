# Gr4vy Test Cheat Sheet - Quick Reference

## 1. Decimal Import & Usage

```python
from decimal import Decimal

# ✅ CORRECT
balance = Decimal('10.50')
amount = Decimal('5.25')
total = balance + amount  # Decimal('15.75')

# ❌ WRONG
balance = 10.50  # float - NEVER for money!
```

## 2. Account Class Template

```python
from decimal import Decimal

class Account:
    def __init__(self, account_id: str, owner: str,
                 initial_balance: Decimal = Decimal('0.00')) -> None:
        if not account_id:
            raise ValueError("Account ID cannot be empty")
        if initial_balance < Decimal('0.00'):
            raise ValueError("Balance cannot be negative")

        self.account_id = account_id
        self.owner = owner
        self._balance = initial_balance

    def deposit(self, amount: Decimal) -> None:
        if amount <= Decimal('0.00'):
            raise ValueError("Amount must be positive")
        self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= Decimal('0.00'):
            raise ValueError("Amount must be positive")
        if amount > self._balance:
            raise ValueError(
                f"Insufficient funds: has ${self._balance}, needs ${amount}"
            )
        self._balance -= amount

    def get_balance(self) -> Decimal:
        return self._balance
```

## 3. Transfer Function

```python
def transfer(from_account: Account, to_account: Account,
             amount: Decimal) -> None:
    """Transfer money between accounts"""
    if amount <= Decimal('0.00'):
        raise ValueError("Transfer amount must be positive")

    from_account.withdraw(amount)  # This validates sufficient funds
    to_account.deposit(amount)
```

## 4. Common Validations

```python
# String not empty
if not account_id:
    raise ValueError("Account ID cannot be empty")

# Amount positive
if amount <= Decimal('0.00'):
    raise ValueError("Amount must be positive")

# Sufficient funds
if amount > self._balance:
    raise ValueError("Insufficient funds")

# Type checking (if needed)
if not isinstance(amount, Decimal):
    raise TypeError("Amount must be Decimal")
```

## 5. Quick Test Code

```python
if __name__ == "__main__":
    # Create accounts
    alice = Account('A001', 'Alice', Decimal('1000.00'))
    bob = Account('B002', 'Bob', Decimal('500.00'))

    # Test transfer
    print(f"Before: Alice=${alice.get_balance()}, Bob=${bob.get_balance()}")
    transfer(alice, bob, Decimal('100.00'))
    print(f"After: Alice=${alice.get_balance()}, Bob=${bob.get_balance()}")

    # Test error case
    try:
        transfer(bob, alice, Decimal('10000.00'))
        print("❌ Should have raised error")
    except ValueError as e:
        print(f"✓ Correctly raised error: {e}")
```

## 6. Type Hints Quick Reference

```python
from decimal import Decimal

# Function with type hints
def transfer(from_acc: Account, to_acc: Account,
             amount: Decimal) -> None:
    pass

# Class attributes
class Account:
    account_id: str
    owner: str
    _balance: Decimal
```

## 7. Custom Exceptions (If Time)

```python
class InsufficientFundsError(Exception):
    """Raised when account has insufficient funds"""
    pass

# Usage
if amount > self._balance:
    raise InsufficientFundsError(
        f"Account {self.account_id} has ${self._balance} but needs ${amount}"
    )
```

## 8. Dictionary for Account Lookup (If Needed)

```python
class TransferService:
    def __init__(self):
        self.accounts: dict[str, Account] = {}

    def create_account(self, account_id: str, owner: str,
                      balance: Decimal) -> Account:
        if account_id in self.accounts:
            raise ValueError(f"Account {account_id} already exists")

        account = Account(account_id, owner, balance)
        self.accounts[account_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")
        return self.accounts[account_id]

    def transfer(self, from_id: str, to_id: str,
                amount: Decimal) -> None:
        if from_id == to_id:
            raise ValueError("Cannot transfer to same account")

        from_account = self.get_account(from_id)
        to_account = self.get_account(to_id)

        from_account.withdraw(amount)
        to_account.deposit(amount)
```

## 9. Common Mistakes - Quick Check

### ❌ DON'T:
- Use `float` for money
- Forget validation
- Allow negative amounts
- Allow overdrafts
- Use vague error messages

### ✅ DO:
- Use `Decimal` for money
- Validate all inputs
- Raise clear errors
- Test your code
- Use type hints

## 10. Time Management

| Time | Task |
|------|------|
| 0-5 min | Read requirements, plan structure |
| 5-15 min | Write Account class |
| 15-25 min | Write transfer logic |
| 25-35 min | Add validation & error handling |
| 35-40 min | Test and verify |

## 11. Pre-Test Checklist

- [ ] File created
- [ ] `from decimal import Decimal` imported
- [ ] Requirements read twice
- [ ] Core classes identified
- [ ] Ready to start!

## 12. Red Flags to Avoid

❌ `balance = 10.50` - Using float
❌ `self.balance -= amount` - No validation
❌ `raise ValueError("Error")` - Vague message
❌ No test code
❌ No type hints

## 13. Green Flags to Include

✅ `balance = Decimal('10.50')` - Correct type
✅ Input validation in every method
✅ Clear error messages with context
✅ Test code at bottom
✅ Type hints on methods

## Remember:

**CORE FIRST, POLISH LATER**

1. Get basic Account working (15 min)
2. Get basic transfer working (10 min)
3. Add validation (10 min)
4. Test (5 min)

**YOU GOT THIS!** 🚀
