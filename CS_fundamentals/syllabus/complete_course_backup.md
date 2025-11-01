# CS Fundamentals: Complete Course Backup
## Full Curriculum with All Lectures, Exercises, and Guidelines

---

# 📋 TABLE OF CONTENTS

1. [Course Overview & Philosophy](#course-overview)
2. [UMPIRE Problem-Solving Method](#umpire-method)
3. [Learning Rules & Guidelines](#learning-rules)
4. [Module 1: Programming Fundamentals & Clean Code](#module-1)
5. [Module 2: Object-Oriented Programming Basics](#module-2)
6. [Module 3: Object-Oriented Programming Advanced](#module-3)
7. [Module 4: SOLID Principles](#module-4)
8. [Module 5: Data Structures](#module-5)
9. [Module 6: Algorithms](#module-6)
10. [Module 7: SQL and Database Design](#module-7)
11. [Module 8: Design Patterns (Gang of Four)](#module-8)
12. [Module 9: Testing and TDD](#module-9)
13. [Final Project: Pizza Restaurant System](#final-project)
14. [Resources & References](#resources)

---

<a name="course-overview"></a>
# 📚 COURSE OVERVIEW

## Course Goals

By the end of this course, you will:
- ✅ Master Object-Oriented Programming in Python
- ✅ Apply SOLID principles to write maintainable code
- ✅ Understand and implement all 23 Gang of Four design patterns
- ✅ Build data structures from scratch
- ✅ Analyze algorithms using Big O notation
- ✅ Design and query relational databases
- ✅ Write comprehensive tests using pytest
- ✅ Think systematically about problems using UMPIRE
- ✅ Debug effectively without relying on AI
- ✅ Build production-quality applications

## Course Philosophy

### The Struggle is the Point
- You will get stuck - that's GOOD
- You will get frustrated - that's NORMAL
- You will struggle - that's LEARNING
- You will solve problems yourself - that's CONFIDENCE

### No AI Shortcuts
This course focuses on building YOUR problem-solving brain. AI tools are powerful but can prevent learning if used too early.

## Duration
- **Fast Track:** 6-8 weeks (if you know Python basics)
- **Standard:** 10-12 weeks (learning from scratch)
- **Thorough:** 12-15 weeks (with deep practice)

## Prerequisites
- Python basics (variables, functions, control flow)
- Willingness to struggle and learn
- 10-15 hours per week commitment

---

<a name="umpire-method"></a>
# 🧠 THE UMPIRE PROBLEM-SOLVING METHOD

This is the systematic approach you'll use for EVERY exercise.

## What is UMPIRE?

**U - Understand**  
**M - Match**  
**P - Plan**  
**I - Implement**  
**R - Review**  
**E - Evaluate**

---

## U - UNDERSTAND

**Goal:** Fully comprehend what the problem is asking.

### Questions to Ask:
- What is the problem asking me to build/solve?
- What are the inputs? (types, constraints, edge cases)
- What are the outputs? (types, format)
- What are the constraints?
- Are there any ambiguities I need to clarify?

### Example:
```
Problem: Create a function to check if a string is a palindrome.

Understanding:
- Input: A string (could be empty, could have spaces)
- Output: Boolean (True if palindrome, False otherwise)
- Constraints: Should it be case-sensitive? Should spaces matter?
- Clarifications needed: "racecar" → True, "A man a plan" → True?
```

---

## M - MATCH

**Goal:** Connect this problem to things you already know.

### Questions to Ask:
- Have I solved something similar before?
- What data structures would work well here?
- What algorithms or techniques apply?
- What patterns do I recognize?

### Common Patterns to Recognize:
- **Input validation** - Check before processing
- **Accumulator** - Build up a result
- **Two pointers** - Work from both ends
- **Hash table lookup** - Fast searching
- **Recursion** - Problem contains smaller versions of itself
- **Divide and conquer** - Break into smaller problems

### Example:
```
Matching for palindrome:
- Similar: I've checked if strings are equal
- Data structure: Just need string indexing
- Technique: Compare characters from both ends (two pointers)
- Pattern: Two-pointer pattern
```

---

## P - PLAN

**Goal:** Design your solution BEFORE writing code.

### Steps:
1. Write pseudocode (plain English, not code)
2. Break problem into sub-problems
3. Identify edge cases
4. Create test cases (with expected outputs)

### Example:
```
Pseudocode for palindrome:
1. Convert string to lowercase
2. Remove spaces
3. Set left pointer at start, right pointer at end
4. While left < right:
   a. If characters don't match, return False
   b. Move left forward, right backward
5. If we get through loop, return True

Edge cases:
- Empty string → True (palindrome by definition)
- Single character → True
- Two characters same → True
- Two characters different → False
- String with spaces → Handle correctly

Test cases:
- is_palindrome("racecar") → True
- is_palindrome("hello") → False
- is_palindrome("") → True
- is_palindrome("A") → True
- is_palindrome("A man a plan a canal Panama") → True
```

---

## I - IMPLEMENT

**Goal:** Write clean, working code.

### Guidelines:
- Start simple, then optimize
- Use meaningful variable names
- Add type hints
- Write docstrings
- Test as you go (don't wait until the end)
- Use print statements to debug

### Example:
```python
def is_palindrome(text: str) -> bool:
    """Check if a string is a palindrome.
    
    Args:
        text: String to check
        
    Returns:
        True if palindrome, False otherwise
    """
    # Remove spaces and convert to lowercase
    cleaned = text.replace(" ", "").lower()
    
    # Two-pointer approach
    left = 0
    right = len(cleaned) - 1
    
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left += 1
        right -= 1
    
    return True
```

---

## R - REVIEW

**Goal:** Verify your solution works correctly.

### Checklist:
- [ ] Does it pass all test cases?
- [ ] Did I handle all edge cases?
- [ ] Are there any bugs?
- [ ] Does it work for unexpected inputs?
- [ ] Can I trace through the logic step-by-step?

### Debugging Strategies:
1. **Print debugging** - Add print statements
2. **Test small inputs** - Try simplest cases first
3. **Trace execution** - Walk through line by line
4. **Check assumptions** - Verify what you think is happening
5. **Rubber duck** - Explain code to yourself out loud

---

## E - EVALUATE

**Goal:** Assess the quality and efficiency of your solution.

### Questions:
- **Time Complexity:** How does runtime scale with input size? O(?)
- **Space Complexity:** How much memory does it use? O(?)
- **Code Quality:** Is it readable? Maintainable? Following conventions?
- **Optimizations:** Could it be improved?
- **Trade-offs:** What did you optimize for? What did you sacrifice?

### Example:
```
Evaluation for palindrome:

Time Complexity: O(n) where n is string length
- We check each character once
- String cleaning is O(n)

Space Complexity: O(n)
- We create a cleaned copy of the string
- Could optimize to O(1) by checking in place

Code Quality:
- Clear variable names ✓
- Type hints ✓
- Docstring ✓
- Handles edge cases ✓

Possible optimization:
- Could check without creating cleaned string
- Would be O(1) space but more complex logic
- Current solution prioritizes readability
```

---

## UMPIRE Submission Template

Use this for every exercise:

```markdown
## U - UNDERSTAND

**Problem Restatement:**
[Explain in your own words]

**Inputs:**
- Input 1: [type, description, constraints]
- Input 2: [type, description, constraints]

**Outputs:**
- [type, description, format]

**Constraints:**
- [List all constraints]

**Questions/Clarifications:**
- [Any unclear parts?]

---

## M - MATCH

**Similar problems I've solved:**
- [List any similar problems]

**Data structures needed:**
- [Which data structures fit this problem?]

**Algorithms/techniques needed:**
- [What approaches could work?]

**Patterns that might apply:**
- [Any recognizable patterns?]

---

## P - PLAN

**Pseudocode:**
```
function_name(parameters):
    1. [First step]
    2. [Second step]
    3. [etc.]
```

**Sub-problems:**
1. [Break down into smaller pieces]
2. [What needs to be solved first?]

**Edge cases:**
- [What could go wrong?]
- [What are boundary conditions?]

**Test cases:**
```
Test 1: input → expected output
Test 2: input → expected output
Test 3: edge_case → expected output
```

---

## I - IMPLEMENT

[Your Python code here with type hints and docstrings]

---

## R - REVIEW

**Does it pass all tests?** [Yes/No]

**Bugs found and fixed:**
- [List any bugs you encountered]

**Edge cases handled:**
- [Which edge cases did you address?]

---

## E - EVALUATE

**Time Complexity:** O(?)
**Space Complexity:** O(?)

**Code Quality:**
- Readability: [assessment]
- Follows conventions: [yes/no]
- Well-documented: [yes/no]

**Possible Optimizations:**
- [How could this be improved?]

**Trade-offs:**
- [What did you optimize for?]
```

---

<a name="learning-rules"></a>
# 📖 LEARNING RULES & GUIDELINES

## The Rules

### ✅ ALLOWED:
1. **Google documentation** - Python docs, library references
2. **Google concepts** - "What is polymorphism?", "How does hashing work?"
3. **Google algorithms** - "How does binary search work?"
4. **Read Stack Overflow** - Understand approaches, don't copy code
5. **Official tutorials** - Python.org, Real Python
6. **Draw diagrams** - Visualize the problem
7. **Use print statements** - Debug your code
8. **Ask for hints** - "Should I check type first or value first?"

### ❌ NOT ALLOWED:
1. **AI code generation** - ChatGPT, Copilot, Claude for code
2. **Copying code directly** - Even from Stack Overflow
3. **Looking at solutions first** - Spoils the learning
4. **Asking AI to solve problems** - Defeats the purpose
5. **Using libraries that do it for you** - Build from scratch first

---

## When You Get Stuck

### The Debugging Process:

**Step 1: Read the Error Message**
- What does it say?
- What line is it pointing to?
- What type of error is it?

**Step 2: Add Print Statements**
```python
print(f"Input value: {value}")
print(f"After processing: {result}")
print(f"Type: {type(variable)}")
```

**Step 3: Test with Simple Input**
- Use the simplest possible case
- Does it work for that?
- If not, why not?

**Step 4: Check Your Assumptions**
- What do you THINK is happening?
- Add prints to verify
- Is it what you expected?

**Step 5: Trace Through Line by Line**
- Pretend you're the computer
- What's the value of each variable at each step?
- Where does it go wrong?

**Step 6: Take a Break**
- Walk away for 10 minutes
- Come back with fresh eyes
- Often you'll see the issue immediately

**Step 7: Ask for a Hint**
- Explain what you've tried
- Show your debugging attempts
- Ask specific questions

---

## Asking Good Questions

### ❌ Bad Question:
"My code doesn't work, can you fix it?"

### ✅ Good Question:
"I'm trying to validate if the input is a number. I'm using `type(x) == float` but it's not catching integers. I've tried printing the type and it shows `<class 'int'>`. Should I be checking for both int and float?"

### Question Template:
```
1. What I'm trying to do: [goal]
2. What I've tried: [your attempts]
3. What's happening: [actual behavior]
4. What I expected: [expected behavior]
5. Specific question: [what you need help with]
```

---

## Code Quality Standards

### Always Include:

**1. Type Hints**
```python
def calculate_area(width: float, height: float) -> float:
    return width * height
```

**2. Docstrings**
```python
def calculate_area(width: float, height: float) -> float:
    """Calculate the area of a rectangle.
    
    Args:
        width: Width of the rectangle
        height: Height of the rectangle
        
    Returns:
        Area of the rectangle
    """
    return width * height
```

**3. Meaningful Names**
```python
# ❌ Bad
def calc(x, y):
    return x * y

# ✅ Good
def calculate_rectangle_area(width: float, height: float) -> float:
    return width * height
```

**4. Error Handling**
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**5. Input Validation**
```python
def process_age(age: int) -> str:
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")
    if age < 0 or age > 150:
        raise ValueError("Age must be between 0 and 150")
    return f"Age: {age}"
```

---

## Python Style Guidelines (PEP 8)

### Naming Conventions:
```python
# Variables and functions: snake_case
user_name = "Alice"
total_price = 100.50

def calculate_discount(price: float) -> float:
    return price * 0.1

# Constants: UPPER_SNAKE_CASE
MAX_USERS = 100
DEFAULT_TIMEOUT = 30
PI = 3.14159

# Classes: PascalCase
class BankAccount:
    pass

class UserProfile:
    pass
```

### Spacing:
```python
# Two blank lines between top-level functions/classes
def function_one():
    pass


def function_two():
    pass


class MyClass:
    pass
```

### Line Length:
- Maximum 79 characters per line
- Break long lines logically

---

<a name="module-1"></a>
# MODULE 1: Programming Fundamentals & Clean Code

**Duration:** 1-2 weeks  
**Focus:** Clean code principles, functions, validation

---

## Lecture 1.1: Functions and Clean Code

### Core Principles

#### 1. Functions Should Do ONE Thing

A function should have a single, well-defined responsibility.

**❌ Bad Example:**
```python
def process_user(name, email):
    # Does too many things!
    # 1. Validates email
    if "@" not in email:
        return False
    # 2. Saves to database
    save_to_db(name, email)
    # 3. Sends email
    send_email(email, "Welcome!")
    return True
```

**✅ Good Example:**
```python
def is_valid_email(email: str) -> bool:
    """Check if email format is valid."""
    return "@" in email and "." in email.split("@")[1]

def save_user(name: str, email: str) -> None:
    """Save user to database."""
    save_to_db(name, email)

def send_welcome_email(email: str) -> None:
    """Send welcome email to user."""
    send_email(email, "Welcome!")

def process_user(name: str, email: str) -> bool:
    """Process new user registration."""
    if not is_valid_email(email):
        return False
    save_user(name, email)
    send_welcome_email(email)
    return True
```

**Why is this better?**
- Each function has ONE job
- Easy to test individually
- Easy to understand
- Easy to reuse
- Easy to modify

---

#### 2. Meaningful Names

Names should reveal intent.

**❌ Bad:**
```python
def calc(x, y):
    return x * y

def process(data):
    result = []
    for d in data:
        if d > 0:
            result.append(d * 2)
    return result

n = 5
t = 10
p = n * t
```

**✅ Good:**
```python
def calculate_rectangle_area(width: float, height: float) -> float:
    return width * height

def double_positive_numbers(numbers: list[int]) -> list[int]:
    doubled_numbers = []
    for number in numbers:
        if number > 0:
            doubled_numbers.append(number * 2)
    return doubled_numbers

quantity = 5
price_per_item = 10
total_price = quantity * price_per_item
```

**Naming Guidelines:**
- Use full words, not abbreviations (unless very common like `id`)
- Be specific: `user_email` not just `email`
- Booleans should sound like questions: `is_valid`, `has_permission`
- Functions should be verbs: `calculate_`, `get_`, `validate_`

---

#### 3. Type Hints Are Mandatory

Always use type hints in Python 3.5+.

**✅ Always do this:**
```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price.
    
    Args:
        price: Original price
        discount_percent: Discount as percentage (0-100)
    
    Returns:
        Discounted price
    """
    return price * (1 - discount_percent / 100)

def process_names(names: list[str]) -> dict[str, int]:
    """Count characters in each name.
    
    Args:
        names: List of names to process
        
    Returns:
        Dictionary mapping names to character counts
    """
    return {name: len(name) for name in names}
```

**Benefits:**
- Self-documenting code
- Catch type errors early
- IDE autocomplete works better
- Easier to understand function contracts

---

#### 4. DRY - Don't Repeat Yourself

If you write the same code twice, make it a function.

**❌ Bad - Repetition:**
```python
# Calculate area of rectangle 1
width1 = 5
height1 = 10
area1 = width1 * height1

# Calculate area of rectangle 2
width2 = 3
height2 = 7
area2 = width2 * height2

# Calculate area of rectangle 3
width3 = 8
height3 = 4
area3 = width3 * height3
```

**✅ Good - Function:**
```python
def calculate_area(width: float, height: float) -> float:
    """Calculate rectangle area."""
    return width * height

area1 = calculate_area(5, 10)
area2 = calculate_area(3, 7)
area3 = calculate_area(8, 4)
```

---

#### 5. Magic Numbers Should Be Constants

Don't use unexplained numbers in your code.

**❌ Bad:**
```python
def calculate_discount(price):
    return price * 0.15  # What is 0.15?

def calculate_tax(price):
    return price * 0.08  # What is 0.08?
```

**✅ Good:**
```python
STANDARD_DISCOUNT_RATE = 0.15
SALES_TAX_RATE = 0.08

def calculate_discount(price: float) -> float:
    """Apply standard discount to price."""
    return price * STANDARD_DISCOUNT_RATE

def calculate_tax(price: float) -> float:
    """Calculate sales tax on price."""
    return price * SALES_TAX_RATE
```

---

#### 6. Error Handling

Handle errors appropriately with exceptions.

**Types of Exceptions:**
- `TypeError` - Wrong type (string instead of int)
- `ValueError` - Right type, wrong value (negative age)
- `KeyError` - Key not in dictionary
- `IndexError` - Index out of range
- `FileNotFoundError` - File doesn't exist

**Example:**
```python
def divide(a: float, b: float) -> float:
    """Divide two numbers.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Result of division
        
    Raises:
        TypeError: If inputs are not numbers
        ValueError: If denominator is zero
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    
    if b == 0:
        raise ValueError("Cannot divide by zero")
    
    return a / b
```

---

## Exercise 1.1: Temperature Converter with Validation

### Problem Statement

Create two functions to convert temperatures between Celsius and Fahrenheit with proper input validation.

### Requirements

**Function 1: celsius_to_fahrenheit**
- **Input:** Temperature in Celsius (int or float)
- **Output:** Temperature in Fahrenheit (float)
- **Validation:**
  - Must raise `TypeError` if input is not a number
  - Must raise `ValueError` if temperature is below absolute zero (-273.15°C)

**Function 2: fahrenheit_to_celsius**
- **Input:** Temperature in Fahrenheit (int or float)
- **Output:** Temperature in Celsius (float)
- **Validation:**
  - Must raise `TypeError` if input is not a number
  - Must raise `ValueError` if temperature is below absolute zero (-459.67°F)

### Formulas

```
Celsius to Fahrenheit: F = (C × 9/5) + 32
Fahrenheit to Celsius: C = (F - 32) × 5/9
```

### Constants

```python
ABSOLUTE_ZERO_CELSIUS = -273.15
ABSOLUTE_ZERO_FAHRENHEIT = -459.67
```

### Example Usage

```python
# Valid conversions
result = celsius_to_fahrenheit(0)  # 32.0
result = celsius_to_fahrenheit(100)  # 212.0
result = fahrenheit_to_celsius(32)  # 0.0
result = fahrenheit_to_celsius(212)  # 100.0

# Edge cases
result = celsius_to_fahrenheit(-273.15)  # -459.67 (absolute zero, valid)

# Should raise TypeError
celsius_to_fahrenheit("hot")  # TypeError
celsius_to_fahrenheit(None)  # TypeError
celsius_to_fahrenheit([100])  # TypeError

# Should raise ValueError
celsius_to_fahrenheit(-300)  # ValueError (below absolute zero)
fahrenheit_to_celsius(-500)  # ValueError (below absolute zero)
```

### Your Task

Complete the UMPIRE analysis following the template provided in the UMPIRE section.

---

## Exercise 1.2: Refactoring Practice

### Problem Statement

Refactor the following poorly written code to follow clean code principles.

### Bad Code:

```python
def f(x, y, z):
    a = x + y
    b = a * z
    if b > 100:
        return b - 10
    else:
        return b

def proc(data):
    r = []
    for d in data:
        if d > 0:
            r.append(d * 2)
    return r

x = 50
y = 30
result = x * 0.15
print(result)
```

### Your Task

Rewrite this code with:
1. Meaningful function and variable names
2. Type hints
3. Docstrings
4. Constants instead of magic numbers
5. Clear logic

---

## Exercise 1.3: Email Validator

### Problem Statement

Write a function that validates email addresses according to simple rules.

### Requirements

Create a function `is_valid_email(email: str) -> bool` that returns `True` if the email is valid, `False` otherwise.

**Validation Rules:**
1. Must contain exactly one `@` symbol
2. Must have at least one character before `@`
3. Must have at least one character after `@`
4. The part after `@` must contain at least one `.`
5. Must have at least one character after the last `.`

### Examples

```python
is_valid_email("user@example.com")  # True
is_valid_email("alice@company.co.uk")  # True
is_valid_email("invalid")  # False (no @)
is_valid_email("@example.com")  # False (nothing before @)
is_valid_email("user@")  # False (nothing after @)
is_valid_email("user@example")  # False (no . after @)
is_valid_email("user@example.")  # False (nothing after .)
```

### Your Task

Use the UMPIRE method to solve this problem.

---

## Challenge 1.1: Calculator with Error Handling

### Problem Statement

Build a calculator that performs basic arithmetic operations with comprehensive error handling.

### Requirements

Create a function `calculate(operation: str, a: float, b: float) -> float`

**Supported Operations:**
- `"add"` - Addition
- `"subtract"` - Subtraction
- `"multiply"` - Multiplication
- `"divide"` - Division

**Error Handling:**
- Raise `TypeError` if inputs are not numbers
- Raise `ValueError` if operation is not supported
- Raise `ZeroDivisionError` if dividing by zero

### Examples

```python
calculate("add", 5, 3)  # 8.0
calculate("subtract", 10, 4)  # 6.0
calculate("multiply", 6, 7)  # 42.0
calculate("divide", 15, 3)  # 5.0

calculate("divide", 10, 0)  # ZeroDivisionError
calculate("power", 2, 3)  # ValueError (unsupported operation)
calculate("add", "5", 3)  # TypeError
```

### Bonus Challenge

Extend the calculator to support:
- `"power"` - Exponentiation (a^b)
- `"modulo"` - Remainder (a % b)
- Handle negative numbers correctly

---

<a name="module-2"></a>
# MODULE 2: Object-Oriented Programming Basics

**Duration:** 1-2 weeks  
**Focus:** Classes, objects, encapsulation, constructors

---

## Lecture 2.1: Introduction to Classes and Objects

### What is Object-Oriented Programming?

**OOP is a programming paradigm based on the concept of "objects"** - data structures that contain:
- **Data** (attributes/properties)
- **Behavior** (methods/functions)

### Real-World Analogy

Think of a **blueprint for a house**:
- The **blueprint** (class) describes what a house should have
- An actual **house** (object) is built from that blueprint
- You can build many houses from the same blueprint

```python
# Class = Blueprint
class House:
    def __init__(self, address, rooms):
        self.address = address
        self.rooms = rooms

# Objects = Actual houses built from blueprint
house1 = House("123 Main St", 3)
house2 = House("456 Oak Ave", 4)
```

---

### Key Concepts

#### 1. Class

A **class** is a template/blueprint for creating objects.

```python
class Dog:
    """A class representing a dog."""
    pass  # Empty class for now
```

#### 2. Object (Instance)

An **object** is a specific instance of a class.

```python
# Creating objects from the Dog class
my_dog = Dog()
your_dog = Dog()

# These are different objects from the same class
print(my_dog is your_dog)  # False
```

#### 3. Attributes (Data)

**Attributes** are variables that belong to an object.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name  # attribute
        self.age = age    # attribute

buddy = Dog("Buddy", 3)
print(buddy.name)  # "Buddy"
print(buddy.age)   # 3
```

#### 4. Methods (Behavior)

**Methods** are functions that belong to a class.

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def bark(self):
        """Make the dog bark."""
        return f"{self.name} says Woof!"
    
    def have_birthday(self):
        """Increment dog's age."""
        self.age += 1

buddy = Dog("Buddy", 3)
print(buddy.bark())  # "Buddy says Woof!"
buddy.have_birthday()
print(buddy.age)  # 4
```

---

### The `self` Parameter

**`self` represents the instance of the class.**

```python
class Counter:
    def __init__(self):
        self.count = 0  # This counter's count
    
    def increment(self):
        self.count += 1  # Increment THIS counter's count

counter1 = Counter()
counter2 = Counter()

counter1.increment()
counter1.increment()

print(counter1.count)  # 2
print(counter2.count)  # 0 (different object!)
```

**Key Points:**
- `self` is always the first parameter in methods
- Python automatically passes it
- You don't include it when calling methods

```python
# Python does this automatically:
counter1.increment()  # Python calls: Counter.increment(counter1)
```

---

## Lecture 2.2: Constructors and Initialization

### The `__init__` Method

The **constructor** (`__init__`) is called when creating a new object.

```python
class BankAccount:
    def __init__(self, account_number: str, initial_balance: float):
        """Initialize a new bank account.
        
        Args:
            account_number: Unique account identifier
            initial_balance: Starting balance
        """
        self.account_number = account_number
        self.balance = initial_balance
        print(f"Account {account_number} created with balance ${initial_balance}")

# When you create an object, __init__ is called
account = BankAccount("12345", 1000.0)
# Output: Account 12345 created with balance $1000.0
```

### Instance Variables

**Instance variables** are unique to each object.

```python
class Student:
    def __init__(self, name: str, student_id: str):
        self.name = name
        self.student_id = student_id
        self.grades = []  # Each student has their own grades list

alice = Student("Alice", "S001")
bob = Student("Bob", "S002")

alice.grades.append(95)
bob.grades.append(87)

print(alice.grades)  # [95]
print(bob.grades)    # [87] - Different list!
```

### Default Parameters

You can provide default values in the constructor.

```python
class Rectangle:
    def __init__(self, width: float = 1.0, height: float = 1.0):
        """Create a rectangle.
        
        Args:
            width: Width of rectangle (default 1.0)
            height: Height of rectangle (default 1.0)
        """
        self.width = width
        self.height = height

# Different ways to create rectangles
rect1 = Rectangle()           # 1.0 x 1.0
rect2 = Rectangle(5.0)        # 5.0 x 1.0
rect3 = Rectangle(5.0, 3.0)   # 5.0 x 3.0
```

### Validation in Constructor

**Always validate inputs in the constructor!**

```python
class BankAccount:
    def __init__(self, account_number: str, initial_balance: float):
        # Validate inputs
        if not isinstance(account_number, str):
            raise TypeError("Account number must be a string")
        if not account_number:
            raise ValueError("Account number cannot be empty")
        if not isinstance(initial_balance, (int, float)):
            raise TypeError("Balance must be a number")
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self.account_number = account_number
        self.balance = initial_balance
```

---

## Lecture 2.3: Encapsulation and Privacy

### What is Encapsulation?

**Encapsulation** means:
1. Bundling data and methods together
2. Hiding internal implementation details
3. Controlling access to data

**Why?**
- Prevent invalid states
- Allow changing implementation without breaking external code
- Provide clear interface

### Private Attributes in Python

Python uses **naming conventions** for privacy:

```python
class BankAccount:
    def __init__(self, account_number: str, balance: float):
        self.account_number = account_number  # Public
        self._balance = balance               # "Private" (by convention)
    
    def get_balance(self) -> float:
        """Get current balance."""
        return self._balance
    
    def deposit(self, amount: float) -> None:
        """Deposit money."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
    
    def withdraw(self, amount: float) -> None:
        """Withdraw money."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

# Usage
account = BankAccount("12345", 1000.0)

# ✅ Good - use methods
account.deposit(500.0)
print(account.get_balance())  # 1500.0

# ❌ Bad - direct access (but not prevented in Python)
account._balance = 999999  # Don't do this!
```

**Convention:**
- `attribute` - Public (anyone can access)
- `_attribute` - Private (internal use only, please don't touch)
- `__attribute` - Name mangling (very private)

### Property Decorators

**Better way to control access:**

```python
class BankAccount:
    def __init__(self, account_number: str, balance: float):
        self.account_number = account_number
        self._balance = balance
    
    @property
    def balance(self) -> float:
        """Get balance (read-only)."""
        return self._balance
    
    def deposit(self, amount: float) -> None:
        """Deposit money."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount

# Usage
account = BankAccount("12345", 1000.0)

# ✅ Can read balance like an attribute
print(account.balance)  # 1000.0

# ❌ Cannot set it directly
account.balance = 5000  # AttributeError: can't set attribute

# ✅ Must use methods
account.deposit(500.0)
```

### Getter and Setter Pattern

```python
class Person:
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age
    
    @property
    def name(self) -> str:
        """Get person's name."""
        return self._name
    
    @property
    def age(self) -> int:
        """Get person's age."""
        return self._age
    
    @age.setter
    def age(self, value: int) -> None:
        """Set person's age with validation."""
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be between 0 and 150")
        self._age = value

# Usage
person = Person("Alice", 25)

# ✅ Can read
print(person.name)  # "Alice"
print(person.age)   # 25

# ✅ Can set age (with validation)
person.age = 26  # OK

# ❌ Invalid values caught
person.age = -5  # ValueError
person.age = "thirty"  # TypeError
```

---

## Lecture 2.4: String Representation

### The `__str__` Method

**`__str__`** defines what `print()` shows.

```python
class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"'{self.title}' by {self.author} ({self.pages} pages)"

book = Book("1984", "George Orwell", 328)
print(book)  # '1984' by George Orwell (328 pages)
```

### The `__repr__` Method

**`__repr__`** defines the "official" string representation (for debugging).

```python
class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages
    
    def __str__(self) -> str:
        """For end users."""
        return f"'{self.title}' by {self.author}"
    
    def __repr__(self) -> str:
        """For developers (should be unambiguous)."""
        return f"Book(title='{self.title}', author='{self.author}', pages={self.pages})"

book = Book("1984", "George Orwell", 328)

print(str(book))   # '1984' by George Orwell
print(repr(book))  # Book(title='1984', author='George Orwell', pages=328)

# In Python console
>>> book
Book(title='1984', author='George Orwell', pages=328)
```

**Rule of thumb:**
- `__str__`: Nice, readable output for users
- `__repr__`: Unambiguous, debugging-friendly output for developers

---

## Exercise 2.1: Bank Account Class

### Problem Statement

Create a `BankAccount` class that manages a simple bank account with deposits, withdrawals, and balance tracking.

### Requirements

**Class: BankAccount**

**Attributes:**
- `account_number` (str): Unique account identifier
- `owner_name` (str): Name of account owner
- `balance` (float): Current balance (private)

**Methods:**
- `__init__(account_number, owner_name, initial_balance=0.0)`: Constructor
- `deposit(amount)`: Add money to account
- `withdraw(amount)`: Remove money from account
- `get_balance()`: Return current balance
- `__str__()`: Return string representation

**Validation Rules:**
- Account number cannot be empty
- Owner name cannot be empty
- Initial balance cannot be negative
- Deposit amount must be positive
- Withdrawal amount must be positive
- Cannot withdraw more than current balance

**Exceptions to Raise:**
- `TypeError`: For wrong types
- `ValueError`: For invalid values

### Examples

```python
# Create account
account = BankAccount("ACC001", "Alice Smith", 1000.0)
print(account)  # Account ACC001 (Alice Smith): Balance $1000.00

# Deposit money
account.deposit(500.0)
print(account.get_balance())  # 1500.0

# Withdraw money
account.withdraw(200.0)
print(account.get_balance())  # 1300.0

# Error handling
account.withdraw(2000.0)  # ValueError: Insufficient funds
account.deposit(-100.0)   # ValueError: Deposit amount must be positive
```

### Your Task

Use UMPIRE to design and implement this class.

---

## Exercise 2.2: Book Class

### Problem Statement

Create a `Book` class for a library system with checkout and return functionality.

### Requirements

**Class: Book**

**Attributes:**
- `title` (str): Book title
- `author` (str): Book author
- `isbn` (str): 13-digit ISBN
- `available` (bool): Whether book is available

**Methods:**
- `__init__(title, author, isbn)`: Constructor (book starts as available)
- `checkout()`: Mark book as checked out
- `return_book()`: Mark book as returned
- `is_available()`: Return availability status
- `__str__()`: Return string representation

**Validation Rules:**
- Title cannot be empty
- Author cannot be empty
- ISBN must be exactly 13 digits
- Cannot checkout a book that's already checked out
- Cannot return a book that's not checked out

### Examples

```python
book = Book("1984", "George Orwell", "9780451524935")
print(book)  # '1984' by George Orwell [Available]

book.checkout()
print(book.is_available())  # False
print(book)  # '1984' by George Orwell [Checked Out]

book.checkout()  # ValueError: Book is already checked out

book.return_book()
print(book.is_available())  # True
```

### Your Task

Use UMPIRE to implement this class with all validations.

---

## Exercise 2.3: Enhanced Temperature Class

### Problem Statement

Create a `Temperature` class that stores a temperature and provides automatic conversion between units.

### Requirements

**Class: Temperature**

**Attributes:**
- Store temperature internally in Celsius

**Methods:**
- `__init__(value, unit='C')`: Constructor accepting value and unit ('C' or 'F')
- `celsius` property: Get/set temperature in Celsius
- `fahrenheit` property: Get/set temperature in Fahrenheit
- `__str__()`: Return formatted string

**Validation:**
- Temperature cannot be below absolute zero
- Unit must be 'C' or 'F'

### Examples

```python
# Create from Celsius
temp1 = Temperature(25, 'C')
print(temp1.celsius)     # 25.0
print(temp1.fahrenheit)  # 77.0

# Create from Fahrenheit
temp2 = Temperature(68, 'F')
print(temp2.celsius)     # 20.0
print(temp2.fahrenheit)  # 68.0

# Set via property
temp1.fahrenheit = 32
print(temp1.celsius)     # 0.0

# String representation
print(temp1)  # 0.0°C (32.0°F)

# Validation
temp3 = Temperature(-300, 'C')  # ValueError: Below absolute zero
```

### Your Task

Implement with properties for automatic conversion.

---

## Challenge 2.1: Shopping Cart System

### Problem Statement

Create a shopping cart system with products and a cart that calculates totals.

### Requirements

**Class 1: Product**
- Attributes: name, price, category
- Validation: price must be positive
- `__str__()` method

**Class 2: ShoppingCart**
- Can add products
- Can remove products
- Calculate subtotal
- Calculate tax (8%)
- Calculate total
- Display cart contents

### Examples

```python
# Create products
apple = Product("Apple", 0.99, "Fruit")
banana = Product("Banana", 0.59, "Fruit")
bread = Product("Bread", 2.99, "Bakery")

# Create cart
cart = ShoppingCart()
cart.add_product(apple, quantity=5)
cart.add_product(banana, quantity=3)
cart.add_product(bread, quantity=1)

print(cart.get_subtotal())  # Calculate
print(cart.get_tax())       # Calculate
print(cart.get_total())     # Calculate

print(cart)  # Display cart contents
```

### Your Task

Design and implement both classes with proper encapsulation.

---

<a name="module-3"></a>
# MODULE 3: Object-Oriented Programming Advanced

**Duration:** 1-2 weeks  
**Focus:** Inheritance, composition, polymorphism, abstract classes

---

## Lecture 3.1: Inheritance

### What is Inheritance?

**Inheritance** allows a class to inherit attributes and methods from another class.

**Key Terms:**
- **Parent class** (superclass, base class): The class being inherited from
- **Child class** (subclass, derived class): The class inheriting

**Real-world analogy:** Animals
- All animals eat and sleep
- But dogs bark, cats meow, birds fly
- "Dog IS-A Animal"

### Basic Inheritance

```python
class Animal:
    """Base class for all animals."""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def eat(self) -> str:
        return f"{self.name} is eating"
    
    def sleep(self) -> str:
        return f"{self.name} is sleeping"


class Dog(Animal):  # Dog inherits from Animal
    """A dog is an animal that can bark."""
    
    def bark(self) -> str:
        return f"{self.name} says Woof!"


class Cat(Animal):  # Cat inherits from Animal
    """A cat is an animal that can meow."""
    
    def meow(self) -> str:
        return f"{self.name} says Meow!"


# Usage
dog = Dog("Buddy", 3)
cat = Cat("Whiskers", 5)

# Both have inherited methods
print(dog.eat())    # "Buddy is eating"
print(cat.sleep())  # "Whiskers is sleeping"

# Each has their own methods
print(dog.bark())   # "Buddy says Woof!"
print(cat.meow())   # "Whiskers says Meow!"
```

### The `super()` Function

**`super()`** calls methods from the parent class.

```python
class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        print(f"Animal {name} created")


class Dog(Animal):
    def __init__(self, name: str, age: int, breed: str):
        super().__init__(name, age)  # Call parent constructor
        self.breed = breed
        print(f"Dog breed: {breed}")


dog = Dog("Buddy", 3, "Golden Retriever")
# Output:
# Animal Buddy created
# Dog breed: Golden Retriever

print(dog.name)   # "Buddy" (from Animal)
print(dog.breed)  # "Golden Retriever" (from Dog)
```

### Method Overriding

**Child classes can override parent methods.**

```python
class Animal:
    def make_sound(self) -> str:
        return "Some generic animal sound"


class Dog(Animal):
    def make_sound(self) -> str:  # Override
        return "Woof!"


class Cat(Animal):
    def make_sound(self) -> str:  # Override
        return "Meow!"


# Polymorphism in action
animals = [Dog("Buddy", 3), Cat("Whiskers", 5), Animal("Generic", 1)]

for animal in animals:
    print(animal.make_sound())

# Output:
# Woof!
# Meow!
# Some generic animal sound
```

### Extending Parent Methods

```python
class Animal:
    def __init__(self, name: str):
        self.name = name
    
    def describe(self) -> str:
        return f"This is {self.name}"


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed
    
    def describe(self) -> str:
        # Call parent method AND add more
        parent_description = super().describe()
        return f"{parent_description}, a {self.breed}"


dog = Dog("Buddy", "Golden Retriever")
print(dog.describe())
# "This is Buddy, a Golden Retriever"
```

---

## Lecture 3.2: Composition

### What is Composition?

**Composition** means building complex objects by combining simpler objects.

**"HAS-A" relationship** (not "IS-A")
- A car HAS-A engine
- A person HAS-AN address
- A book HAS-A author

### Composition vs Inheritance

**Use Inheritance when:** "IS-A" relationship
```python
class Dog(Animal):  # Dog IS-A Animal
    pass
```

**Use Composition when:** "HAS-A" relationship
```python
class Car:
    def __init__(self):
        self.engine = Engine()  # Car HAS-A Engine
```

### Example: Address and Person

```python
class Address:
    """Represents a physical address."""
    
    def __init__(self, street: str, city: str, postal_code: str):
        self.street = street
        self.city = city
        self.postal_code = postal_code
    
    def __str__(self) -> str:
        return f"{self.street}, {self.city} {self.postal_code}"


class Person:
    """A person has an address."""
    
    def __init__(self, name: str, address: Address):
        self.name = name
        self.address = address  # Composition!
    
    def __str__(self) -> str:
        return f"{self.name} lives at {self.address}"


# Usage
address = Address("123 Main St", "Springfield", "12345")
person = Person("Alice", address)
print(person)
# "Alice lives at 123 Main St, Springfield 12345"
```

### Example: Engine and Car

```python
class Engine:
    """Car engine."""
    
    def __init__(self, horsepower: int):
        self.horsepower = horsepower
        self.running = False
    
    def start(self) -> str:
        self.running = True
        return "Engine started"
    
    def stop(self) -> str:
        self.running = False
        return "Engine stopped"


class Car:
    """A car has an engine."""
    
    def __init__(self, make: str, model: str, horsepower: int):
        self.make = make
        self.model = model
        self.engine = Engine(horsepower)  # Composition!
    
    def start(self) -> str:
        return f"{self.make} {self.model}: {self.engine.start()}"
    
    def stop(self) -> str:
        return f"{self.make} {self.model}: {self.engine.stop()}"


car = Car("Toyota", "Camry", 200)
print(car.start())  # "Toyota Camry: Engine started"
print(car.stop())   # "Toyota Camry: Engine stopped"
```

### Why Favor Composition?

**Problems with deep inheritance:**
```python
# ❌ Inheritance hierarchy can get messy
class Vehicle:
    pass

class LandVehicle(Vehicle):
    pass

class WaterVehicle(Vehicle):
    pass

class AmphibiousVehicle(LandVehicle, WaterVehicle):  # Multiple inheritance - complex!
    pass
```

**Better with composition:**
```python
# ✅ Composition is clearer
class LandCapability:
    def drive(self):
        return "Driving on land"

class WaterCapability:
    def sail(self):
        return "Sailing on water"

class AmphibiousVehicle:
    def __init__(self):
        self.land = LandCapability()
        self.water = WaterCapability()
    
    def drive(self):
        return self.land.drive()
    
    def sail(self):
        return self.water.sail()
```

---

## Lecture 3.3: Polymorphism

### What is Polymorphism?

**Polymorphism** = "many forms"

Same interface, different implementations.

### Example: Payment Processing

```python
class CreditCard:
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount} via Credit Card"


class PayPal:
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount} via PayPal"


class BankTransfer:
    def process_payment(self, amount: float) -> str:
        return f"Processing ${amount} via Bank Transfer"


def checkout(payment_method, amount: float):
    """Polymorphic function - works with any payment method."""
    print(payment_method.process_payment(amount))


# All work the same way!
checkout(CreditCard(), 100.0)
checkout(PayPal(), 50.0)
checkout(BankTransfer(), 200.0)
```

### Duck Typing

**"If it walks like a duck and quacks like a duck, it's a duck."**

Python doesn't care about the class, only that it has the required methods.

```python
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Car:
    def honk(self):
        return "Beep!"


def make_it_speak(thing):
    """Works with anything that has a speak() method."""
    return thing.speak()


make_it_speak(Dog())  # Works!
make_it_speak(Cat())  # Works!
make_it_speak(Car())  # AttributeError: 'Car' object has no attribute 'speak'
```

---

## Lecture 3.4: Abstract Base Classes

### What are Abstract Classes?

**Abstract classes** define a contract that subclasses must follow.

**Can't instantiate abstract classes directly** - must create concrete subclasses.

### Using ABC (Abstract Base Class)

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract base class for shapes."""
    
    @abstractmethod
    def area(self) -> float:
        """Calculate area - must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter - must be implemented by subclasses."""
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


# Cannot instantiate abstract class
shape = Shape()  # TypeError: Can't instantiate abstract class

# Can instantiate concrete classes
rect = Rectangle(5, 3)
circle = Circle(4)

print(rect.area())      # 15
print(circle.area())    # 50.26544

# Polymorphism with abstract base class
shapes: list[Shape] = [rect, circle]
for shape in shapes:
    print(f"Area: {shape.area()}")
```

### Why Use Abstract Classes?

**1. Enforce contracts**
```python
class IncompleteRectangle(Shape):
    def area(self) -> float:
        return 0
    # Missing perimeter() - won't let you create this!

rect = IncompleteRectangle()  # TypeError
```

**2. Document interfaces**
```python
class PaymentMethod(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Process a payment - returns True if successful."""
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> bool:
        """Refund a payment - returns True if successful."""
        pass
```

**3. Enable polymorphism with type safety**
```python
def calculate_total_area(shapes: list[Shape]) -> float:
    """Calculate total area of shapes."""
    return sum(shape.area() for shape in shapes)
```

---

## Exercise 3.1: Vehicle Hierarchy

### Problem Statement

Create an inheritance hierarchy for different types of vehicles.

### Requirements

**Base Class: Vehicle**
- Attributes: `make`, `model`, `year`
- Methods: `describe()`, `start()`, `stop()`

**Subclass: Car**
- Additional attribute: `num_doors`
- Override `describe()` to include number of doors

**Subclass: Motorcycle**
- Additional attribute: `engine_cc`
- Override `describe()` to include engine size

### Your Task

Implement with proper use of `super()` and method overriding.

---

## Exercise 3.2: Composition Example

### Problem Statement

Create a `Library` system using composition.

### Requirements

**Class: Book**
- Attributes: title, author, ISBN

**Class: Member**
- Attributes: name, member_id, borrowed_books (list)

**Class: Library**
- Has collection of books
- Has collection of members
- Can add/remove books
- Can register members
- Can handle checkouts/returns

### Your Task

Use composition to build this system.

---

## Exercise 3.3: Abstract Shapes

### Problem Statement

Create an abstract shape system with multiple concrete implementations.

### Requirements

**Abstract Class: Shape**
- Abstract methods: `area()`, `perimeter()`

**Concrete Classes:**
- `Rectangle(width, height)`
- `Circle(radius)`
- `Triangle(side1, side2, side3)`

Each must implement both abstract methods.

### Your Task

Use ABC to create this hierarchy.

---

## Challenge 3.1: Payment Processing System

### Problem Statement

Design a flexible payment processing system.

### Requirements

**Abstract Base Class: PaymentMethod**
- Abstract method: `process_payment(amount) -> bool`
- Abstract method: `get_fee(amount) -> float`

**Concrete Classes:**
- `CreditCard` - 2.9% + $0.30 fee
- `PayPal` - 3.5% fee
- `BankTransfer` - $1.00 flat fee

**Class: PaymentProcessor**
- Accepts any PaymentMethod
- Processes payments
- Calculates total with fees

### Your Task

Implement with proper abstraction and polymorphism.

---

(Continued in next part due to length limit...)