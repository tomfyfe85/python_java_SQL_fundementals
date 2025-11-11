# UMPIRE Problem-Solving Worksheet

**Problem Name:** ******\_\_\_\_****** **Date:** ******\_\_\_\_******

---

## U - UNDERSTAND

class to track whether a book is available to checkout from a library

**Inputs:**

- title (str): Book title
- author (str): Book author
- isbn (str): 13-digit ISBN
- available (bool): Whether book is available

**Outputs:** [type and description]

- is_available(): Return availability status - string
- **str**(): Return string representation

**Constraints:**

- Title cannot be empty
- Author cannot be empty
- ISBN must be exactly 13 digits
- Cannot checkout a book that's already checked out
- Cannot return a book that's not checked out

---

## M - MATCH

[What similar problems have you solved? What data structures and techniques apply?]

**Similar Problems:**
**Data Structures:** [lists, dicts, strings, sets?]
**Patterns/Techniques:** [iteration, validation, string methods, filtering?]

---

## P - PLAN

**Pseudocode:**

```
Book:
    __init__(self, title, author, isbn)
    add validation
    - Title cannot be empty
    - Author cannot be empty
    - ISBN must be exactly 13 digits
    self.is_available = True

    checkout(self)
        if not self.is_available:
            raise ValueError
        !self.is_available

    return(self)
        if self.is_available:
            raise ValueError
        !self.is_available

    is_available()
        return self.is_available




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
