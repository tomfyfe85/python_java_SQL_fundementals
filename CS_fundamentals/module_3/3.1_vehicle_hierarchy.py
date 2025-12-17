"""
Exercise 3.1: Vehicle Hierarchy

INTRODUCTION TO INHERITANCE:

INHERITANCE is when a class (child/subclass) inherits attributes and methods
from another class (parent/superclass).

Think of it like family genetics:
- A parent has certain traits (attributes) and abilities (methods)
- Children inherit those traits and abilities
- Children can also have their own unique traits
- Children can modify inherited abilities (method overriding)

IS-A RELATIONSHIP:
Inheritance represents an "IS-A" relationship:
- A Car IS-A Vehicle
- A Motorcycle IS-A Vehicle
- A Truck IS-A Vehicle

THE super() FUNCTION:
- Calls methods from the parent class
- Commonly used in __init__ to call parent constructor
- Allows you to extend parent functionality rather than replace it

EXAMPLE:
    class Vehicle:
        def __init__(self, make, model):
            self.make = make
            self.model = model

    class Car(Vehicle):  # Car inherits from Vehicle
        def __init__(self, make, model, num_doors):
            super().__init__(make, model)  # Call parent constructor
            self.num_doors = num_doors

METHOD OVERRIDING:
- Subclass can provide its own implementation of a parent method
- Use super() to extend rather than completely replace

===================================
EXERCISE 3.1: Vehicle Hierarchy
===================================

Create an inheritance hierarchy for different types of vehicles.

REQUIREMENTS:

Base Class: Vehicle

Attributes:
- make (str): The manufacturer/brand of the vehicle
- model (str): The model name of the vehicle
- year (int): The year the vehicle was manufactured

Methods:
- __init__(make, model, year): Constructor
- describe(): Returns a string description of the vehicle
- start(): Simulates starting the vehicle
- stop(): Simulates stopping the vehicle

---

Subclass: Car (inherits from Vehicle)

Additional Attributes:
- num_doors (int): The number of doors on the car

Overridden Methods:
- describe(): Override to include the number of doors in the description

---

Subclass: Motorcycle (inherits from Vehicle)

Additional Attributes:
- engine_cc (int): Engine displacement in cubic centimeters

Overridden Methods:
- describe(): Override to include the engine size in the description

---

Subclass: Truck (inherits from Vehicle)

Additional Attributes:
- cargo_capacity (float): Maximum payload capacity in tons

Overridden Methods:
- describe(): Override to include the cargo capacity in the description

---

Validation Rules:
- make cannot be empty
- model cannot be empty
- year must be between 1900 and current year + 1
- num_doors must be positive (typically 2-5)
- engine_cc must be positive
- cargo_capacity must be positive

EXAMPLES:

# Create instances
car = Car("Toyota", "Camry", 2023, num_doors=4)
motorcycle = Motorcycle("Harley-Davidson", "Street 750", 2022, engine_cc=750)
truck = Truck("Ford", "F-150", 2023, cargo_capacity=3.5)

# Using methods
print(car.describe())        # 2023 Toyota Camry (4 doors)
print(motorcycle.describe()) # 2022 Harley-Davidson Street 750 (750cc)
print(truck.describe())      # 2023 Ford F-150 (3.5 tons capacity)

car.start()  # Starting 2023 Toyota Camry
car.stop()   # Stopping 2023 Toyota Camry

YOUR TASK:
1. Implement the Vehicle base class with all required methods
2. Implement Car, Motorcycle, and Truck subclasses
3. Use super() to call parent constructors
4. Override describe() in each subclass to add specific details
5. Add comprehensive validation and error handling
6. Test with the provided test cases
"""

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================

# Methods:
# - __init__(make, model, year): Constructor
# - describe(): Returns a string description of the vehicle
# - start(): Simulates starting the vehicle
# - stop(): Simulates stopping the vehicle


class Vehicle:
    """Base class for all vehicles"""
    def __init__(self, make:str, model:str, year:int) -> None:
        self.make = make
        self.model = model
        self.year = year

    def describe(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    """Car subclass with door count"""
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        self._num_doors = num_doors
        
    def describe(self):
        return f"{self.year} {self.make} {self.model} ({self._num_doors} doors)"


class Motorcycle(Vehicle):
    """Motorcycle subclass with engine size"""
    pass


class Truck(Vehicle):
    """Truck subclass with cargo capacity"""
    pass


# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing Vehicle Creation ===")

    # Test 1: Create basic vehicle
    vehicle = Vehicle("Honda", "Civic", 2022)
    print(vehicle.describe())  # 2022 Honda Civic

    print("\n=== Testing Car ===")
    car = Car("Toyota", "Camry", 2023, num_doors=4)
    print(car.describe())  # 2023 Toyota Camry (4 doors)
    assert isinstance(car, Vehicle)  # Car IS-A Vehicle

    # print("\n=== Testing Motorcycle ===")
    # motorcycle = Motorcycle("Harley-Davidson", "Street 750", 2022, engine_cc=750)
    # print(motorcycle.describe())  # 2022 Harley-Davidson Street 750 (750cc)
    # assert isinstance(motorcycle, Vehicle)  # Motorcycle IS-A Vehicle

    # print("\n=== Testing Truck ===")
    # truck = Truck("Ford", "F-150", 2023, cargo_capacity=3.5)
    # print(truck.describe())  # 2023 Ford F-150 (3.5 tons capacity)
    # assert isinstance(truck, Vehicle)  # Truck IS-A Vehicle

    # print("\n=== Testing Start/Stop ===")
    # car.start()  # Starting 2023 Toyota Camry
    # car.stop()   # Stopping 2023 Toyota Camry

    # motorcycle.start()  # Starting 2022 Harley-Davidson Street 750
    # motorcycle.stop()   # Stopping 2022 Harley-Davidson Street 750

    # print("\n=== Testing Error Handling ===")

    # # Test empty make
    # try:
    #     bad_vehicle = Vehicle("", "Model", 2023)
    #     print("❌ FAIL: Should raise ValueError for empty make")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test empty model
    # try:
    #     bad_vehicle = Vehicle("Make", "", 2023)
    #     print("❌ FAIL: Should raise ValueError for empty model")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test invalid year (too old)
    # try:
    #     bad_vehicle = Vehicle("Make", "Model", 1899)
    #     print("❌ FAIL: Should raise ValueError for year < 1900")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test invalid year (too new)
    # try:
    #     bad_vehicle = Vehicle("Make", "Model", 2030)
    #     print("❌ FAIL: Should raise ValueError for year > current + 1")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test negative doors
    # try:
    #     bad_car = Car("Toyota", "Camry", 2023, num_doors=-2)
    #     print("❌ FAIL: Should raise ValueError for negative doors")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test zero doors
    # try:
    #     bad_car = Car("Toyota", "Camry", 2023, num_doors=0)
    #     print("❌ FAIL: Should raise ValueError for zero doors")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test negative engine_cc
    # try:
    #     bad_motorcycle = Motorcycle("Yamaha", "R1", 2023, engine_cc=-500)
    #     print("❌ FAIL: Should raise ValueError for negative engine_cc")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # # Test negative cargo capacity
    # try:
    #     bad_truck = Truck("Ford", "F-150", 2023, cargo_capacity=-1.5)
    #     print("❌ FAIL: Should raise ValueError for negative cargo_capacity")
    # except ValueError as e:
    #     print(f"✓ ValueError: {e}")

    # print("\n=== Testing Inheritance ===")
    # print(f"Car is a Vehicle: {isinstance(car, Vehicle)}")
    # print(f"Motorcycle is a Vehicle: {isinstance(motorcycle, Vehicle)}")
    # print(f"Truck is a Vehicle: {isinstance(truck, Vehicle)}")

    # print("\n✓ All tests passed!")
