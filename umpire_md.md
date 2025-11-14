# UMPIRE Problem-Solving Worksheet

---

## U - UNDERSTAND

Build a class that automatically converts Celsius to F initially with the constructor
however, it should be able to covert F to C internally too. 
It should use properties to allow a getter and a setter for each unit of temp.




**Inputs:**
(Value: float - temperature to convert, unit: str - 'C' or 'F'. This is 
the unit that the value should be converted from - 

**Outputs:** when called, each method should return a temp
**Constraints:** unit must be either 'C' or 'F'
Edge:
input temps must not be below absolute zero

---

## M - MATCH

[What similar problems have you solved? What data structures and techniques apply?]
Use conversion methods from the previous module


**Similar Problems:**
**Data Structures:** [lists, dicts, strings, sets?]
use floats as return values. They should be to 2 decimal places
**Patterns/Techniques:** 
getter and setters for celsius and fahrenheit 

Raise value error if values are below ab zero
---

## P - PLAN

[Write pseudocode and create test cases BEFORE coding]

**Pseudocode:**

```
class Temperature(parameters):
    1. constructor
    validation:
    unit can't be empty and must be "F" or "C" - Value error
    
    if elif - value can't be below ab zero for C or F

    must use _celsius to store initial celsius
    
    unit is just so you check the iput

    if 'C' then store value in the instance variable
    elfif 'F' then convert from F to C and store in instance variable 

    write getter and setter for each
    
    

    str method is 'self._celsius (self.fahrenheit)'


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
