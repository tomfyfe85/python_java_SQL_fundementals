# CS Fundamentals: A Complete Course
## Object-Oriented Programming, Data Structures, Algorithms & SQL

---

## Course Structure

This course is divided into 8 modules, each building on the previous. Each module contains:
- **Theory Lectures** - Core concepts explained
- **Coding Examples** - Working code to study
- **Exercises** - Practice problems
- **Challenges** - Harder problems to test mastery
- **Project Work** - Building toward your Pizza Restaurant

**Estimated Time:** 10-12 weeks (10-15 hours/week)

---

## MODULE 1: Programming Fundamentals & Clean Code (Week 1-2)

### Learning Objectives
- Understand variables, data types, and control flow
- Write clean, readable code
- Use functions effectively
- Understand naming conventions and code organization

### Topics

#### 1.1 Variables and Basic Types
- Primitive types (int, float, str, bool)
- Type hints in Python
- Variable naming conventions (snake_case)
- Constants vs variables

#### 1.2 Functions and Scope
- Function definition and calling
- Parameters vs arguments
- Return values
- Scope (local, global)
- Pure functions vs side effects

#### 1.3 Clean Code Principles
- Meaningful names
- Functions should do ONE thing
- DRY (Don't Repeat Yourself)
- Comments vs self-documenting code
- Code formatting (PEP 8)

#### 1.4 Control Flow
- if/elif/else
- Boolean logic
- while loops
- for loops
- break and continue

### Exercises

**Exercise 1.1:** Write a function `calculate_discount(price, discount_percent)` that returns the discounted price. Use type hints.

**Exercise 1.2:** Refactor this bad code:
```python
def f(x, y, z):
    a = x + y
    b = a * z
    if b > 100:
        return b - 10
    else:
        return b
```

**Exercise 1.3:** Write a function that validates an email address (contains @, has text before and after @).

**Challenge 1.1:** Create a simple calculator that takes two numbers and an operation (+, -, *, /) and returns the result. Handle division by zero gracefully.

---

## MODULE 2: Object-Oriented Programming Basics (Week 2-3)

### Learning Objectives
- Understand what objects and classes are
- Create classes with attributes and methods
- Understand encapsulation
- Use constructors properly

### Topics

#### 2.1 Classes and Objects
- What is a class? (Blueprint metaphor)
- What is an object? (Instance of a class)
- Attributes (data)
- Methods (behavior)
- The `self` parameter

#### 2.2 Constructors
- `__init__` method
- Instance variables
- Default parameters
- Initialization logic

#### 2.3 Encapsulation
- Public vs private (underscore convention)
- Getters and setters
- Property decorators
- Why hide implementation details?

#### 2.4 String Representation
- `__str__` vs `__repr__`
- Debugging your objects

### Exercises

**Exercise 2.1:** Create a `BankAccount` class with:
- Attributes: account_number, balance, owner_name
- Methods: deposit(amount), withdraw(amount), get_balance()
- Ensure balance cannot go negative

**Exercise 2.2:** Create a `Book` class with:
- Attributes: title, author, isbn, available (boolean)
- Methods: checkout(), return_book(), __str__()

**Exercise 2.3:** Add validation to the Book class:
- ISBN must be exactly 13 digits
- Title and author cannot be empty
- Use property decorators or validation in __init__

**Challenge 2.1:** Create a `Temperature` class that:
- Stores temperature in Celsius internally
- Has properties to get/set in Celsius, Fahrenheit, and Kelvin
- Automatically converts between units

---

## MODULE 3: Object-Oriented Programming Advanced (Week 3-4)

### Learning Objectives
- Understand inheritance and composition
- Learn polymorphism
- Use abstract base classes
- Understand when to use inheritance vs composition

### Topics

#### 3.1 Inheritance
- Parent/child classes (superclass/subclass)
- The `super()` function
- Method overriding
- When to use inheritance (IS-A relationship)

#### 3.2 Composition
- Has-A relationship
- Building complex objects from simpler ones
- Favor composition over inheritance (why?)

#### 3.3 Polymorphism
- Same interface, different behavior
- Duck typing in Python
- Method overriding vs overloading

#### 3.4 Abstract Classes
- Abstract Base Classes (ABC)
- Abstract methods
- Enforcing contracts

### Exercises

**Exercise 3.1:** Create an inheritance hierarchy:
- Base class: `Vehicle` (brand, model, year)
- Child classes: `Car` (num_doors), `Motorcycle` (engine_cc)
- Each has a `describe()` method

**Exercise 3.2:** Create a composition example:
- `Address` class (street, city, postal_code)
- `Person` class that HAS an Address
- Method to get full address string

**Exercise 3.3:** Create an abstract `Shape` class with:
- Abstract method: `area()`
- Abstract method: `perimeter()`
- Concrete implementations: `Rectangle`, `Circle`, `Triangle`

**Challenge 3.1:** Design a simple payment system:
- Abstract `PaymentMethod` class
- Concrete classes: `CreditCard`, `PayPal`, `BankTransfer`
- Each processes payments differently
- A `PaymentProcessor` that accepts any PaymentMethod

---

## MODULE 4: SOLID Principles (Week 4-5)

### Learning Objectives
- Understand each SOLID principle deeply
- Recognize violations in code
- Refactor code to follow SOLID
- Apply principles in design

### Topics

#### 4.1 Single Responsibility Principle (SRP)
- A class should have ONE reason to change
- Separating concerns
- Example: User class vs UserRepository

#### 4.2 Open/Closed Principle (OCP)
- Open for extension, closed for modification
- Using inheritance and composition
- Plugin architecture

#### 4.3 Liskov Substitution Principle (LSP)
- Subtypes must be substitutable for base types
- Contract enforcement
- Common violations

#### 4.4 Interface Segregation Principle (ISP)
- Many specific interfaces > one general interface
- Clients shouldn't depend on unused methods
- Using ABC in Python

#### 4.5 Dependency Inversion Principle (DIP)
- Depend on abstractions, not concretions
- Dependency injection
- Testability

### Exercises

**Exercise 4.1 (SRP):** Refactor this class that does too much:
```python
class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def save_to_database(self):
        # saves user to DB
        pass
    
    def send_email(self, message):
        # sends email to user
        pass
```

**Exercise 4.2 (OCP):** Create a discount system:
- Base `Discount` class
- Extendable without modifying existing code
- Types: `PercentageDiscount`, `FixedAmountDiscount`, `BuyOneGetOne`

**Exercise 4.3 (DIP):** Refactor to use dependency injection:
```python
class OrderService:
    def __init__(self):
        self.db = MySQLDatabase()  # tight coupling!
    
    def place_order(self, order):
        self.db.save(order)
```

**Challenge 4.1:** Design a notification system following ALL SOLID principles:
- Multiple notification types (Email, SMS, Push)
- Easy to add new types
- Different formatting for each
- Don't violate any SOLID principle

---

## MODULE 5: Data Structures (Week 5-7)

### Learning Objectives
- Understand fundamental data structures
- Know when to use each structure
- Implement structures from scratch
- Analyze time/space complexity (Big O)

### Topics

#### 5.1 Arrays and Lists
- Dynamic arrays
- Time complexity of operations
- List comprehensions
- When to use lists

#### 5.2 Linked Lists
- Singly linked lists
- Doubly linked lists
- Implementation from scratch
- Comparison with arrays

#### 5.3 Stacks and Queues
- LIFO vs FIFO
- Implementation using lists
- Use cases
- Deque in Python

#### 5.4 Hash Tables / Dictionaries
- How hashing works
- Collision resolution
- Time complexity (average vs worst case)
- Sets vs dictionaries

#### 5.5 Trees
- Binary trees
- Binary search trees
- Tree traversal (in-order, pre-order, post-order)
- Balanced trees (concept)

#### 5.6 Graphs
- Representations (adjacency list/matrix)
- Directed vs undirected
- Weighted vs unweighted
- Use cases

### Exercises

**Exercise 5.1:** Implement a `Stack` class with push, pop, peek, is_empty methods.

**Exercise 5.2:** Implement a `Queue` class using two stacks.

**Exercise 5.3:** Implement a `LinkedList` class with:
- append, prepend, insert_at, delete, find

**Exercise 5.4:** Create a `BinarySearchTree` class with:
- insert, search, delete methods
- in_order_traversal method

**Challenge 5.1:** Implement a `LRU Cache` (Least Recently Used):
- Uses hash table + doubly linked list
- O(1) get and put operations
- Fixed capacity

---

## MODULE 6: Algorithms (Week 7-8)

### Learning Objectives
- Understand Big O notation
- Master searching and sorting
- Solve problems recursively
- Recognize algorithm patterns

### Topics

#### 6.1 Algorithm Analysis
- Time complexity (Big O, Omega, Theta)
- Space complexity
- Best, average, worst case
- Common complexities (O(1), O(log n), O(n), O(n²))

#### 6.2 Searching Algorithms
- Linear search
- Binary search
- When to use each

#### 6.3 Sorting Algorithms
- Bubble sort (educational)
- Selection sort
- Insertion sort
- Merge sort
- Quick sort
- When to use each

#### 6.4 Recursion
- Base case and recursive case
- Call stack
- Recursive vs iterative
- Common patterns

#### 6.5 Algorithm Patterns
- Two pointers
- Sliding window
- Divide and conquer
- Dynamic programming (intro)

### Exercises

**Exercise 6.1:** Implement binary search recursively and iteratively.

**Exercise 6.2:** Implement merge sort from scratch.

**Exercise 6.3:** Solve: Find all pairs in an array that sum to a target value (use two pointers).

**Exercise 6.4:** Calculate Fibonacci(n) three ways:
- Recursive (slow)
- Iterative
- With memoization

**Challenge 6.1:** Solve the "Maximum Subarray Sum" problem (Kadane's algorithm).

**Challenge 6.2:** Implement quicksort with random pivot selection.

---

## MODULE 7: SQL and Database Design (Week 8-10)

### Learning Objectives
- Design normalized databases
- Write complex SQL queries
- Understand transactions and constraints
- Integrate SQL with Python

### Topics

#### 7.1 Database Fundamentals
- What is a database?
- RDBMS concepts
- Tables, rows, columns
- Primary keys and foreign keys

#### 7.2 SQL Basics
- CREATE TABLE
- INSERT, SELECT, UPDATE, DELETE
- WHERE clauses
- ORDER BY, LIMIT

#### 7.3 SQL Intermediate
- JOINs (INNER, LEFT, RIGHT, FULL)
- Aggregate functions (COUNT, SUM, AVG, MAX, MIN)
- GROUP BY and HAVING
- Subqueries

#### 7.4 Database Design
- Normalization (1NF, 2NF, 3NF)
- Entity-Relationship diagrams
- One-to-many, many-to-many relationships
- Junction tables

#### 7.5 Constraints and Indexes
- NOT NULL, UNIQUE, CHECK
- Indexes for performance
- FOREIGN KEY constraints
- ON DELETE CASCADE

#### 7.6 Transactions
- ACID properties
- BEGIN, COMMIT, ROLLBACK
- Isolation levels (concept)

#### 7.7 Python + SQL
- psycopg2 library
- Parameterized queries (SQL injection prevention)
- Connection management
- Cursor usage

### Exercises

**Exercise 7.1:** Design a database for a library:
- Books, Authors, Members, Loans
- Draw ER diagram
- Write CREATE TABLE statements

**Exercise 7.2:** Write queries:
- Find all books by a specific author
- Find all overdue loans
- Count books per genre

**Exercise 7.3:** Create a many-to-many relationship:
- Students and Courses
- With enrollment date

**Exercise 7.4:** Write a Python function that:
- Connects to PostgreSQL
- Inserts a new record using parameters
- Returns the inserted ID

**Challenge 7.1:** Design and implement a database for a blog:
- Users, Posts, Comments, Tags
- Posts can have multiple tags
- Users can follow other users
- Write 5 complex queries

---

## MODULE 8: Testing and Integration (Week 10-11)

### Learning Objectives
- Write unit tests with pytest
- Understand Test-Driven Development
- Mock dependencies
- Integration testing

### Topics

#### 8.1 Why Test?
- Catching bugs early
- Refactoring confidence
- Documentation through tests
- Test pyramid

#### 8.2 Unit Testing with pytest
- Writing test functions
- Assertions
- Fixtures
- Parametrized tests

#### 8.3 Test-Driven Development
- Red-Green-Refactor cycle
- Writing tests first
- Benefits and challenges

#### 8.4 Mocking
- Why mock?
- unittest.mock
- Mocking database calls
- Mocking external services

#### 8.5 Integration Testing
- Testing multiple components
- Database testing strategies
- Test database setup/teardown

### Exercises

**Exercise 8.1:** Write tests for your BankAccount class from Module 2.

**Exercise 8.2:** Practice TDD: Build a `Calculator` class test-first.

**Exercise 8.3:** Create a mock for a database repository and test a service that uses it.

**Challenge 8.1:** Write integration tests for a repository class that actually connects to a test database.

---

## FINAL PROJECT: Pizza Takeaway System (Week 11-12)

Now you'll apply EVERYTHING you've learned!

### Requirements

**Models:**
- Customer, Pizza, Topping, Order
- Use proper OOP with encapsulation

**Services:**
- OrderService, MenuService, PricingService
- Follow SOLID principles
- Single Responsibility for each service

**Data Layer:**
- Repository classes for each model
- Use raw SQL with psycopg2
- Proper database design (normalized)

**CLI Interface:**
- User-friendly command-line menu
- Create orders, view menu, see order history

**Testing:**
- Unit tests for all models
- Unit tests for services (with mocks)
- Integration tests for repositories
- 80%+ code coverage

**Data Structures:**
- Use appropriate data structures
- Implement a simple order queue

**Algorithms:**
- Sort pizzas by price
- Search orders by customer

### Deliverables
1. Complete working application
2. Test suite (all passing)
3. Database schema
4. README with setup instructions

---

## Assessment Criteria

For each module, you should be able to:
- ✅ Explain concepts in your own words
- ✅ Complete all exercises independently
- ✅ Solve challenges with minimal hints
- ✅ Apply concepts to new problems

**Don't move to the next module until you're comfortable with the current one!**

---

## Getting Started

**Reply with:** "I'm ready for Module 1" and I'll give you the first lecture and exercises.

We'll go step by step. I'll explain concepts, give you exercises, review your code, and help you when you're stuck - but I won't do the work for you. You'll learn by doing!

**Questions before we start?**