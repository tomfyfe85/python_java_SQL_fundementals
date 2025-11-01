# CS Fundamentals: Complete Course Part 2
## Modules 4-9, Final Project, and Resources

---

# 📋 TABLE OF CONTENTS - PART 2

1. [Module 4: SOLID Principles](#module-4)
2. [Module 5: Data Structures](#module-5)
3. [Module 6: Algorithms](#module-6)
4. [Module 7: SQL and Database Design](#module-7)
5. [Module 8: Design Patterns (Gang of Four)](#module-8)
6. [Module 9: Testing and TDD](#module-9)
7. [Final Project: Pizza Restaurant System](#final-project)
8. [Resources and References](#resources)
9. [Progress Tracking](#progress-tracking)

---

<a name="module-4"></a>
# MODULE 4: SOLID Principles

**Duration:** 1-2 weeks  
**Focus:** Writing maintainable, extensible, professional code

---

## Introduction to SOLID

**SOLID** is an acronym for five design principles that make software more:
- Understandable
- Flexible
- Maintainable
- Testable

**Created by:** Robert C. Martin (Uncle Bob)

**The Five Principles:**
- **S** - Single Responsibility Principle
- **O** - Open/Closed Principle
- **L** - Liskov Substitution Principle
- **I** - Interface Segregation Principle
- **D** - Dependency Inversion Principle

---

## Lecture 4.1: Single Responsibility Principle (SRP)

### Definition

**"A class should have one, and only one, reason to change."**

Each class should have a single responsibility - one job to do.

### Why SRP Matters

**Without SRP:**
- Hard to understand (class does too much)
- Hard to test (many things to test at once)
- Hard to reuse (can't use one part without the rest)
- Hard to maintain (changes affect many things)

### Example: Violation of SRP

```python
# ❌ BAD - User class has too many responsibilities
class User:
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
    
    # Responsibility 1: User data management
    def get_username(self) -> str:
        return self.username
    
    # Responsibility 2: Database operations
    def save_to_database(self) -> None:
        """Save user to database."""
        connection = create_db_connection()
        connection.execute(f"INSERT INTO users VALUES ('{self.username}', '{self.email}')")
    
    # Responsibility 3: Email sending
    def send_welcome_email(self) -> None:
        """Send welcome email to user."""
        smtp = create_smtp_connection()
        smtp.send(self.email, "Welcome!", "Thanks for joining!")
    
    # Responsibility 4: Validation
    def validate_email(self) -> bool:
        """Validate email format."""
        return "@" in self.email
```

**Problems:**
- If database schema changes, User class must change
- If email service changes, User class must change
- If validation rules change, User class must change
- Can't test validation without database
- Can't reuse email sending elsewhere

### Example: Following SRP

```python
# ✅ GOOD - Each class has one responsibility

class User:
    """Represents a user - only manages user data."""
    
    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email
    
    def get_username(self) -> str:
        return self.username
    
    def get_email(self) -> str:
        return self.email


class UserRepository:
    """Handles database operations for users."""
    
    def save(self, user: User) -> None:
        """Save user to database."""
        connection = create_db_connection()
        connection.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (user.get_username(), user.get_email())
        )
    
    def find_by_username(self, username: str) -> User:
        """Find user by username."""
        # Database query logic
        pass


class EmailService:
    """Handles email sending."""
    
    def send_welcome_email(self, email: str) -> None:
        """Send welcome email."""
        smtp = create_smtp_connection()
        smtp.send(email, "Welcome!", "Thanks for joining!")


class EmailValidator:
    """Validates email addresses."""
    
    @staticmethod
    def is_valid(email: str) -> bool:
        """Check if email format is valid."""
        return "@" in email and "." in email.split("@")[1]


# Usage
user = User("alice", "alice@example.com")

# Each class does its own job
if EmailValidator.is_valid(user.get_email()):
    repository = UserRepository()
    repository.save(user)
    
    email_service = EmailService()
    email_service.send_welcome_email(user.get_email())
```

**Benefits:**
- Each class has one reason to change
- Easy to test each class independently
- Easy to reuse components
- Clear separation of concerns

### How to Identify SRP Violations

Ask: **"How many reasons does this class have to change?"**

If more than one, you're violating SRP.

**Examples of multiple responsibilities:**
- User class that also handles database operations
- Product class that also calculates taxes
- Order class that also sends email notifications

### Real-World Example: Report Generator

```python
# ❌ BAD - ReportGenerator does too much
class ReportGenerator:
    def generate_report(self, data: list) -> None:
        """Generate and send report."""
        # Responsibility 1: Data processing
        processed = self.process_data(data)
        
        # Responsibility 2: Formatting
        formatted = self.format_as_pdf(processed)
        
        # Responsibility 3: Saving
        self.save_to_file(formatted)
        
        # Responsibility 4: Emailing
        self.email_report(formatted)


# ✅ GOOD - Separate responsibilities
class DataProcessor:
    """Process raw data."""
    def process(self, data: list) -> dict:
        # Processing logic
        pass


class PDFFormatter:
    """Format data as PDF."""
    def format(self, data: dict) -> bytes:
        # PDF formatting logic
        pass


class FileStorage:
    """Save files to disk."""
    def save(self, filename: str, content: bytes) -> None:
        # File saving logic
        pass


class EmailSender:
    """Send emails."""
    def send_report(self, recipient: str, attachment: bytes) -> None:
        # Email sending logic
        pass


class ReportGenerator:
    """Orchestrate report generation."""
    def __init__(self, processor, formatter, storage, emailer):
        self.processor = processor
        self.formatter = formatter
        self.storage = storage
        self.emailer = emailer
    
    def generate_report(self, data: list, email: str) -> None:
        """Generate and distribute report."""
        processed = self.processor.process(data)
        formatted = self.formatter.format(processed)
        self.storage.save("report.pdf", formatted)
        self.emailer.send_report(email, formatted)
```

---

## Lecture 4.2: Open/Closed Principle (OCP)

### Definition

**"Software entities should be open for extension, but closed for modification."**

- **Open for extension:** You can add new functionality
- **Closed for modification:** You don't change existing code

### Why OCP Matters

**Without OCP:**
- Every new feature requires modifying existing code
- Risk of breaking existing functionality
- Hard to add features without side effects

### Example: Violation of OCP

```python
# ❌ BAD - Must modify calculate_discount() for each new discount type
class DiscountCalculator:
    def calculate_discount(self, customer_type: str, total: float) -> float:
        """Calculate discount based on customer type."""
        if customer_type == "regular":
            return total * 0.0  # No discount
        elif customer_type == "silver":
            return total * 0.10  # 10% discount
        elif customer_type == "gold":
            return total * 0.20  # 20% discount
        elif customer_type == "platinum":  # Added new type - must modify existing code!
            return total * 0.30  # 30% discount
        else:
            return 0.0
```

**Problems:**
- Adding "platinum" requires modifying existing code
- Must test all cases again after each change
- Risk of breaking existing discount types

### Example: Following OCP

```python
# ✅ GOOD - Use inheritance/polymorphism to extend behavior
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract base class for discount strategies."""
    
    @abstractmethod
    def calculate_discount(self, total: float) -> float:
        """Calculate discount amount."""
        pass


class NoDiscount(DiscountStrategy):
    """No discount."""
    def calculate_discount(self, total: float) -> float:
        return 0.0


class PercentageDiscount(DiscountStrategy):
    """Percentage-based discount."""
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate_discount(self, total: float) -> float:
        return total * self.percentage


class FixedAmountDiscount(DiscountStrategy):
    """Fixed amount discount."""
    def __init__(self, amount: float):
        self.amount = amount
    
    def calculate_discount(self, total: float) -> float:
        return min(self.amount, total)


class DiscountCalculator:
    """Calculate discount using strategy pattern."""
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy
    
    def calculate_discount(self, total: float) -> float:
        """Calculate discount using current strategy."""
        return self.strategy.calculate_discount(total)


# Usage - easily extensible without modifying existing code
regular = DiscountCalculator(NoDiscount())
silver = DiscountCalculator(PercentageDiscount(0.10))
gold = DiscountCalculator(PercentageDiscount(0.20))

# Adding new discount type - no existing code modified!
class PlatinumDiscount(DiscountStrategy):
    """30% discount plus $10 fixed."""
    def calculate_discount(self, total: float) -> float:
        percentage = total * 0.30
        return percentage + 10.0

platinum = DiscountCalculator(PlatinumDiscount())
```

**Benefits:**
- Add new discount types without changing existing code
- Each discount type is independently testable
- No risk of breaking existing functionality

### Real-World Example: Shape Area Calculator

```python
# ❌ BAD - Must modify for each new shape
class AreaCalculator:
    def calculate_area(self, shapes: list) -> float:
        total = 0
        for shape in shapes:
            if shape['type'] == 'circle':
                total += 3.14159 * shape['radius'] ** 2
            elif shape['type'] == 'rectangle':
                total += shape['width'] * shape['height']
            elif shape['type'] == 'triangle':  # Adding triangle requires modification
                total += 0.5 * shape['base'] * shape['height']
        return total


# ✅ GOOD - Open for extension
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract shape."""
    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height


class AreaCalculator:
    """Calculate total area - never needs modification."""
    def calculate_area(self, shapes: list[Shape]) -> float:
        return sum(shape.area() for shape in shapes)


# Adding new shape - no modification to AreaCalculator!
class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
    
    def area(self) -> float:
        return 0.5 * self.base * self.height
```

---

## Lecture 4.3: Liskov Substitution Principle (LSP)

### Definition

**"Subtypes must be substitutable for their base types."**

If class B is a subtype of class A, you should be able to replace A with B without breaking the program.

### Why LSP Matters

**Without LSP:**
- Inheritance hierarchies are fragile
- Polymorphism doesn't work correctly
- Runtime errors and unexpected behavior

### Example: Violation of LSP

```python
# ❌ BAD - Square violates LSP
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def set_width(self, width: float) -> None:
        self.width = width
    
    def set_height(self, height: float) -> None:
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height


class Square(Rectangle):
    """A square IS-A rectangle, right? Wrong for this implementation!"""
    def set_width(self, width: float) -> None:
        self.width = width
        self.height = width  # Square must keep width == height
    
    def set_height(self, height: float) -> None:
        self.width = height
        self.height = height


# This function expects Rectangle behavior
def resize_rectangle(rect: Rectangle) -> None:
    """Set rectangle to 5x4."""
    rect.set_width(5)
    rect.set_height(4)
    assert rect.area() == 20, "Expected area of 20"


# Works with Rectangle
rectangle = Rectangle(0, 0)
resize_rectangle(rectangle)  # ✅ Works - area is 20

# Breaks with Square!
square = Square(0, 0)
resize_rectangle(square)  # ❌ AssertionError - area is 16, not 20!
```

**Problem:** Square can't substitute for Rectangle because it changes the behavior.

### Example: Following LSP

```python
# ✅ GOOD - Separate hierarchies
from abc import ABC, abstractmethod


class Shape(ABC):
    """Base class for all shapes."""
    @abstractmethod
    def area(self) -> float:
        pass


class Rectangle(Shape):
    """Rectangle with independent width and height."""
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height


class Square(Shape):
    """Square with single side length."""
    def __init__(self, side: float):
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2


# Now both follow their contracts correctly
def calculate_total_area(shapes: list[Shape]) -> float:
    """Works with any shape."""
    return sum(shape.area() for shape in shapes)


shapes = [Rectangle(5, 4), Square(3)]
print(calculate_total_area(shapes))  # Works correctly!
```

### LSP Rules

**Subclass must:**
1. Accept the same inputs (or more general)
2. Return the same types (or more specific)
3. Not throw new exceptions
4. Maintain the base class invariants
5. Not strengthen preconditions
6. Not weaken postconditions

### Example: Bird Hierarchy Violation

```python
# ❌ BAD - Penguin violates LSP
class Bird:
    def fly(self) -> str:
        return "Flying through the air"


class Sparrow(Bird):
    pass  # Can fly


class Penguin(Bird):
    def fly(self) -> str:
        raise Exception("Penguins can't fly!")  # Violates LSP!


def make_bird_fly(bird: Bird) -> None:
    print(bird.fly())  # Should work for any Bird


make_bird_fly(Sparrow())  # ✅ Works
make_bird_fly(Penguin())  # ❌ Exception! LSP violated


# ✅ GOOD - Better hierarchy
from abc import ABC, abstractmethod


class Bird(ABC):
    @abstractmethod
    def move(self) -> str:
        pass


class FlyingBird(Bird):
    def move(self) -> str:
        return "Flying"
    
    def fly(self) -> str:
        return "Flying through the air"


class FlightlessBird(Bird):
    def move(self) -> str:
        return "Walking"


class Sparrow(FlyingBird):
    pass


class Penguin(FlightlessBird):
    def swim(self) -> str:
        return "Swimming"


# Now all birds follow their contracts
def move_bird(bird: Bird) -> None:
    print(bird.move())  # Works for all birds!


move_bird(Sparrow())  # "Flying"
move_bird(Penguin())  # "Walking"
```

---

## Lecture 4.4: Interface Segregation Principle (ISP)

### Definition

**"Clients should not be forced to depend on interfaces they don't use."**

Many specific interfaces are better than one general-purpose interface.

### Why ISP Matters

**Without ISP:**
- Classes forced to implement methods they don't need
- Fat interfaces hard to implement
- Changes affect unrelated classes

### Example: Violation of ISP

```python
# ❌ BAD - Fat interface
from abc import ABC, abstractmethod


class Worker(ABC):
    """All workers must implement all methods - even if they don't apply!"""
    
    @abstractmethod
    def work(self) -> None:
        pass
    
    @abstractmethod
    def eat(self) -> None:
        pass
    
    @abstractmethod
    def sleep(self) -> None:
        pass


class Human(Worker):
    """Human workers need all methods."""
    def work(self) -> None:
        print("Human working")
    
    def eat(self) -> None:
        print("Human eating")
    
    def sleep(self) -> None:
        print("Human sleeping")


class Robot(Worker):
    """Robots don't eat or sleep - but forced to implement these methods!"""
    def work(self) -> None:
        print("Robot working")
    
    def eat(self) -> None:
        pass  # Robots don't eat - empty implementation (bad!)
    
    def sleep(self) -> None:
        pass  # Robots don't sleep - empty implementation (bad!)
```

**Problems:**
- Robot forced to implement eat() and sleep()
- Empty implementations are confusing
- Interface is too broad

### Example: Following ISP

```python
# ✅ GOOD - Segregated interfaces
from abc import ABC, abstractmethod


class Workable(ABC):
    """Interface for things that can work."""
    @abstractmethod
    def work(self) -> None:
        pass


class Eatable(ABC):
    """Interface for things that can eat."""
    @abstractmethod
    def eat(self) -> None:
        pass


class Sleepable(ABC):
    """Interface for things that can sleep."""
    @abstractmethod
    def sleep(self) -> None:
        pass


class Human(Workable, Eatable, Sleepable):
    """Humans can do all three."""
    def work(self) -> None:
        print("Human working")
    
    def eat(self) -> None:
        print("Human eating")
    
    def sleep(self) -> None:
        print("Human sleeping")


class Robot(Workable):
    """Robots only work - implements only what it needs!"""
    def work(self) -> None:
        print("Robot working")


# Functions work with specific interfaces
def make_work(worker: Workable) -> None:
    worker.work()


def feed(eater: Eatable) -> None:
    eater.eat()


# Both can work
make_work(Human())
make_work(Robot())

# Only humans can eat
feed(Human())
# feed(Robot())  # Type error - Robot doesn't implement Eatable
```

### Real-World Example: Printer Interface

```python
# ❌ BAD - All printers forced to implement all methods
from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print_document(self, doc: str) -> None:
        pass
    
    @abstractmethod
    def scan_document(self) -> str:
        pass
    
    @abstractmethod
    def fax_document(self, doc: str, number: str) -> None:
        pass


class AllInOnePrinter(Printer):
    """Can do everything - interface fits."""
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")
    
    def scan_document(self) -> str:
        return "Scanned content"
    
    def fax_document(self, doc: str, number: str) -> None:
        print(f"Faxing {doc} to {number}")


class SimplePrinter(Printer):
    """Can only print - but forced to implement scan and fax!"""
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")
    
    def scan_document(self) -> str:
        raise NotImplementedError("This printer can't scan")
    
    def fax_document(self, doc: str, number: str) -> None:
        raise NotImplementedError("This printer can't fax")


# ✅ GOOD - Segregated interfaces
class Printable(ABC):
    @abstractmethod
    def print_document(self, doc: str) -> None:
        pass


class Scannable(ABC):
    @abstractmethod
    def scan_document(self) -> str:
        pass


class Faxable(ABC):
    @abstractmethod
    def fax_document(self, doc: str, number: str) -> None:
        pass


class SimplePrinter(Printable):
    """Implements only what it can do."""
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")


class AllInOnePrinter(Printable, Scannable, Faxable):
    """Implements all interfaces."""
    def print_document(self, doc: str) -> None:
        print(f"Printing: {doc}")
    
    def scan_document(self) -> str:
        return "Scanned content"
    
    def fax_document(self, doc: str, number: str) -> None:
        print(f"Faxing {doc} to {number}")
```

---

## Lecture 4.5: Dependency Inversion Principle (DIP)

### Definition

**"Depend on abstractions, not concretions."**

- High-level modules should not depend on low-level modules
- Both should depend on abstractions
- Abstractions should not depend on details
- Details should depend on abstractions

### Why DIP Matters

**Without DIP:**
- High-level code tightly coupled to low-level details
- Hard to change implementations
- Hard to test (can't mock dependencies)
- Inflexible system

### Example: Violation of DIP

```python
# ❌ BAD - High-level class depends on low-level concrete class
class MySQLDatabase:
    """Low-level database implementation."""
    def connect(self) -> None:
        print("Connecting to MySQL")
    
    def save(self, data: str) -> None:
        print(f"Saving to MySQL: {data}")


class OrderService:
    """High-level business logic - depends directly on MySQL!"""
    def __init__(self):
        self.db = MySQLDatabase()  # Tight coupling!
    
    def place_order(self, order: str) -> None:
        self.db.connect()
        self.db.save(order)


# Problems:
# 1. Can't switch to PostgreSQL without changing OrderService
# 2. Can't test OrderService without a real database
# 3. OrderService knows too much about database implementation
```

### Example: Following DIP

```python
# ✅ GOOD - Depend on abstraction
from abc import ABC, abstractmethod


class Database(ABC):
    """Abstract database interface."""
    @abstractmethod
    def connect(self) -> None:
        pass
    
    @abstractmethod
    def save(self, data: str) -> None:
        pass


class MySQLDatabase(Database):
    """Concrete MySQL implementation."""
    def connect(self) -> None:
        print("Connecting to MySQL")
    
    def save(self, data: str) -> None:
        print(f"Saving to MySQL: {data}")


class PostgreSQLDatabase(Database):
    """Concrete PostgreSQL implementation."""
    def connect(self) -> None:
        print("Connecting to PostgreSQL")
    
    def save(self, data: str) -> None:
        print(f"Saving to PostgreSQL: {data}")


class OrderService:
    """High-level business logic - depends on abstraction!"""
    def __init__(self, database: Database):  # Dependency injection
        self.db = database
    
    def place_order(self, order: str) -> None:
        self.db.connect()
        self.db.save(order)


# Usage - easy to switch implementations
mysql_service = OrderService(MySQLDatabase())
postgres_service = OrderService(PostgreSQLDatabase())

# Easy to test with mock
class MockDatabase(Database):
    def connect(self) -> None:
        print("Mock connect")
    
    def save(self, data: str) -> None:
        print(f"Mock save: {data}")

test_service = OrderService(MockDatabase())
```

**Benefits:**
- OrderService doesn't know about specific databases
- Easy to switch database implementations
- Easy to test with mocks
- Flexible and maintainable

### Dependency Injection

**Three types of dependency injection:**

#### 1. Constructor Injection (Most Common)

```python
class OrderService:
    def __init__(self, database: Database, email: EmailService):
        self.db = database
        self.email = email
```

#### 2. Setter Injection

```python
class OrderService:
    def set_database(self, database: Database) -> None:
        self.db = database
```

#### 3. Method Injection

```python
class OrderService:
    def place_order(self, order: str, database: Database) -> None:
        database.save(order)
```

### Real-World Example: Payment Processing

```python
# ❌ BAD - Tight coupling
class PaymentProcessor:
    def __init__(self):
        self.stripe = StripeAPI()  # Hardcoded dependency
    
    def process_payment(self, amount: float) -> bool:
        return self.stripe.charge(amount)


# ✅ GOOD - Depend on abstraction
from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    """Abstract payment gateway."""
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


class StripeGateway(PaymentGateway):
    """Stripe implementation."""
    def process_payment(self, amount: float) -> bool:
        # Stripe-specific logic
        return True


class PayPalGateway(PaymentGateway):
    """PayPal implementation."""
    def process_payment(self, amount: float) -> bool:
        # PayPal-specific logic
        return True


class PaymentProcessor:
    """Process payments - doesn't know which gateway."""
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    
    def process_payment(self, amount: float) -> bool:
        return self.gateway.process_payment(amount)


# Easy to switch payment gateways
stripe_processor = PaymentProcessor(StripeGateway())
paypal_processor = PaymentProcessor(PayPalGateway())
```

---

## Exercise 4.1: Refactor for SRP

### Problem Statement

Refactor the following class that violates Single Responsibility Principle.

### Bad Code

```python
class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password
    
    def save_to_database(self) -> None:
        """Save user to database."""
        import sqlite3
        conn = sqlite3.connect('users.db')
        conn.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (self.username, self.email, self.password)
        )
        conn.commit()
        conn.close()
    
    def send_welcome_email(self) -> None:
        """Send welcome email."""
        import smtplib
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.send_message(f"Welcome {self.username}!")
        server.quit()
    
    def hash_password(self) -> str:
        """Hash the password."""
        import hashlib
        return hashlib.sha256(self.password.encode()).hexdigest()
    
    def validate_email(self) -> bool:
        """Validate email format."""
        return "@" in self.email
```

### Your Task

Refactor into separate classes following SRP:
- `User` - Only user data
- `UserRepository` - Database operations
- `EmailService` - Email sending
- `PasswordHasher` - Password hashing
- `EmailValidator` - Email validation

Use UMPIRE to plan and implement.

---

## Exercise 4.2: Discount System (OCP)

### Problem Statement

Create an extensible discount system following the Open/Closed Principle.

### Requirements

**Base Abstraction: DiscountStrategy**
- Abstract method: `calculate_discount(price: float) -> float`

**Concrete Strategies:**
- `NoDiscount` - 0% discount
- `PercentageDiscount(percentage)` - X% off
- `FixedAmountDiscount(amount)` - $X off
- `BuyOneGetOneFree` - 50% off if quantity > 1

**DiscountCalculator Class:**
- Uses any DiscountStrategy
- Calculates final price

### Challenge

Add a new discount type without modifying existing code:
- `SeasonalDiscount` - 20% in December, 10% otherwise

---

## Exercise 4.3: Dependency Injection (DIP)

### Problem Statement

Refactor tightly coupled code to use Dependency Inversion.

### Bad Code

```python
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Sending email: {message}")


class OrderService:
    def __init__(self):
        self.email_sender = EmailSender()  # Tight coupling!
    
    def place_order(self, order_id: str) -> None:
        print(f"Order {order_id} placed")
        self.email_sender.send(f"Order {order_id} confirmed")
```

### Your Task

Refactor to:
1. Create abstract `NotificationService` interface
2. Implement `EmailNotification` and `SMSNotification`
3. Use dependency injection in `OrderService`
4. Make it easy to test with mocks

---

## Challenge 4.1: Notification System

### Problem Statement

Design a notification system following ALL SOLID principles.

### Requirements

**Multiple notification types:**
- Email
- SMS
- Push notification
- Slack message

**Features:**
- Send notifications
- Format messages differently per type
- Log all notifications
- Retry failed notifications

**SOLID Requirements:**
- **SRP:** Separate concerns (sending, formatting, logging, retry)
- **OCP:** Easy to add new notification types
- **LSP:** All notifications substitutable
- **ISP:** Specific interfaces for different capabilities
- **DIP:** Depend on abstractions

### Your Task

Design and implement using UMPIRE method.

---

<a name="module-5"></a>
# MODULE 5: Data Structures

**Duration:** 2-3 weeks  
**Focus:** Implement fundamental data structures from scratch

---

## Introduction to Data Structures

**Data structures** organize and store data efficiently.

**Why learn data structures?**
- Solve problems efficiently
- Understand how things work under the hood
- Pass technical interviews
- Choose the right tool for the job

---

## Lecture 5.1: Arrays and Lists

### Python Lists

Python lists are **dynamic arrays** - they automatically resize.

**Time Complexity:**
- Access by index: O(1)
- Append to end: O(1) amortized
- Insert at beginning: O(n)
- Delete from end: O(1)
- Delete from beginning: O(n)
- Search: O(n)

### Example Operations

```python
# Creating lists
numbers = [1, 2, 3, 4, 5]
empty = []
mixed = [1, "hello", 3.14, True]

# Accessing elements - O(1)
first = numbers[0]  # 1
last = numbers[-1]  # 5

# Modifying - O(1)
numbers[2] = 10  # [1, 2, 10, 4, 5]

# Appending - O(1) amortized
numbers.append(6)  # [1, 2, 10, 4, 5, 6]

# Inserting - O(n)
numbers.insert(0, 0)  # [0, 1, 2, 10, 4, 5, 6]

# Removing - O(n)
numbers.remove(10)  # [0, 1, 2, 4, 5, 6]

# Pop from end - O(1)
last = numbers.pop()  # 6, list is now [0, 1, 2, 4, 5]

# Pop from beginning - O(n)
first = numbers.pop(0)  # 0, list is now [1, 2, 4, 5]

# Length - O(1)
length = len(numbers)
```

### List Comprehensions

```python
# Create list of squares
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Filter even numbers
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Transform strings
words = ["hello", "world"]
upper = [word.upper() for word in words]
# ["HELLO", "WORLD"]
```

---

## Lecture 5.2: Linked Lists

### What is a Linked List?

A **linked list** is a sequence of nodes where each node contains:
- Data
- Reference (link) to the next node

**Types:**
- **Singly linked list:** Each node points to next
- **Doubly linked list:** Each node points to next AND previous

### Why Use Linked Lists?

**Advantages:**
- Efficient insertion/deletion at beginning: O(1)
- Dynamic size (no wasting memory)
- Easy to implement stacks and queues

**Disadvantages:**
- No random access (must traverse from head)
- Extra memory for links
- Poor cache locality

### Implementing Singly Linked List

```python
class Node:
    """Node in a linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Singly linked list implementation."""
    
    def __init__(self):
        self.head = None
        self._size = 0
    
    def append(self, data) -> None:
        """Add element to end - O(n)."""
        new_node = Node(data)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self._size += 1
    
    def prepend(self, data) -> None:
        """Add element to beginning - O(1)."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def delete(self, data) -> bool:
        """Delete first occurrence - O(n)."""
        if not self.head:
            return False
        
        # If head needs to be deleted
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        
        # Find node before the one to delete
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def find(self, data) -> bool:
        """Search for element - O(n)."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def __len__(self) -> int:
        """Return size - O(1)."""
        return self._size
    
    def __str__(self) -> str:
        """String representation - O(n)."""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        return " -> ".join(elements)


# Usage
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
print(ll)  # "1 -> 2 -> 3"

ll.prepend(0)
print(ll)  # "0 -> 1 -> 2 -> 3"

ll.delete(2)
print(ll)  # "0 -> 1 -> 3"

print(ll.find(3))  # True
print(ll.find(5))  # False
```

### Doubly Linked List

```python
class DNode:
    """Node in doubly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Doubly linked list - can traverse both directions."""
    
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
    
    def append(self, data) -> None:
        """Add to end - O(1) with tail pointer."""
        new_node = DNode(data)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self._size += 1
    
    def prepend(self, data) -> None:
        """Add to beginning - O(1)."""
        new_node = DNode(data)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        
        self._size += 1
```

---

## Lecture 5.3: Stacks and Queues

### Stack (LIFO - Last In, First Out)

**Like a stack of plates:**
- Add to top (push)
- Remove from top (pop)
- Look at top (peek)

**Use cases:**
- Function call stack
- Undo/redo functionality
- Expression evaluation
- Backtracking algorithms

### Implementing a Stack

```python
class Stack:
    """Stack implementation using list."""
    
    def __init__(self):
        self._items = []
    
    def push(self, item) -> None:
        """Add item to top - O(1)."""
        self._items.append(item)
    
    def pop(self):
        """Remove and return top item - O(1)."""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        """Return top item without removing - O(1)."""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty - O(1)."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return size - O(1)."""
        return len(self._items)


# Usage
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)

print(stack.peek())  # 3
print(stack.pop())   # 3
print(stack.pop())   # 2
print(stack.size())  # 1
```

### Queue (FIFO - First In, First Out)

**Like a line at a store:**
- Add to back (enqueue)
- Remove from front (dequeue)

**Use cases:**
- Task scheduling
- Breadth-first search
- Print queue
- Message queues

### Implementing a Queue

```python
from collections import deque


class Queue:
    """Queue implementation using deque."""
    
    def __init__(self):
        self._items = deque()
    
    def enqueue(self, item) -> None:
        """Add item to back - O(1)."""
        self._items.append(item)
    
    def dequeue(self):
        """Remove and return front item - O(1)."""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()
    
    def peek(self):
        """Return front item without removing - O(1)."""
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._items[0]
    
    def is_empty(self) -> bool:
        """Check if queue is empty - O(1)."""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return size - O(1)."""
        return len(self._items)


# Usage
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)

print(queue.dequeue())  # 1 (first in, first out)
print(queue.dequeue())  # 2
print(queue.size())     # 1
```

---

## Lecture 5.4: Hash Tables / Dictionaries

### What is a Hash Table?

A **hash table** stores key-value pairs with fast lookup.

**How it works:**
1. Hash function converts key to array index
2. Value stored at that index
3. Collisions handled (multiple keys hash to same index)

**Time Complexity (average case):**
- Insert: O(1)
- Search: O(1)
- Delete: O(1)

### Python Dictionaries

Python's `dict` is a hash table implementation.

```python
# Creating dictionaries
person = {"name": "Alice", "age": 30}
empty = {}
scores = dict(alice=95, bob=87)

# Accessing - O(1)
name = person["name"]  # "Alice"
age = person.get("age", 0)  # 30, or 0 if not found

# Adding/Modifying - O(1)
person["email"] = "alice@example.com"
person["age"] = 31

# Deleting - O(1)
del person["email"]

# Checking existence - O(1)
if "name" in person:
    print("Name exists")

# Iteration
for key in person:
    print(key, person[key])

for key, value in person.items():
    print(f"{key}: {value}")

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Implementing a Simple Hash Table

```python
class HashTable:
    """Simple hash table implementation."""
    
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key) -> int:
        """Hash function - convert key to index."""
        return hash(key) % self.size
    
    def insert(self, key, value) -> None:
        """Insert key-value pair - O(1) average."""
        index = self._hash(key)
        
        # Check if key already exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)  # Update
                return
        
        # Key doesn't exist, append
        self.table[index].append((key, value))
    
    def get(self, key):
        """Get value by key - O(1) average."""
        index = self._hash(key)
        
        for k, v in self.table[index]:
            if k == key:
                return v
        
        raise KeyError(f"Key '{key}' not found")
    
    def delete(self, key) -> None:
        """Delete key - O(1) average."""
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return
        
        raise KeyError(f"Key '{key}' not found")


# Usage
ht = HashTable()
ht.insert("name", "Alice")
ht.insert("age", 30)

print(ht.get("name"))  # "Alice"
ht.delete("age")
```

---

## Lecture 5.5: Trees

### Binary Tree

A **binary tree** is a hierarchical structure where each node has at most two children.

**Terminology:**
- **Root:** Top node
- **Parent:** Node with children
- **Child:** Node below parent
- **Leaf:** Node with no children
- **Height:** Longest path from root to leaf

### Binary Search Tree (BST)

**Binary Search Tree** property:
- Left child < Parent
- Right child > Parent

**Benefits:**
- Efficient search: O(log n) average
- Ordered traversal

```python
class TreeNode:
    """Node in a binary tree."""
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree implementation."""
    
    def __init__(self):
        self.root = None
    
    def insert(self, data) -> None:
        """Insert value - O(log n) average."""
        if not self.root:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node: TreeNode, data) -> None:
        """Helper for insertion."""
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_recursive(node.right, data)
    
    def search(self, data) -> bool:
        """Search for value - O(log n) average."""
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node: TreeNode, data) -> bool:
        """Helper for search."""
        if node is None:
            return False
        
        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)
    
    def inorder_traversal(self) -> list:
        """Return sorted list of values."""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: TreeNode, result: list) -> None:
        """Helper for inorder traversal (Left, Root, Right)."""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)


# Usage
bst = BinarySearchTree()
bst.insert(5)
bst.insert(3)
bst.insert(7)
bst.insert(1)
bst.insert(9)

print(bst.search(7))  # True
print(bst.search(4))  # False
print(bst.inorder_traversal())  # [1, 3, 5, 7, 9] (sorted!)
```

---

## Exercise 5.1: Implement Stack

Build a Stack class with all operations.

**Requirements:**
- `push(item)` - Add to top
- `pop()` - Remove from top
- `peek()` - View top
- `is_empty()` - Check if empty
- `size()` - Return size
- Raise exceptions for invalid operations

---

## Exercise 5.2: Queue from Two Stacks

Implement a Queue using only two Stack objects.

**Challenge:** How do you achieve O(1) amortized dequeue?

---

## Exercise 5.3: Complete Linked List

Implement a LinkedList with:
- `append(data)`
- `prepend(data)`
- `insert_at(index, data)`
- `delete(data)`
- `find(data)`
- `reverse()`
- `get_middle()`

---

## Exercise 5.4: Binary Search Tree

Implement BST with:
- `insert(value)`
- `search(value)`
- `delete(value)` (challenging!)
- `find_min()`
- `find_max()`
- `inorder_traversal()`
- `preorder_traversal()`
- `postorder_traversal()`

---

## Challenge 5.1: LRU Cache

Implement a Least Recently Used (LRU) Cache.

**Requirements:**
- Fixed capacity
- `get(key)` - Return value, mark as recently used
- `put(key, value)` - Add/update value
- When full, evict least recently used item
- **Both operations must be O(1)**

**Hint:** Use hash table + doubly linked list

---

<a name="module-6"></a>
# MODULE 6: Algorithms

**Duration:** 2-3 weeks  
**Focus:** Searching, sorting, recursion, algorithm analysis

---

## Lecture 6.1: Algorithm Analysis & Big O

### What is Algorithm Analysis?

**Algorithm analysis** measures how an algorithm's performance scales with input size.

### Big O Notation

**Big O** describes the **worst-case** time or space complexity.

**Common Complexities (from best to worst):**
- **O(1)** - Constant: Same time regardless of input size
- **O(log n)** - Logarithmic: Halves problem each step
- **O(n)** - Linear: Time grows linearly with input
- **O(n log n)** - Linearithmic: Efficient sorting algorithms
- **O(n²)** - Quadratic: Nested loops
- **O(2ⁿ)** - Exponential: Recursive without memoization
- **O(n!)** - Factorial: Trying all permutations

### Examples

```python
# O(1) - Constant
def get_first(arr: list):
    return arr[0]  # Always one operation


# O(n) - Linear
def find_max(arr: list) -> int:
    max_val = arr[0]
    for num in arr:  # n operations
        if num > max_val:
            max_val = num
    return max_val


# O(n²) - Quadratic
def bubble_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n):           # n times
        for j in range(n - 1):   # n times
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


# O(log n) - Logarithmic
def binary_search(arr: list, target: int) -> int:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## Lecture 6.2: Searching Algorithms

### Linear Search

**Idea:** Check each element sequentially.

**Time:** O(n)  
**Space:** O(1)

```python
def linear_search(arr: list, target) -> int:
    """Return index of target, or -1 if not found."""
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

### Binary Search

**Idea:** Divide and conquer on sorted array.

**Time:** O(log n)  
**Space:** O(1) iterative, O(log n) recursive

```python
def binary_search_iterative(arr: list, target: int) -> int:
    """Binary search - iterative."""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def binary_search_recursive(arr: list, target: int, left: int = 0, right: int = None) -> int:
    """Binary search - recursive."""
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, right)
    else:
        return binary_search_recursive(arr, target, left, mid - 1)
```

---

## Lecture 6.3: Sorting Algorithms

### Bubble Sort

**Idea:** Repeatedly swap adjacent elements if out of order.

**Time:** O(n²)  
**Space:** O(1)

```python
def bubble_sort(arr: list) -> list:
    """Bubble sort - simple but slow."""
    n = len(arr)
    
    for i in range(n):
        # Flag to optimize - stop if no swaps
        swapped = False
        
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        if not swapped:
            break
    
    return arr
```

### Selection Sort

**Idea:** Find minimum, swap with first unsorted element.

**Time:** O(n²)  
**Space:** O(1)

```python
def selection_sort(arr: list) -> list:
    """Selection sort."""
    n = len(arr)
    
    for i in range(n):
        min_idx = i
        
        # Find minimum in remaining array
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        # Swap minimum to current position
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr
```

### Insertion Sort

**Idea:** Build sorted array one element at a time.

**Time:** O(n²) worst, O(n) best  
**Space:** O(1)

```python
def insertion_sort(arr: list) -> list:
    """Insertion sort - efficient for small/nearly sorted arrays."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Shift elements greater than key to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr
```

### Merge Sort

**Idea:** Divide array in half, sort each half, merge.

**Time:** O(n log n)  
**Space:** O(n)

```python
def merge_sort(arr: list) -> list:
    """Merge sort - efficient divide and conquer."""
    if len(arr) <= 1:
        return arr
    
    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Conquer (merge)
    return merge(left, right)


def merge(left: list, right: list) -> list:
    """Merge two sorted arrays."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result
```

### Quick Sort

**Idea:** Pick pivot, partition around it, recursively sort.

**Time:** O(n log n) average, O(n²) worst  
**Space:** O(log n)

```python
def quick_sort(arr: list) -> list:
    """Quick sort - fast in practice."""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)
```

---

## Lecture 6.4: Recursion

### What is Recursion?

**Recursion:** A function that calls itself.

**Components:**
1. **Base case:** When to stop
2. **Recursive case:** Call itself with smaller problem

### Simple Examples

```python
# Factorial
def factorial(n: int) -> int:
    """Calculate n!"""
    if n == 0:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case


# Fibonacci
def fibonacci(n: int) -> int:
    """Calculate nth Fibonacci number."""
    if n <= 1:  # Base case
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)  # Recursive case


# Sum of list
def sum_list(arr: list) -> int:
    """Sum all elements recursively."""
    if not arr:  # Base case
        return 0
    return arr[0] + sum_list(arr[1:])  # Recursive case
```

### Recursion vs Iteration

**Recursion:**
- Often more elegant
- Matches problem structure (trees, etc.)
- Can cause stack overflow

**Iteration:**
- Usually more efficient
- No stack overflow risk
- Sometimes less intuitive

### Example: Fibonacci Both Ways

```python
# Recursive - elegant but slow O(2^n)
def fib_recursive(n: int) -> int:
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


# Iterative - fast O(n)
def fib_iterative(n: int) -> int:
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


# Recursive with memoization - fast O(n)
def fib_memo(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {}
    
    if n in memo:
        return memo[n]
    
    if n <= 1:
        return n
    
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]
```

---

## Lecture 6.5: Algorithm Patterns

### Two Pointers

**Idea:** Use two pointers moving toward each other.

**Use cases:**
- Palindrome checking
- Finding pairs
- Removing duplicates

```python
def two_sum_sorted(arr: list, target: int) -> tuple:
    """Find two numbers that sum to target in sorted array."""
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if current_sum == target:
            return (arr[left], arr[right])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None
```

### Sliding Window

**Idea:** Maintain a window and slide it across array.

**Use cases:**
- Maximum sum subarray
- Substring problems

```python
def max_sum_subarray(arr: list, k: int) -> int:
    """Find maximum sum of any contiguous subarray of size k."""
    if len(arr) < k:
        return None
    
    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide window
    for i in range(len(arr) - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### Divide and Conquer

**Idea:** Break problem into smaller subproblems, solve recursively.

**Examples:** Merge sort, binary search

---

## Exercise 6.1: Binary Search

Implement binary search both ways:
- Iteratively
- Recursively

Test with sorted arrays.

---

## Exercise 6.2: Merge Sort

Implement merge sort from scratch.

**Requirements:**
- Recursive implementation
- Separate merge function
- Handle edge cases

---

## Exercise 6.3: Two Sum Problem

Given an array and target, find two numbers that sum to target.

**Requirements:**
- Use two pointers if array is sorted
- Use hash table if unsorted
- Return indices, not values

---

## Exercise 6.4: Fibonacci Three Ways

Implement Fibonacci:
1. Recursive (slow)
2. Iterative (fast)
3. Memoized recursive (fast)

Compare performance for n=35.

---

## Challenge 6.1: Maximum Subarray (Kadane's Algorithm)

Find contiguous subarray with largest sum.

**Example:**
```
[-2, 1, -3, 4, -1, 2, 1, -5, 4]
Answer: [4, -1, 2, 1] = 6
```

**Requirement:** O(n) time complexity

---

## Challenge 6.2: Quicksort with Random Pivot

Implement quicksort with random pivot selection.

**Requirements:**
- In-place sorting
- Random pivot to avoid worst case
- Handle duplicates correctly

---

<a name="module-7"></a>
# MODULE 7: SQL and Database Design

**Duration:** 2-3 weeks  
**Focus:** Relational databases, SQL, normalization

---

## Lecture 7.1: Database Fundamentals

### What is a Database?

A **database** is an organized collection of structured data.

**RDBMS (Relational Database Management System):**
- PostgreSQL
- MySQL
- SQLite
- Oracle
- SQL Server

### Key Concepts

**Table:** Collection of related data (like a spreadsheet)
- **Rows:** Individual records
- **Columns:** Attributes/fields

**Example: Users Table**
```
| id | username | email            | age |
|----|----------|------------------|-----|
| 1  | alice    | alice@email.com  | 25  |
| 2  | bob      | bob@email.com    | 30  |
| 3  | charlie  | charlie@email.com| 28  |
```

### Primary Key

**Primary Key:** Unique identifier for each row
- Must be unique
- Cannot be NULL
- Usually an integer ID or UUID

### Foreign Key

**Foreign Key:** References primary key in another table
- Creates relationships between tables
- Enforces referential integrity

**Example:**
```
Orders table has customer_id (foreign key) → Customers table id (primary key)
```

---

## Lecture 7.2: SQL Basics

### CREATE TABLE

```sql
-- Create a table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data types
-- INTEGER, BIGINT - whole numbers
-- DECIMAL(10,2), NUMERIC - exact decimals
-- VARCHAR(n) - variable length string
-- TEXT - unlimited length string
-- BOOLEAN - true/false
-- DATE - date only
-- TIMESTAMP - date and time
-- SERIAL - auto-incrementing integer
```

### INSERT

```sql
-- Insert single row
INSERT INTO users (username, email, age)
VALUES ('alice', 'alice@email.com', 25);

-- Insert multiple rows
INSERT INTO users (username, email, age)
VALUES 
    ('bob', 'bob@email.com', 30),
    ('charlie', 'charlie@email.com', 28);

-- Insert with RETURNING (get back inserted data)
INSERT INTO users (username, email, age)
VALUES ('dave', 'dave@email.com', 35)
RETURNING id, username;
```

### SELECT

```sql
-- Select all columns
SELECT * FROM users;

-- Select specific columns
SELECT username, email FROM users;

-- Select with alias
SELECT username AS name, email AS contact FROM users;

-- Select distinct values
SELECT DISTINCT age FROM users;
```

### WHERE

```sql
-- Filter rows
SELECT * FROM users WHERE age > 25;

-- Multiple conditions (AND)
SELECT * FROM users WHERE age > 25 AND username LIKE 'a%';

-- OR condition
SELECT * FROM users WHERE age < 20 OR age > 60;

-- IN operator
SELECT * FROM users WHERE age IN (25, 30, 35);

-- BETWEEN
SELECT * FROM users WHERE age BETWEEN 25 AND 35;

-- LIKE pattern matching
SELECT * FROM users WHERE username LIKE '%li%';  -- Contains 'li'
SELECT * FROM users WHERE email LIKE '%@gmail.com';  -- Ends with

-- IS NULL
SELECT * FROM users WHERE age IS NULL;
```

### ORDER BY

```sql
-- Sort ascending (default)
SELECT * FROM users ORDER BY age;

-- Sort descending
SELECT * FROM users ORDER BY age DESC;

-- Multiple columns
SELECT * FROM users ORDER BY age DESC, username ASC;
```

### LIMIT

```sql
-- Get first 5 rows
SELECT * FROM users LIMIT 5;

-- Skip first 10, get next 5 (pagination)
SELECT * FROM users LIMIT 5 OFFSET 10;
```

### UPDATE

```sql
-- Update single row
UPDATE users
SET email = 'newemail@email.com'
WHERE id = 1;

-- Update multiple columns
UPDATE users
SET age = 26, email = 'alice_new@email.com'
WHERE username = 'alice';

-- Update multiple rows
UPDATE users
SET age = age + 1
WHERE age < 30;
```

### DELETE

```sql
-- Delete specific row
DELETE FROM users WHERE id = 3;

-- Delete multiple rows
DELETE FROM users WHERE age < 18;

-- Delete all rows (be careful!)
DELETE FROM users;
```

---

## Lecture 7.3: SQL Intermediate

### JOINs

**INNER JOIN:** Return rows that match in both tables

```sql
-- Create related tables
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product VARCHAR(100),
    total DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INNER JOIN - only matching rows
SELECT users.username, orders.product, orders.total
FROM users
INNER JOIN orders ON users.id = orders.user_id;
```

**LEFT JOIN:** All rows from left table, matching rows from right

```sql
-- Get all users and their orders (including users with no orders)
SELECT users.username, orders.product
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

**RIGHT JOIN:** All rows from right table, matching rows from left

```sql
-- Get all orders and their users
SELECT users.username, orders.product
FROM users
RIGHT JOIN orders ON users.id = orders.user_id;
```

**FULL OUTER JOIN:** All rows from both tables

```sql
-- Get all users and all orders
SELECT users.username, orders.product
FROM users
FULL OUTER JOIN orders ON users.id = orders.user_id;
```

### Aggregate Functions

```sql
-- COUNT
SELECT COUNT(*) FROM users;
SELECT COUNT(DISTINCT age) FROM users;

-- SUM
SELECT SUM(total) FROM orders;

-- AVG
SELECT AVG(age) FROM users;

-- MAX, MIN
SELECT MAX(age), MIN(age) FROM users;
```

### GROUP BY

```sql
-- Count orders per user
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id;

-- Total spent per user
SELECT user_id, SUM(total) as total_spent
FROM orders
GROUP BY user_id;

-- With JOIN
SELECT users.username, COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id, users.username;
```

### HAVING

**HAVING:** Filter grouped results (WHERE filters before grouping)

```sql
-- Users with more than 2 orders
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 2;

-- Users who spent more than $100
SELECT user_id, SUM(total) as total_spent
FROM orders
GROUP BY user_id
HAVING SUM(total) > 100;
```

### Subqueries

```sql
-- Find users who have placed orders
SELECT username
FROM users
WHERE id IN (SELECT DISTINCT user_id FROM orders);

-- Find users with above-average age
SELECT username, age
FROM users
WHERE age > (SELECT AVG(age) FROM users);

-- Subquery in FROM clause
SELECT avg_age_group.category, COUNT(*)
FROM (
    SELECT 
        CASE 
            WHEN age < 20 THEN 'teen'
            WHEN age < 30 THEN 'twenties'
            ELSE 'older'
        END as category
    FROM users
) as avg_age_group
GROUP BY avg_age_group.category;
```

---

## Lecture 7.4: Database Design & Normalization

### Entity-Relationship Diagrams

**ERD** shows entities (tables) and relationships.

**Example: Blog System**
```
Users (1) ----< (many) Posts
Posts (1) ----< (many) Comments
Users (many) >----< (many) Tags  [many-to-many]
```

### Relationships

**One-to-Many:**
- One user has many orders
- One customer has many addresses

**Many-to-Many:**
- Students and courses
- Posts and tags
- Requires junction table

**One-to-One:**
- User and profile
- Person and passport

### Normalization

**Goal:** Reduce redundancy and improve data integrity

#### First Normal Form (1NF)

- Each cell contains atomic (single) value
- Each column has unique name
- Each row is unique

**❌ Violates 1NF:**
```
| id | name  | phones               |
|----|-------|----------------------|
| 1  | Alice | 555-1234, 555-5678  |
```

**✅ Follows 1NF:**
```
Users table:
| id | name  |

Phones table:
| id | user_id | phone     |
|----|---------|-----------|
| 1  | 1       | 555-1234  |
| 2  | 1       | 555-5678  |
```

#### Second Normal Form (2NF)

- Must be in 1NF
- All non-key attributes fully dependent on primary key

**❌ Violates 2NF:**
```
| order_id | product_id | product_name | quantity |
|----------|------------|--------------|----------|
| 1        | 100        | Laptop       | 2        |
```
(product_name depends only on product_id, not full key)

**✅ Follows 2NF:**
```
Orders table:
| order_id | product_id | quantity |

Products table:
| product_id | product_name |
```

#### Third Normal Form (3NF)

- Must be in 2NF
- No transitive dependencies

**❌ Violates 3NF:**
```
| id | name  | zip   | city        | state |
|----|-------|-------|-------------|-------|
| 1  | Alice | 12345 | Springfield | IL    |
```
(city and state depend on zip, not directly on id)

**✅ Follows 3NF:**
```
Users table:
| id | name  | zip   |

ZipCodes table:
| zip   | city        | state |
```

### Many-to-Many Relationship

**Example: Students and Courses**

```sql
-- Students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Courses table
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL
);

-- Junction table (enrollments)
CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    grade VARCHAR(2),
    PRIMARY KEY (student_id, course_id)
);

-- Query: Get all courses for a student
SELECT courses.name, enrollments.grade
FROM courses
JOIN enrollments ON courses.id = enrollments.course_id
WHERE enrollments.student_id = 1;

-- Query: Get all students in a course
SELECT students.name, enrollments.grade
FROM students
JOIN enrollments ON students.id = enrollments.student_id
WHERE enrollments.course_id = 101;
```

---

## Lecture 7.5: Constraints and Indexes

### Constraints

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,              -- Cannot be NULL
    sku VARCHAR(50) UNIQUE NOT NULL,         -- Must be unique
    price DECIMAL(10,2) CHECK (price >= 0),  -- Must be >= 0
    category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    stock INTEGER DEFAULT 0                  -- Default value
);
```

**Common Constraints:**
- `NOT NULL` - Value required
- `UNIQUE` - No duplicates
- `PRIMARY KEY` - Unique + Not Null
- `FOREIGN KEY` - Reference another table
- `CHECK` - Custom validation
- `DEFAULT` - Default value

### ON DELETE Options

```sql
-- CASCADE: Delete related rows
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

-- SET NULL: Set to NULL
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL

-- RESTRICT: Prevent deletion (default)
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE RESTRICT

-- NO ACTION: Same as RESTRICT
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE NO ACTION
```

### Indexes

**Index:** Data structure that improves query speed

```sql
-- Create index
CREATE INDEX idx_users_email ON users(email);

-- Composite index
CREATE INDEX idx_orders_user_date ON orders(user_id, order_date);

-- Unique index
CREATE UNIQUE INDEX idx_products_sku ON products(sku);

-- Drop index
DROP INDEX idx_users_email;
```

**When to use indexes:**
- Columns frequently in WHERE clauses
- Columns used in JOINs
- Columns used in ORDER BY

**When NOT to use:**
- Small tables
- Columns with low cardinality (few unique values)
- Tables with frequent INSERT/UPDATE (indexes slow writes)

---

## Lecture 7.6: Transactions

### ACID Properties

**A**tomicity - All or nothing  
**C**onsistency - Data integrity maintained  
**I**solation - Transactions don't interfere  
**D**urability - Changes permanent after commit

### Using Transactions

```sql
-- Begin transaction
BEGIN;

-- Make changes
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Commit (save changes)
COMMIT;

-- Or rollback (undo changes)
ROLLBACK;
```

**Example: Bank Transfer**

```sql
BEGIN;

-- Deduct from sender
UPDATE accounts 
SET balance = balance - 500 
WHERE user_id = 1;

-- Check if balance went negative
SELECT balance FROM accounts WHERE user_id = 1;
-- If negative, ROLLBACK

-- Add to receiver
UPDATE accounts 
SET balance = balance + 500 
WHERE user_id = 2;

COMMIT;
```

---

## Lecture 7.7: Python + PostgreSQL

### Using psycopg2

```python
import psycopg2
from psycopg2.extras import RealDictCursor

# Connect to database
conn = psycopg2.connect(
    dbname="mydb",
    user="postgres",
    password="password",
    host="localhost",
    port=5432
)

# Create cursor
cursor = conn.cursor(cursor_factory=RealDictCursor)

# Execute query
cursor.execute("SELECT * FROM users WHERE age > %s", (25,))

# Fetch results
users = cursor.fetchall()
for user in users:
    print(user['username'], user['email'])

# Insert data (ALWAYS use parameters to prevent SQL injection!)
cursor.execute(
    "INSERT INTO users (username, email, age) VALUES (%s, %s, %s)",
    ('dave', 'dave@email.com', 30)
)

# Commit changes
conn.commit()

# Close
cursor.close()
conn.close()
```

### Connection Management

```python
from contextlib import contextmanager

class Database:
    def __init__(self, dbname, user, password, host='localhost'):
        self.connection_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host
        }
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database cursor."""
        conn = psycopg2.connect(**self.connection_params)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

# Usage
db = Database('mydb', 'postgres', 'password')

with db.get_cursor() as cursor:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
```

### SQL Injection Prevention

```python
# ❌ NEVER DO THIS - SQL Injection vulnerability!
username = "admin' OR '1'='1"
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# ✅ ALWAYS use parameterized queries
username = "admin"
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
```

---

## Exercise 7.1: Library Database Design

### Problem Statement

Design a complete database schema for a library system.

### Requirements

**Tables needed:**
- Books (id, title, isbn, publication_year)
- Authors (id, name, birth_year)
- Members (id, name, email, join_date)
- Loans (id, book_id, member_id, loan_date, return_date)

**Relationships:**
- Books can have multiple authors (many-to-many)
- Members can borrow multiple books
- Track loan history

### Your Task

1. Draw ER diagram
2. Write CREATE TABLE statements
3. Implement all constraints and foreign keys
4. Add appropriate indexes

---

## Exercise 7.2: Complex Queries

### Problem Statement

Write SQL queries for the library system.

### Queries to Write

1. Find all books by a specific author
2. Find all books currently on loan
3. Find members with overdue books (>14 days)
4. Count total books per author
5. Find most popular books (most loans)
6. List members who never borrowed books
7. Calculate average loan duration
8. Find books with multiple authors

---

## Exercise 7.3: Blog Database

### Problem Statement

Design a blog system with tags (many-to-many).

### Requirements

**Tables:**
- Users
- Posts
- Tags
- Comments
- post_tags (junction table)

**Features:**
- Posts belong to users
- Posts can have multiple tags
- Comments belong to posts and users
- Track creation dates

### Your Task

Design schema and write queries:
- Get all posts with a specific tag
- Get all tags for a post
- Get comments for a post with user info
- Find most active commenters

---

## Exercise 7.4: Python Repository Pattern

### Problem Statement

Create a Python repository class for the Users table.

### Requirements

```python
class UserRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def create(self, user: User) -> User:
        """Insert user and return with ID."""
        pass
    
    def find_by_id(self, user_id: int) -> User | None:
        """Find user by ID."""
        pass
    
    def find_by_email(self, email: str) -> User | None:
        """Find user by email."""
        pass
    
    def find_all(self) -> list[User]:
        """Get all users."""
        pass
    
    def update(self, user: User) -> User:
        """Update user."""
        pass
    
    def delete(self, user_id: int) -> bool:
        """Delete user."""
        pass
```

### Your Task

Implement with proper error handling and SQL injection prevention.

---

## Challenge 7.1: Complete E-Commerce Database

### Problem Statement

Design a complete e-commerce database.

### Requirements

**Tables:**
- Users
- Products
- Categories
- Orders
- OrderItems
- Addresses
- Reviews
- Cart

**Features:**
- Products belong to categories
- Orders contain multiple products
- Users can have multiple addresses
- Products can have reviews
- Shopping cart functionality

### Your Task

1. Design normalized schema (3NF)
2. Write 10 complex queries including:
   - Sales reports
   - Product recommendations
   - Customer analytics
   - Inventory management
3. Implement in Python with repository pattern
4. Add transaction handling for orders

---

<a name="module-8"></a>
# MODULE 8: Design Patterns (Gang of Four)

**Duration:** 2-3 weeks  
**Focus:** The 23 classic design patterns

---

## Introduction to Design Patterns

**Design patterns** are reusable solutions to common software design problems.

**The Gang of Four (GoF):** Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides

**Three Categories:**
1. **Creational** - Object creation mechanisms
2. **Structural** - Object composition
3. **Behavioral** - Object interaction and responsibility

---

## CREATIONAL PATTERNS

### Pattern 1: Singleton

**Problem:** Ensure a class has only one instance.

**Use cases:**
- Database connection pool
- Logger
- Configuration manager

```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Database(Singleton):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = "DB Connection"
            self.initialized = True


# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # True - same instance
```

### Pattern 2: Factory Method

**Problem:** Create objects without specifying exact class.

**Use cases:**
- Creating different types of documents
- Payment gateways
- UI components

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


class AnimalFactory:
    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Unknown animal type: {animal_type}")


# Usage
factory = AnimalFactory()
dog = factory.create_animal("dog")
print(dog.speak())  # "Woof!"
```

### Pattern 3: Builder

**Problem:** Construct complex objects step by step.

**Use cases:**
- Building pizzas with toppings
- Creating complex configurations
- SQL query builders

```python
class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
    
    def __str__(self):
        toppings = []
        if self.cheese:
            toppings.append("cheese")
        if self.pepperoni:
            toppings.append("pepperoni")
        if self.mushrooms:
            toppings.append("mushrooms")
        return f"{self.size} pizza with {', '.join(toppings)}"


class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()
    
    def set_size(self, size: str):
        self.pizza.size = size
        return self
    
    def add_cheese(self):
        self.pizza.cheese = True
        return self
    
    def add_pepperoni(self):
        self.pizza.pepperoni = True
        return self
    
    def add_mushrooms(self):
        self.pizza.mushrooms = True
        return self
    
    def build(self) -> Pizza:
        return self.pizza


# Usage - fluent interface
pizza = (PizzaBuilder()
    .set_size("large")
    .add_cheese()
    .add_pepperoni()
    .add_mushrooms()
    .build())

print(pizza)  # "large pizza with cheese, pepperoni, mushrooms"
```

---

## STRUCTURAL PATTERNS

### Pattern 4: Adapter

**Problem:** Make incompatible interfaces work together.

**Use cases:**
- Legacy system integration
- Third-party API integration

```python
# Old interface
class OldPaymentGateway:
    def make_payment(self, amount):
        return f"Old gateway: ${amount}"


# New interface
class NewPaymentGateway:
    def process(self, amount, currency):
        return f"New gateway: {amount} {currency}"


# Adapter
class PaymentAdapter:
    def __init__(self, old_gateway: OldPaymentGateway):
        self.old_gateway = old_gateway
    
    def process(self, amount, currency):
        # Convert new interface to old interface
        return self.old_gateway.make_payment(amount)


# Usage
old = OldPaymentGateway()
adapter = PaymentAdapter(old)
result = adapter.process(100, "USD")  # Works with new interface!
```

### Pattern 5: Decorator

**Problem:** Add responsibilities to objects dynamically.

**Use cases:**
- Adding features to coffee orders
- Adding logging to functions
- Adding validation

```python
from abc import ABC, abstractmethod

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass
    
    @abstractmethod
    def description(self) -> str:
        pass


class SimpleCoffee(Coffee):
    def cost(self) -> float:
        return 2.0
    
    def description(self) -> str:
        return "Simple coffee"


class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self) -> float:
        return self._coffee.cost()
    
    def description(self) -> str:
        return self._coffee.description()


class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.5
    
    def description(self) -> str:
        return self._coffee.description() + ", milk"


class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.2
    
    def description(self) -> str:
        return self._coffee.description() + ", sugar"


# Usage - wrap decorators
coffee = SimpleCoffee()
coffee = Milk(coffee)
coffee = Sugar(coffee)

print(coffee.description())  # "Simple coffee, milk, sugar"
print(f"${coffee.cost()}")   # "$2.7"
```

---

## BEHAVIORAL PATTERNS

### Pattern 6: Strategy

**Problem:** Define family of algorithms, make them interchangeable.

**Use cases:**
- Sorting strategies
- Payment methods
- Compression algorithms

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        # Bubble sort implementation
        return sorted(data)  # Simplified


class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        # Quick sort implementation
        return sorted(data)  # Simplified


class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def sort_data(self, data: list) -> list:
        return self.strategy.sort(data)


# Usage - swap strategies
data = [3, 1, 4, 1, 5, 9, 2, 6]

sorter = Sorter(BubbleSort())
print(sorter.sort_data(data))

sorter = Sorter(QuickSort())
print(sorter.sort_data(data))
```

### Pattern 7: Observer

**Problem:** Notify multiple objects about state changes.

**Use cases:**
- Event handling
- MVC pattern
- Pub/sub systems

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass


class Subject:
    def __init__(self):
        self._observers: list[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)


class EmailNotifier(Observer):
    def update(self, message: str) -> None:
        print(f"Email: {message}")


class SMSNotifier(Observer):
    def update(self, message: str) -> None:
        print(f"SMS: {message}")


# Usage
subject = Subject()
subject.attach(EmailNotifier())
subject.attach(SMSNotifier())

subject.notify("Order placed!")
# Output:
# Email: Order placed!
# SMS: Order placed!
```

### Pattern 8: Command

**Problem:** Encapsulate requests as objects.

**Use cases:**
- Undo/redo functionality
- Transaction systems
- Task queues

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass


class Light:
    def turn_on(self):
        print("Light is ON")
    
    def turn_off(self):
        print("Light is OFF")


class LightOnCommand(Command):
    def __init__(self, light: Light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()


class RemoteControl:
    def __init__(self):
        self.history = []
    
    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)
    
    def undo_last(self):
        if self.history:
            command = self.history.pop()
            command.undo()


# Usage
light = Light()
light_on = LightOnCommand(light)

remote = RemoteControl()
remote.execute_command(light_on)  # Light is ON
remote.undo_last()                # Light is OFF
```

---

## All 23 Patterns Summary

**Creational (5):**
1. Singleton - One instance
2. Factory Method - Create objects
3. Abstract Factory - Families of objects
4. Builder - Complex construction
5. Prototype - Clone objects

**Structural (7):**
6. Adapter - Interface compatibility
7. Bridge - Separate abstraction/implementation
8. Composite - Tree structures
9. Decorator - Add responsibilities
10. Facade - Simplified interface
11. Flyweight - Share objects
12. Proxy - Control access

**Behavioral (11):**
13. Chain of Responsibility - Pass request along chain
14. Command - Encapsulate requests
15. Interpreter - Language grammar
16. Iterator - Sequential access
17. Mediator - Object interactions
18. Memento - Save/restore state
19. Observer - Notify dependents
20. State - Alter behavior based on state
21. Strategy - Interchangeable algorithms
22. Template Method - Algorithm skeleton
23. Visitor - Operations on elements

---

## Exercise 8.1-8.8

Each exercise focuses on implementing one pattern. Use UMPIRE method.

---

## Challenge 8.1: Multi-Pattern System

Design a notification system using:
- Factory (create notifiers)
- Strategy (formatting)
- Observer (subscribers)
- Decorator (add features)

---

<a name="module-9"></a>
# MODULE 9: Testing and Test-Driven Development

**Duration:** 1-2 weeks  
**Focus:** pytest, TDD, mocking

---

## Lecture 9.1: Why Test?

### Benefits of Testing

**Catch bugs early:** Before production  
**Confidence to refactor:** Tests verify nothing broke  
**Documentation:** Tests show how to use code  
**Better design:** Testable code is better code

### Test Pyramid

```
       /\
      /  \  E2E Tests (Few)
     /----\
    /      \ Integration Tests (Some)
   /--------\
  /          \ Unit Tests (Many)
 /____________\
```

---

## Lecture 9.2: Unit Testing with pytest

### Basic Test

```python
# calculator.py
def add(a: int, b: int) -> int:
    return a + b


# test_calculator.py
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest test_calculator.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=mymodule
```

### Assertions

```python
def test_assertions():
    # Equality
    assert 1 + 1 == 2
    
    # Inequality
    assert 5 != 6
    
    # Boolean
    assert True
    assert not False
    
    # Membership
    assert 'a' in 'abc'
    
    # Type checking
    assert isinstance(5, int)
    
    # Exceptions
    import pytest
    with pytest.raises(ValueError):
        int('invalid')
```

### Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    """Provide test data."""
    return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_max(sample_data):
    assert max(sample_data) == 5
```

### Parametrized Tests

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

---

## Lecture 9.3: Test-Driven Development (TDD)

### The TDD Cycle

**Red-Green-Refactor:**

1. **RED:** Write failing test
2. **GREEN:** Write minimum code to pass
3. **REFACTOR:** Improve code quality

### TDD Example: FizzBuzz

```python
# Step 1: RED - Write failing test
def test_fizzbuzz_returns_1_for_1():
    assert fizzbuzz(1) == "1"

# Step 2: GREEN - Minimum code to pass
def fizzbuzz(n):
    return "1"

# Step 3: Add more tests
def test_fizzbuzz_returns_fizz_for_3():
    assert fizzbuzz(3) == "Fizz"

# Step 4: Implement
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    return str(n)

# Continue...
def test_fizzbuzz_returns_buzz_for_5():
    assert fizzbuzz(5) == "Buzz"

def test_fizzbuzz_returns_fizzbuzz_for_15():
    assert fizzbuzz(15) == "FizzBuzz"

# Final implementation
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

---

## Lecture 9.4: Mocking

### Why Mock?

**Mock external dependencies:**
- Databases
- APIs
- File systems
- Time-dependent code

```python
from unittest.mock import Mock, patch

# Mock object
def test_with_mock():
    mock_db = Mock()
    mock_db.get_user.return_value = {"id": 1, "name": "Alice"}
    
    result = mock_db.get_user(1)
    assert result["name"] == "Alice"
    mock_db.get_user.assert_called_once_with(1)


# Patch function
def get_data_from_api():
    # Expensive API call
    pass

@patch('module.get_data_from_api')
def test_api_call(mock_api):
    mock_api.return_value = {"data": "test"}
    
    result = get_data_from_api()
    assert result["data"] == "test"
```

---

## Exercise 9.1-9.3

Practice TDD and mocking with various exercises.

---

<a name="final-project"></a>
# FINAL PROJECT: Pizza Restaurant System

**Duration:** 2-3 weeks  
**Apply everything you've learned!**

---

## Project Requirements

### Core Features

**Models (OOP):**
- Customer
- Pizza
- Topping
- Order

**Services (SOLID):**
- OrderService
- MenuService
- PricingService

**Data Layer (SQL):**
- Repository pattern
- PostgreSQL database
- Raw SQL queries

**Design Patterns:**
- Builder (Pizza construction)
- Factory (Create pizza types)
- Strategy (Pricing strategies)
- Observer (Order notifications - bonus)

**CLI Interface:**
- User-friendly menu
- Create orders
- View menu
- Order history

**Testing:**
- Unit tests (models, services)
- Integration tests (repositories)
- Mocks for external dependencies
- 80%+ coverage

---

## Database Schema

```sql
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE pizzas (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    size VARCHAR(20) NOT NULL,
    crust_type VARCHAR(50) NOT NULL,
    base_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE toppings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE pizza_toppings (
    pizza_id INTEGER REFERENCES pizzas(id) ON DELETE CASCADE,
    topping_id INTEGER REFERENCES toppings(id),
    PRIMARY KEY (pizza_id, topping_id)
);
```

---

## Deliverables

1. **Complete Python implementation**
2. **Test suite (all passing)**
3. **Database schema + seed data**
4. **README with setup instructions**
5. **Architecture document explaining:**
   - OOP design choices
   - SOLID principles applied
   - Design patterns used
   - Database design decisions

---

<a name="resources"></a>
# RESOURCES AND REFERENCES

## Python Resources

- Python Official Docs: https://docs.python.org
- Real Python: https://realpython.com
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- Python Tutor (visualize code): https://pythontutor.com

## OOP & Design

- Clean Code by Robert C. Martin
- Design Patterns (GoF Book)
- Refactoring by Martin Fowler
- SOLID Principles explanations

## Data Structures & Algorithms

- VisuAlgo: https://visualgo.net
- Big-O Cheat Sheet: https://bigocheatsheet.com
- LeetCode: https://leetcode.com
- HackerRank: https://hackerrank.com

## SQL

- PostgreSQL Documentation
- SQLBolt: https://sqlbolt.com
- Mode Analytics SQL Tutorial

## Testing

- pytest Documentation
- Test-Driven Development by Kent Beck

---

<a name="progress-tracking"></a>
# PROGRESS TRACKING

## Module 4: SOLID Principles
- [ ] Exercise 4.1 - Refactor for SRP
- [ ] Exercise 4.2 - Discount System (OCP)
- [ ] Exercise 4.3 - Dependency Injection (DIP)
- [ ] Challenge 4.1 - Notification System

## Module 5: Data Structures
- [ ] Exercise 5.1 - Stack Implementation
- [ ] Exercise 5.2 - Queue from Stacks
- [ ] Exercise 5.3 - LinkedList
- [ ] Exercise 5.4 - Binary Search Tree
- [ ] Challenge 5.1 - LRU Cache

## Module 6: Algorithms
- [ ] Exercise 6.1 - Binary Search
- [ ] Exercise 6.2 - Merge Sort
- [ ] Exercise 6.3 - Two Sum
- [ ] Exercise 6.4 - Fibonacci Three Ways
- [ ] Challenge 6.1 - Maximum Subarray
- [ ] Challenge 6.2 - Quicksort

## Module 7: SQL
- [ ] Exercise 7.1 - Library Database
- [ ] Exercise 7.2 - Complex Queries
- [ ] Exercise 7.3 - Blog Database
- [ ] Exercise 7.4 - Python Repository
- [ ] Challenge 7.1 - E-Commerce Database

## Module 8: Design Patterns
- [ ] Exercise 8.1 - Singleton
- [ ] Exercise 8.2 - Factory Method
- [ ] Exercise 8.3 - Strategy
- [ ] Exercise 8.4 - Observer
- [ ] Exercise 8.5 - Decorator
- [ ] Exercise 8.6 - Builder
- [ ] Exercise 8.7 - Adapter
- [ ] Exercise 8.8 - Command
- [ ] Challenge 8.1 - Multi-Pattern System
- [ ] Challenge 8.2 - Refactoring

## Module 9: Testing
- [ ] Exercise 9.1 - Unit Tests
- [ ] Exercise 9.2 - TDD Practice
- [ ] Exercise 9.3 - Mocking
- [ ] Challenge 9.1 - Integration Tests

## Final Project
- [ ] Design architecture
- [ ] Implement models
- [ ] Implement services
- [ ] Implement repositories
- [ ] Create database schema
- [ ] Build CLI interface
- [ ] Write comprehensive tests
- [ ] Document everything

---

**END OF PART 2**

**Remember:** This is a marathon, not a sprint. Master each concept before moving on!

**Good luck with your journey to becoming a professional developer! 🚀**