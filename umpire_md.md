# UMPIRE Problem-Solving Worksheet

## U - UNDERSTAND

[Restate the problem in your own words, identify inputs/outputs, constraints, and edge cases]

Create a function which validates email address according to the given simple validation rules. It takes a string as an arg. It should return a bool.

**Inputs:** String - represents an email address
**Outputs:** Bool - is the email address valid or not?
**Constraints:**

1. Must contain exactly one '@' symbol
2. Must have at least one character before '@'
3. Must have at least one character after '@'
4. The part after '@' must contain at least one '.'
5. Must have at least one character after the last '.'

**Edge Cases:** -
is_valid_email("invalid") → False (no @)

- is_valid_email("@example.com") → False (nothing before @)
- is_valid_email("user@") → False (nothing after @)
- is_valid_email("user@example") → False (no . after @)
- is_valid_email("user@example.") → False (nothing after .)
- is_valid_email("user@@example.com") → False (multiple @)

---

## M - MATCH

[What similar problems have you solved? What data structures and techniques apply?]

**Similar Problems:**

**Data Structures:** [lists, dicts, strings, sets?]
strings, lists, dictionary

**Patterns/Techniques:** [iteration, validation, string methods, filtering?]
If/else, string indexing, iteration?

---

## P - PLAN

[Write pseudocode and create test cases BEFORE coding]

**Pseudocode:**

```
email_validation_checker(email: string) -> bool:
    1. raise error if not a string
    2. must contain @ only once
    3. @ shouldn't be first or last char
    4. . must not be the last char
    5. . must appear at least once after @
    return result

Raise error if input is not a string
map the email to a dictionary?

2 - use .count(@) to find occurrences of @
3 - find first and last chars. check if they are @
4 - last char shouldnt be . - string[-1] != "."
5 - use hash, hash["."] cant be bigger than hash["]

```

**Test Cases:**

```
Test 1 (normal): 'tomfyfe@gmail.com' → true
Test 2 (edge):   'tomfyfeATgmail.com'→ false
Test 3 (error):   123 → "Please enter a valid string"
```

---

## I - IMPLEMENT

[Write your actual Python code with type hints and docstring]

```python
def function_name(email: string) -> bool:
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
