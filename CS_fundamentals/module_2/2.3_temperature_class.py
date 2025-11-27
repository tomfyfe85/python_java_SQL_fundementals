"""
Exercise 2.3: Enhanced Temperature Class

INTRODUCTION TO PROPERTIES:

Properties allow you to use methods like attributes. They provide:
1. Controlled access to private data
2. Automatic calculations when getting/setting values
3. Validation when setting values

EXAMPLE - Without Properties (verbose):
    temp = Temperature(25)
    print(temp.get_fahrenheit())  # Method call
    temp.set_fahrenheit(77)       # Method call

EXAMPLE - With Properties (clean):
    temp = Temperature(25)
    print(temp.fahrenheit)  # Looks like an attribute!
    temp.fahrenheit = 77    # Looks like assignment!

HOW PROPERTIES WORK:

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius  # Store internally

    @property
    def fahrenheit(self):
        \"\"\"Getter - called when you access temp.fahrenheit\"\"\"
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        \"\"\"Setter - called when you do temp.fahrenheit = value\"\"\"
        self._celsius = (value - 32) * 5/9

Usage:
    temp = Temperature(0)
    print(temp.fahrenheit)  # Calls the getter, returns 32.0
    temp.fahrenheit = 212   # Calls the setter, converts to Celsius internally
    print(temp._celsius)    # 100.0

KEY POINTS:
- @property decorator makes a method act like a getter
- @property_name.setter makes a method act like a setter
- Naming convention: _private_attribute for internal storage
- Properties provide automatic conversion/validation

===================================
EXERCISE 2.3: Temperature Class
===================================

Create a Temperature class that stores a temperature and provides automatic
conversion between Celsius and Fahrenheit.

REQUIREMENTS:

Class: Temperature

Attributes:
- Store temperature internally in Celsius (use _celsius)

Methods:
- __init__(value, unit='C'): Constructor accepting value and unit ('C' or 'F')
- celsius property: Get/set temperature in Celsius
- fahrenheit property: Get/set temperature in Fahrenheit
- __str__(): Return formatted string

Validation:
- Temperature cannot be below absolute zero (-273.15°C or -459.67°F)
- Unit must be 'C' or 'F'

CONSTANTS:
ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_F = -459.67

EXAMPLES:

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

YOUR TASK:
1. Use UMPIRE to plan your approach
2. Implement the Temperature class with @property decorators
3. Add validation for absolute zero
4. Test with the provided test cases
"""

# Constants
ABSOLUTE_ZERO_C = -273.15
ABSOLUTE_ZERO_F = -459.67
UNITS = {'C', 'F'}

class Temperature():
    """Represents a temperatue that can be accessed in Celsius and Fahrenheit"""
    
    def __init__(self, value:float, unit:str) -> None:
        """Create a Temperature object.
        Args:
            value: Temperature value
            unit: 'C' for Celsius or 'F' for Fahrenheit
            
        Raises:
            ValueError: If unit is invalid or temperature is below absolute zero
        """
        if unit not in UNITS:
            raise ValueError('Unit must be C or F')

        if unit == 'C':
            self._celsius = value
        else:
            self._celsius = self._f_to_c_converter(value)

        self._absolute_zero_validator(self._celsius)

    def _f_to_c_converter(self, value:float) -> float:
        """Converts Fahrenheit to Celsius
        Args:
            Value is temp in Fahrenheit
        """
        return (value - 32) * 5/9

    def _absolute_zero_validator(self, celsius:float) -> None:
        """Checks if the given temp is below absolute zero
        Args:
            temp in celsius to validate
        """
        if celsius < ABSOLUTE_ZERO_C:
            raise ValueError('Value must be above absolute zero')

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value:float) -> None:
        """Sets _celsius to given value if validation is successful
        Args:
            Value is temp in Celsius
        """
        celsius_value = value
        self._absolute_zero_validator(celsius_value)
        self._celsius = celsius_value

    @property
    def fahrenheit(self) -> float:
        """Converts _celsius to Fahrenheit
        """
        return (self._celsius * 9/5) + 32

    @fahrenheit.setter
    def fahrenheit(self, value:float) -> None:
        """Converts Fahrenheit to Celsius and sets 
        _celsius to given value if validation is successful
        
        Args:
            Value is temp in Fahrenheit
        """
        celsius_value = self._f_to_c_converter(value)
        self._absolute_zero_validator(celsius_value)
        self._celsius = celsius_value

    def __str__(self):
        return f"{self._celsius}°C ({self.fahrenheit}°F)"

# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    print("=== Testing Temperature Creation ===")

    # Create from Celsius
    temp1 = Temperature(25, 'C')
    print(f"Temp 1: {temp1}")                    # Expected: 25.0°C (77.0°F)
    print(f"  Celsius: {temp1.celsius}")         # Expected: 25.0
    print(f"  Fahrenheit: {temp1.fahrenheit}")   # Expected: 77.0

    # # Create from Fahrenheit
    temp2 = Temperature(68, 'F')
    print(f"\nTemp 2: {temp2}")                  # Expected: 20.0°C (68.0°F)
    print(f"  Celsius: {temp2.celsius}")         # Expected: 20.0
    print(f"  Fahrenheit: {temp2.fahrenheit}")   # Expected: 68.0

    print("\n=== Testing Property Setters ===")

    # # Set via Celsius property
    temp1.celsius = 0
    print(f"After setting celsius to 0:")
    print(f"  Celsius: {temp1.celsius}")         # Expected: 0.0
    print(f"  Fahrenheit: {temp1.fahrenheit}")   # Expected: 32.0

    # # Set via Fahrenheit property
    temp1.fahrenheit = 212
    print(f"\nAfter setting fahrenheit to 212:")
    print(f"  Celsius: {temp1.celsius}")         # Expected: 100.0
    print(f"  Fahrenheit: {temp1.fahrenheit}")   # Expected: 212.0

    print("\n=== Testing Validation ===")

    # # Test absolute zero Celsius - Expected: ValueError raised
    try:
        temp3 = Temperature(-300, 'C')
        print("❌ FAIL: Should raise ValueError for temp below absolute zero")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test absolute zero Fahrenheit - Expected: ValueError raised
    try:
        temp4 = Temperature(-500, 'F')
        print("❌ FAIL: Should raise ValueError for temp below absolute zero")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test invalid unit - Expected: ValueError raised
    try:
        temp5 = Temperature(25, 'K')
        print("❌ FAIL: Should raise ValueError for invalid unit")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # # Test setting below absolute zero via property - Expected: ValueError raised
    try:
        temp1.celsius = -300
        print("❌ FAIL: Should raise ValueError when setting temp below absolute zero")
    except ValueError as e:
        print(f"✓ ValueError: {e}")

    # print("\n=== Edge Cases ===")

    # Test absolute zero exactly - Expected: Should work (at the boundary)
    temp_abs_c = Temperature(ABSOLUTE_ZERO_C, 'C')
    print(f"Absolute zero C: {temp_abs_c}")        # Expected: -273.15°C (-459.67°F)

    temp_abs_f = Temperature(ABSOLUTE_ZERO_F, 'F')
    print(f"Absolute zero F: {temp_abs_f}")        # Expected: -273.15°C (-459.67°F)

    # Test freezing/boiling points
    freezing = Temperature(0, 'C')
    print(f"\nFreezing point: {freezing}")         # Expected: 0.0°C (32.0°F)

    boiling = Temperature(100, 'C')
    print(f"Boiling point: {boiling}")             # Expected: 100.0°C (212.0°F)