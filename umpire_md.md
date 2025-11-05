# UMPIRE Problem-Solving Worksheet

**Problem Name:** **\*\***\_\_\_\_**\*\*** **Date:** **\*\***\_\_\_\_**\*\***

---

## U - UNDERSTAND

create a calculator app
**Inputs:**
string from 'supported operations', 2 floats
**Outputs:** returns a float
**Constraints:**
inputs must be in given as the specified type
**Edge Cases:**
Dividing by zero should raise ZeroDivisionError

- Raise TypeError if inputs are not numbers
- Raise ValueError if operation is not supported

BONUS CHALLENGE (Optional):
Extend the calculator to support:

- "power" - Exponentiation (a^b)
- "modulo" - Remainder (a % b)
- Handle negative numbers - Python does this

---

## M - MATCH

[What similar problems have you solved? What data structures and techniques apply?]

**Similar Problems:**
simpler fiz buzz
**Data Structures:**
**Patterns/Techniques:**
if statements

---

## P - PLAN

First validate input
operation must be a vaild string
a and b must be instances of a float (this will except an int)

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

**Time Complexity:** O(**\_) because [explanation]
**Space Complexity:** O(\_**) because [explanation]
**Improvements:** [could you optimize further?]
**Learned:** [what did you learn from this problem?]
