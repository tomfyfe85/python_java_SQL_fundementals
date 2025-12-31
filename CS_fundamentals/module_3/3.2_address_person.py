"""
Exercise 3.2: Address and Person

INTRODUCTION TO COMPOSITION:

COMPOSITION is when a class contains instances of other classes as attributes.
This represents a "HAS-A" relationship.

Think of it like building with LEGO:
- A house is built FROM bricks (composition)
- A house HAS-A door, HAS-A roof, HAS-A foundation
- Each component is a separate object
- The house object contains these component objects

COMPOSITION vs INHERITANCE:

INHERITANCE (IS-A):
- Car IS-A Vehicle
- Use when there's a parent-child relationship
- Subclass extends parent class

COMPOSITION (HAS-A):
- Person HAS-AN Address
- Car HAS-AN Engine
- Use when one object is MADE UP OF other objects
- Objects collaborate but are independent

EXAMPLE:
    class Engine:
        def __init__(self, horsepower):
            self.horsepower = horsepower

    class Car:
        def __init__(self, make, model, engine):
            self.make = make
            self.model = model
            self.engine = engine  # Car HAS-AN Engine (composition)

    # Create components separately
    v8_engine = Engine(450)
    car = Car("Ford", "Mustang", v8_engine)

    print(car.engine.horsepower)  # Access nested object: 450

WHEN TO USE COMPOSITION:
- Objects are independent but work together
- You want to build complex objects from simpler ones
- Relationship is "part of" or "contains"
- You want flexibility to swap components

===================================
EXERCISE 3.2: Address and Person
===================================

Create two classes that demonstrate composition: Address and Person.
A Person HAS-AN Address.

REQUIREMENTS:

Class: Address

Attributes:
- street (str): Street address
- city (str): City name
- state (str): State/province (2 characters)
- zip_code (str): ZIP/postal code

Methods:
- __init__(street, city, state, zip_code): Constructor
- __str__(): Return formatted address

Validation Rules:
- street cannot be empty
- city cannot be empty
- state must be exactly 2 uppercase letters
- zip_code must be exactly 5 digits

---

Class: Person

Attributes:
- name (str): Person's full name
- age (int): Person's age
- address (Address): Person's address object

Methods:
- __init__(name, age, address): Constructor
- get_full_info(): Return complete person info including address
- move(new_address): Update person's address
- __str__(): Return string representation

Validation Rules:
- name cannot be empty
- age must be between 0 and 150
- address must be an Address object

EXAMPLES:

# Create an address
home = Address("123 Main St", "Springfield", "IL", "62701")
print(home)  # 123 Main St, Springfield, IL 62701

# Create a person with that address
person = Person("Alice Smith", 30, home)
print(person.get_full_info())
# Alice Smith, 30 years old
# Address: 123 Main St, Springfield, IL 62701

# Move to a new address
new_home = Address("456 Oak Ave", "Chicago", "IL", "60601")
person.move(new_home)
print(person.get_full_info())
# Alice Smith, 30 years old
# Address: 456 Oak Ave, Chicago, IL 60601

YOUR TASK:
1. Implement the Address class with validation
2. Implement the Person class that uses Address (composition)
3. Test with the provided test cases
"""

# ==========================================
# YOUR CODE GOES BELOW
# Attributes:
# - street (str): Street address
# - city (str): City name
# - state (str): State/province (2 characters)
# - zip_code (str): ZIP/postal code

# Methods:
# - __init__(street, city, state, zip_code): Constructor
# - __str__(): Return formatted address

# ==========================================

class Address():
    """Represents an American address"""
    def __init__(self, street:str, city:str, state:str, zip_code:str):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __str__(self):
        """Returns a string representation of the class attributes"""
        return f"{self.street}, {self.city}, {self.state} {self.zip_code}"
    
class Person():
    """Name, age, and address of a person"""
    def __init__(self, name:str, age:int, address: Address):
        self.name = name
        self.age = age
        self.address = address

    def get_full_info(self):
        """Returns full details of the person, inc address"""
        return f"{self.__str__()} \nAddress: {self.address.__str__()}"

    def __str__(self):
        return f"{self.name}, {self.age} years old"
    
# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing Address Creation ===")

    # Test 1: Create valid address
    addr1 = Address("123 Main St", "Springfield", "IL", "62701")
    print(addr1)  # 123 Main St, Springfield, IL 62701

    addr2 = Address("456 Oak Ave", "Chicago", "IL", "60601")
    print(addr2)  # 456 Oak Ave, Chicago, IL 60601

    print("\n=== Testing Person Creation ===")

    # Test 2: Create person with address
    person1 = Person("Alice Smith", 30, addr1)
    print(person1)  # Alice Smith, 30 years old

    # Test 3: Get full info (includes address)
    print("\n=== Testing Full Info ===")
    print(person1.get_full_info())
    # Alice Smith, 30 years old
    # Address: 123 Main St, Springfield, IL 62701

    # # Test 4: Move to new address
    # print("\n=== Testing Move ===")
    # person1.move(addr2)
    # print(person1.get_full_info())
    # # Alice Smith, 30 years old
    # # Address: 456 Oak Ave, Chicago, IL 60601

    # # Test 5: Create another person with same address
    # person2 = Person("Bob Jones", 45, addr2)
    # print(person2.get_full_info())
    # # Bob Jones, 45 years old
    # # Address: 456 Oak Ave, Chicago, IL 60601

    # print("\n=== Testing Address Validation ===")

    # # Test empty street
    # try:
    #     bad_addr = Address("", "City", "IL", "12345")
    #     print("❌ FAIL: Should raise ValueError for empty street")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test empty city
    # try:
    #     bad_addr = Address("123 Main St", "", "IL", "12345")
    #     print("❌ FAIL: Should raise ValueError for empty city")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test invalid state (not 2 chars)
    # try:
    #     bad_addr = Address("123 Main St", "City", "Illinois", "12345")
    #     print("❌ FAIL: Should raise ValueError for invalid state")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test invalid state (not uppercase)
    # try:
    #     bad_addr = Address("123 Main St", "City", "il", "12345")
    #     print("❌ FAIL: Should raise ValueError for non-uppercase state")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test invalid zip_code (not 5 digits)
    # try:
    #     bad_addr = Address("123 Main St", "City", "IL", "123")
    #     print("❌ FAIL: Should raise ValueError for invalid zip_code")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test invalid zip_code (not digits)
    # try:
    #     bad_addr = Address("123 Main St", "City", "IL", "ABCDE")
    #     print("❌ FAIL: Should raise ValueError for non-digit zip_code")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # print("\n=== Testing Person Validation ===")

    # # Test empty name
    # try:
    #     bad_person = Person("", 30, addr1)
    #     print("❌ FAIL: Should raise ValueError for empty name")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test negative age
    # try:
    #     bad_person = Person("John Doe", -5, addr1)
    #     print("❌ FAIL: Should raise ValueError for negative age")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test age too high
    # try:
    #     bad_person = Person("John Doe", 200, addr1)
    #     print("❌ FAIL: Should raise ValueError for age > 150")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test invalid address type
    # try:
    #     bad_person = Person("John Doe", 30, "123 Main St")
    #     print("❌ FAIL: Should raise TypeError for non-Address object")
    # except TypeError as e:
    #     print(f"✓ TypeError: {e}")

    # print("\n=== Testing Composition ===")
    # print(f"Person's address city: {person1.address.city}")  # Chicago
    # print(f"Person's address state: {person1.address.state}")  # IL
    # print(f"Person's address is an Address object: {isinstance(person1.address, Address)}")  # True

    # print("\n✓ All tests passed!")