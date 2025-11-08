# UMPIRE Problem-Solving Worksheet

---

## U - UNDERSTAND

Create a bank account class
User should be able to add money, withdraw money, and see tbe balance as a
string representation

**Inputs:**
in the constructor:
account no -str, account holder name - str, balance -float
deposit and withdraw but take an amount - float
**Outputs:**
total amount in string form via getbalance().
total amount is a float
**Constraints:**

- Account number cannot be empty -ValueError
- Owner name cannot be empty - ValueError: For invalid values
- Initial balance cannot be negative ValueError: For invalid values
- Deposit amount must be positive - ValueError
- Withdrawal amount must be positive - ValueError
- Cannot withdraw more than current balance -ValueError
  **Edge Cases:**
  Exceptions to Raise:
- TypeError: For wrong types

---

## M - MATCH

[What similar problems have you solved? What data structures and techniques apply?]

**Similar Problems:**
**Data Structures:** None
**Patterns/Techniques:**
add or subtract from

---

## P - PLAN

[Write pseudocode and create test cases BEFORE coding]

**Pseudocode:**

```
 BankAccount(account_no: str, owner_name:str, initial_balance: float) -> float:
    constructor
    arguments as instance variables
    but create a new total_balance variable which is initially set to initial_balance
    - Account number cannot be empty -ValueError
    - Owner name cannot be empty - ValueError: For invalid values
    - Initial balance cannot be negative ValueError: For invalid values
    put data validation in the constructor

    deposit(amount)
    amount should be a float - value error
    - Deposit amount must be positive - ValueError
    returns nothing

    withdraw(amount)
    amount should be a float - value error
    returns nothing

    - Withdrawal amount must be positive - ValueError
    - Cannot withdraw more than current balance -ValueError
        if amount > total_balance
            -ValueError

    - get_balance(): Return current balance
      returns total_balance() as a float

    __str__ returns total balance as a string representation
```

**Test Cases:**

```
Test 1 (normal): input → expected output
Test 2 (edge):   input → expected output
Test 3 (error):  input → expected output
```

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

**Time Complexity:** O(**\_) because [explanation]
**Space Complexity:** O(\_**) because [explanation]
**Improvements:** [could you optimize further?]
**Learned:** [what did you learn from this problem?]
