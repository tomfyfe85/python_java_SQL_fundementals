# UMPIRE Problem-Solving Worksheet

## U - UNDERSTAND

[Restate the problem in your own words, identify inputs/outputs, constraints, and edge cases]

**Inputs:** [type and description]
**Outputs:** [type and description]
**Constraints:** [list all rules and limitations]
**Edge Cases:** [what could go wrong? boundary conditions?]

---

## M - MATCH

[What similar problems have you solved? What data structures and techniques apply?]

**Similar Problems:**
**Data Structures:** [lists, dicts, strings, sets?]
**Patterns/Techniques:** [iteration, validation, string methods, filtering?]

---

## P - PLAN

[Write pseudocode and create test cases BEFORE coding]

**Pseudocode:**

```
function_name(parameters):
    1. [step]
    2. [step]
    return result
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

**Time Complexity:** O(**_) because [explanation]
**Space Complexity:** O(_**) because [explanation]
**Improvements:** [could you optimize further?]
**Learned:** [what did you learn from this problem?]

REQUIREMENTS:

Class: Account

Attributes:

- account_id (str): Unique account identifier
- owner_name (str): Name of account owner
- balance (Decimal): Current balance (private - use \_balance)

Methods:

- **init**(account_id, owner_name, initial_balance=Decimal('0.00')): Constructor
- deposit(amount: Decimal) -> None: Add money to account
- withdraw(amount: Decimal) -> None: Remove money from account
- get_balance() -> Decimal: Return current balance
- **str**() -> str: Return string representation

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
