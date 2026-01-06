"""
Exercise 4.1: Single Responsibility Principle (SRP)

SOLID PRINCIPLES - Introduction

SOLID is an acronym for five design principles that make software more maintainable:
- S: Single Responsibility Principle
- O: Open/Closed Principle
- L: Liskov Substitution Principle
- I: Interface Segregation Principle
- D: Dependency Inversion Principle

This exercise focuses on the 'S' - Single Responsibility Principle.

===================================
SINGLE RESPONSIBILITY PRINCIPLE
===================================

Definition: A class should have ONE reason to change.

In other words:
- Each class should do ONE thing and do it well
- If a class has multiple responsibilities, changes to one responsibility affect the other
- Leads to tight coupling and makes code hard to maintain and test

EXAMPLE OF VIOLATION:

    class User:
        def __init__(self, email, password):
            self.email = email
            self.password = password

        def save_to_database(self):
            # Database logic here - RESPONSIBILITY 1
            pass

        def send_welcome_email(self):
            # Email logic here - RESPONSIBILITY 2
            pass

        def validate_email(self):
            # Validation logic here - RESPONSIBILITY 3
            pass

Why is this bad?
1. If database structure changes -> User class changes
2. If email service changes -> User class changes
3. If validation rules change -> User class changes
4. Hard to test (need to mock database AND email service)
5. Violates separation of concerns

REFACTORED WITH SRP:

    class User:
        def __init__(self, email, password):
            self.email = email
            self.password = password

    class UserRepository:
        def save(self, user):
            # Database logic
            pass

    class EmailService:
        def send_welcome_email(self, user):
            # Email logic
            pass

    class EmailValidator:
        def validate(self, email):
            # Validation logic
            pass

Now:
- User: Represents user data (ONE responsibility)
- UserRepository: Handles database operations (ONE responsibility)
- EmailService: Handles email sending (ONE responsibility)
- EmailValidator: Handles validation (ONE responsibility)

Each class has ONE reason to change!

===================================
EXERCISE: Refactor Messy User Class
===================================

Below is a MESSY User class that violates SRP.
Your task is to refactor it into separate classes following SRP.

MESSY CLASS (DO NOT MODIFY - READ ONLY):

class MessyUser:
    '''A user class that does way too much!'''

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.is_saved = False

    def validate_username(self):
        '''Validates username is not empty and length 3-20'''
        if not self.username:
            raise ValueError("Username cannot be empty")
        if len(self.username) < 3 or len(self.username) > 20:
            raise ValueError("Username must be 3-20 characters")
        return True

    def validate_email(self):
        '''Validates email contains @ symbol'''
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        return True

    def validate_password(self):
        '''Validates password is at least 8 characters'''
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return True

    def save_to_database(self):
        '''Simulates saving to database'''
        # Validate before saving
        self.validate_username()
        self.validate_email()
        self.validate_password()

        # Simulate database save
        print(f"Saving user {self.username} to database...")
        self.is_saved = True
        return True

    def send_welcome_email(self):
        '''Simulates sending welcome email'''
        print(f"Sending welcome email to {self.email}...")
        print(f"Subject: Welcome {self.username}!")
        print("Body: Thanks for joining us!")
        return True

    def to_dict(self):
        '''Converts user to dictionary'''
        return {
            "username": self.username,
            "email": self.email,
            "is_saved": self.is_saved
        }

Problems with MessyUser:
1. Handles validation (3 different validations!)
2. Handles database operations
3. Handles email sending
4. Handles data serialization
= 4+ different responsibilities!

YOUR TASK:

Refactor into FOUR separate classes:

1. User (data class)
   - Attributes: username, email, password
   - Methods: __init__ only
   - Responsibility: Hold user data

2. UserValidator
   - Methods: validate_username(username), validate_email(email), validate_password(password)
   - Responsibility: Validate user data
   - Each method raises ValueError if invalid, returns True if valid

3. UserRepository
   - Methods: save(user: User) -> bool
   - Responsibility: Save users to database (simulated with print)
   - Should validate before saving using UserValidator
   - Returns True if saved successfully

4. EmailService
   - Methods: send_welcome_email(user: User) -> bool
   - Responsibility: Send emails
   - Returns True if email sent successfully

BENEFITS OF REFACTORING:
- Each class has ONE clear responsibility
- Easy to test (can test validation without database/email)
- Easy to modify (change email provider without touching User)
- Easy to reuse (UserValidator can validate users anywhere)
- Better organization and readability

"""

# ==========================================
# MESSY CODE (DO NOT MODIFY - READ ONLY)
# ==========================================

class MessyUser:
    """A user class that does way too much!"""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.is_saved = False

    def validate_username(self):
        """Validates username is not empty and length 3-20"""
        if not self.username:
            raise ValueError("Username cannot be empty")
        if len(self.username) < 3 or len(self.username) > 20:
            raise ValueError("Username must be 3-20 characters")
        return True

    def validate_email(self):
        """Validates email contains @ symbol"""
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        return True

    def validate_password(self):
        """Validates password is at least 8 characters"""
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        return True

    def save_to_database(self):
        """Simulates saving to database"""
        self.validate_username()
        self.validate_email()
        self.validate_password()

        print(f"Saving user {self.username} to database...")
        self.is_saved = True
        return True

    def send_welcome_email(self):
        """Simulates sending welcome email"""
        print(f"Sending welcome email to {self.email}...")
        print(f"Subject: Welcome {self.username}!")
        print("Body: Thanks for joining us!")
        return True

    def to_dict(self):
        """Converts user to dictionary"""
        return {
            "username": self.username,
            "email": self.email,
            "is_saved": self.is_saved
        }


# ==========================================
# YOUR REFACTORED CODE GOES HERE
# ==========================================




# ==========================================
# TESTS
# ==========================================

if __name__ == "__main__":
    print("=== Test 1: User class (data only) ===")
    user = User("alice", "alice@example.com", "password123")
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.password == "password123"
    print("✓ User class stores data correctly")

    print("\n=== Test 2: UserValidator - valid data ===")
    validator = UserValidator()
    assert validator.validate_username("alice") == True
    assert validator.validate_email("alice@example.com") == True
    assert validator.validate_password("password123") == True
    print("✓ UserValidator accepts valid data")

    print("\n=== Test 3: UserValidator - invalid username (empty) ===")
    try:
        validator.validate_username("")
        print("❌ FAIL: Should reject empty username")
    except ValueError as e:
        print(f"✓ Rejected empty username: {e}")

    print("\n=== Test 4: UserValidator - invalid username (too short) ===")
    try:
        validator.validate_username("ab")
        print("❌ FAIL: Should reject username < 3 chars")
    except ValueError as e:
        print(f"✓ Rejected short username: {e}")

    print("\n=== Test 5: UserValidator - invalid username (too long) ===")
    try:
        validator.validate_username("a" * 21)
        print("❌ FAIL: Should reject username > 20 chars")
    except ValueError as e:
        print(f"✓ Rejected long username: {e}")

    print("\n=== Test 6: UserValidator - invalid email ===")
    try:
        validator.validate_email("notanemail")
        print("❌ FAIL: Should reject email without @")
    except ValueError as e:
        print(f"✓ Rejected invalid email: {e}")

    print("\n=== Test 7: UserValidator - invalid password ===")
    try:
        validator.validate_password("short")
        print("❌ FAIL: Should reject password < 8 chars")
    except ValueError as e:
        print(f"✓ Rejected short password: {e}")

    print("\n=== Test 8: UserRepository - save valid user ===")
    user = User("bob", "bob@example.com", "securepass")
    repo = UserRepository()
    result = repo.save(user)
    assert result == True
    print("✓ UserRepository saved valid user")

    print("\n=== Test 9: UserRepository - reject invalid user ===")
    invalid_user = User("x", "invalid", "123")
    try:
        repo.save(invalid_user)
        print("❌ FAIL: Should reject invalid user")
    except ValueError as e:
        print(f"✓ UserRepository rejected invalid user: {e}")

    print("\n=== Test 10: EmailService ===")
    user = User("charlie", "charlie@example.com", "mypassword")
    email_service = EmailService()
    result = email_service.send_welcome_email(user)
    assert result == True
    print("✓ EmailService sent welcome email")

    print("\n=== Test 11: Separation of concerns ===")
    # Each class can be used independently
    validator = UserValidator()
    assert validator.validate_email("test@test.com") == True
    print("✓ UserValidator works independently")

    repo = UserRepository()
    user = User("dave", "dave@example.com", "password1")
    repo.save(user)
    print("✓ UserRepository works independently")

    email = EmailService()
    email.send_welcome_email(user)
    print("✓ EmailService works independently")

    print("\n✓ All tests passed!")
    print("\n=== SRP Benefits Demonstrated ===")
    print("1. Each class has ONE clear responsibility")
    print("2. Classes can be tested independently")
    print("3. Changes to one class don't affect others")
    print("4. Easy to extend (e.g., add new validators)")