# Gr4vy Interview Strategy - Quick Reference

## About the Role

**Position:** Python Backend Junior Software Engineer
**Company:** Gr4vy - Payments orchestration platform (Former PayPal leaders, $27M funding)
**Test:** 40-minute coding challenge
**Topic:** Moving money from A to B

## What They're Actually Testing

Based on the job description, they want to see:

### 1. Clean Python Code ✅
- Proper variable naming
- Type hints
- Clear function structure
- Following PEP 8 style guide

### 2. Basic OOP ✅
- Can you create classes?
- Can you use `__init__` constructors?
- Can you write instance methods?
- Do you understand encapsulation?

### 3. Money Handling (CRITICAL!) ✅
- **MUST use Decimal, never float**
- This is a payments company - they care deeply about this
- One float error = failed interview

### 4. Error Handling ✅
- Input validation
- Raising appropriate exceptions
- Clear error messages
- Edge case handling

### 5. Testable Code ✅
- Code that can be verified
- Simple assertions to prove it works
- Thinking about edge cases

## The Likely Test Scenario

**Most Probable:**
```
Build a system that can transfer money between accounts.

Requirements:
- Create an Account class that can store a balance
- Implement deposit and withdraw methods
- Implement a transfer function that moves money from account A to account B
- Handle errors (insufficient funds, invalid amounts, etc.)
- Use appropriate data types for currency

You have 40 minutes.
```

**Alternative Scenarios:**
- Payment processing with fees/commissions
- Currency conversion between accounts
- Transaction history tracking
- Multiple transfer types (instant, scheduled)

## Your 40-Minute Game Plan

### Minutes 1-5: READ & PLAN
- [ ] Read requirements carefully twice
- [ ] Identify the classes needed (probably Account, maybe TransferService)
- [ ] List the methods needed
- [ ] Note edge cases mentioned

### Minutes 6-25: IMPLEMENT CORE (20 min)
- [ ] **First 10 min:** Account class
  - Constructor with Decimal balance
  - deposit() method
  - withdraw() method with validation
  - get_balance() method

- [ ] **Next 10 min:** Transfer functionality
  - Either a transfer() function OR TransferService class
  - Validate inputs
  - Perform transfer atomically (withdraw then deposit)

### Minutes 26-35: VALIDATION & ERRORS (10 min)
- [ ] Add all input validation
- [ ] Raise appropriate errors
- [ ] Add helpful error messages
- [ ] Test error cases

### Minutes 36-40: TEST & POLISH (5 min)
- [ ] Run your code
- [ ] Test happy path
- [ ] Test 2-3 error cases
- [ ] Add comments if time permits

## Code Template to Memorize

```python
from decimal import Decimal

class Account:
    def __init__(self, account_id: str, owner: str,
                 initial_balance: Decimal = Decimal('0.00')) -> None:
        # Validate inputs
        if not account_id:
            raise ValueError("Account ID cannot be empty")
        if initial_balance < Decimal('0.00'):
            raise ValueError("Balance cannot be negative")

        self.account_id = account_id
        self.owner = owner
        self._balance = initial_balance

    def deposit(self, amount: Decimal) -> None:
        if amount <= Decimal('0.00'):
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= Decimal('0.00'):
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds: has ${self._balance}, needs ${amount}")
        self._balance -= amount

    def get_balance(self) -> Decimal:
        return self._balance

def transfer(from_account: Account, to_account: Account,
             amount: Decimal) -> None:
    """Transfer money from one account to another"""
    if amount <= Decimal('0.00'):
        raise ValueError("Transfer amount must be positive")

    # Withdraw first (this validates sufficient funds)
    from_account.withdraw(amount)

    # Then deposit
    to_account.deposit(amount)

# Quick test
if __name__ == "__main__":
    alice = Account('A001', 'Alice', Decimal('1000.00'))
    bob = Account('B002', 'Bob', Decimal('500.00'))

    print(f"Before: Alice=${alice.get_balance()}, Bob=${bob.get_balance()}")
    transfer(alice, bob, Decimal('100.00'))
    print(f"After: Alice=${alice.get_balance()}, Bob=${bob.get_balance()}")
```

## Critical Things to Remember

### ✅ MUST DO:
1. **Use Decimal('10.50')** - NEVER `10.50` or `float`
2. **Validate all inputs** - No negative amounts, no empty strings
3. **Type hints** - Show you know modern Python
4. **Test your code** - Run it before submitting!
5. **Clear variable names** - `account_id` not `aid`

### ❌ NEVER DO:
1. Use float for money
2. Allow negative balances
3. Allow withdrawals > balance
4. Forget to validate inputs
5. Leave code untested

## What Makes You Stand Out

### Basic (Everyone Does This):
- Account class exists
- Transfer works
- Code runs

### Good (Shows Competence):
- ✅ Uses Decimal correctly
- ✅ Has input validation
- ✅ Raises clear errors
- ✅ Includes type hints
- ✅ Has test code at bottom

### Excellent (Impresses Them):
- ✅ Clean, readable code structure
- ✅ Docstrings explaining methods
- ✅ Comprehensive error messages
- ✅ Tests multiple scenarios
- ✅ Handles edge cases
- ✅ Comments explaining complex logic

## Common Mistakes to Avoid

### ❌ Mistake #1: Using Float
```python
# WRONG
balance = 10.50  # float
```
```python
# CORRECT
balance = Decimal('10.50')  # Decimal
```

### ❌ Mistake #2: No Validation
```python
# WRONG
def withdraw(self, amount):
    self.balance -= amount  # What if amount > balance?
```
```python
# CORRECT
def withdraw(self, amount: Decimal) -> None:
    if amount <= Decimal('0.00'):
        raise ValueError("Amount must be positive")
    if amount > self._balance:
        raise ValueError("Insufficient funds")
    self._balance -= amount
```

### ❌ Mistake #3: Vague Error Messages
```python
# WRONG
raise ValueError("Invalid")  # Invalid what?
```
```python
# CORRECT
raise ValueError(f"Insufficient funds: account has ${self._balance} but needs ${amount}")
```

### ❌ Mistake #4: No Testing
```python
# WRONG
# Just writing code and submitting without running it
```
```python
# CORRECT
if __name__ == "__main__":
    # Test basic operations
    account = Account('A001', 'Alice', Decimal('100.00'))
    account.deposit(Decimal('50.00'))
    assert account.get_balance() == Decimal('150.00')
    print("✓ Tests passed!")
```

## Questions You Might Ask (If Time Permits)

Good questions show you're thinking beyond the requirements:

1. "Should I handle concurrent transfers?" (Probably no, too complex for 40 min)
2. "Do you want me to track transaction history?" (Only if time permits)
3. "Should amounts have a maximum limit?" (Good thinking, but simple validation is enough)
4. "Would you like me to add fees/commissions?" (Only if mentioned in requirements)

**Best question:** "Should I focus on getting the core working first, then add extras if time permits?"
(Answer is always YES - core functionality first!)

## Day-Before Checklist

- [ ] Re-do Exercise 5 from scratch in 40 minutes
- [ ] Memorize Decimal import and usage
- [ ] Review common validation patterns
- [ ] Practice explaining your code out loud
- [ ] Get good sleep!
- [ ] Have confidence - you've prepared well!

## On Test Day

### Setup (Before Starting):
1. Create a new Python file
2. Add this at the top:
   ```python
   from decimal import Decimal
   ```
3. Take a deep breath!

### During Test:
- Read requirements TWICE
- Start with simplest working version
- Test frequently (run your code every 5 minutes)
- If stuck, move to next part and come back
- Leave 5 minutes for testing

### After Implementing:
- Run the code end-to-end
- Test at least one error case
- Add a comment or two if it helps clarity
- Submit confidently!

## Remember:

**They're hiring a JUNIOR developer.** They expect:
- ✅ Understanding of basics
- ✅ Clean code
- ✅ Proper money handling
- ✅ Good debugging skills

**They DON'T expect:**
- ❌ Perfect architecture
- ❌ Advanced design patterns
- ❌ Production-ready code
- ❌ 100% edge case coverage

**You've got this!** You've practiced the exact scenario. Just stay calm, use Decimal, validate inputs, and test your code.

## Final Pep Talk

You have:
- ✅ Completed your CS fundamentals course (Module 2-3)
- ✅ Learned OOP properly
- ✅ Practiced the exact scenario they'll test
- ✅ Understood Decimal for money handling
- ✅ Studied their tech stack and values

**Confidence is key.** You're prepared. You know this material. Go show Gr4vy what you can do!

Good luck! 🚀
