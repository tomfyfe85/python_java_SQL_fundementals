"""
Both functions must use type hints
Validate that input is a number (int or float)
Validate that temperature is not below absolute zero
Absolute zero in Celsius: -273.15°C
Absolute zero in Fahrenheit: -459.67°
Raise appropriate exceptions for invalid inputs
Return float value  
"""
# Create two functions, one that converts C to F and visa versa
# Add appropriate validation


# inputs:
# #TypeError if input is not a number

# def celsius_to_fahrenheit(celsius)
# integer or double
# represents celsius

# Function (fahrenheit_to_celsius):
# Parameter name: fahrenheit
# Type: integer or double
# Description: represents celsius


# No constraints
# Will the figure be below ab zero - True - throw error

# outputs - a string containing result of temperature conversion

# use if
# if converting C to F, and the result is equal or above absolute zero
# in F, return value

# if not, throw error - this figure is below absolute zero
#ValueError - If temperature is below absolute zero



# edge cases
# handle absolute zero
# handle invalid data -  a string, None

# °C = (°F - 32) / 1.8
# F= (C*9 /5) + 32

# Absolute zero in Celsius: -273.15°C
# Absolute zero in Fahrenheit: -459.67°

# same plan for both:
# put argument into the equation
# first - type check - must be a double or an int
# results are interpolated in a descriptive string
# if result > ab zero - return "'result' fahrenheit "
# elif result == ab zero  - return "'result' fahrenheit  - absolute zero"
# else: Throw error - result is below absolute zero -459.67 farenheigt

#test 100c -> 212f
#test 0c -> 32f
#test 0f -> -17.78c
#test 100f -> 37.78c

## U - UNDERSTAND

# **Problem Restatement:**
# two functions that convert temperatures with validation

# **Inputs:**
# Function 1 (celsius_to_fahrenheit):
# - Parameter name: celsius
# - Type: int or float
# - Description: Temperature in Celsius to convert

# Function 2 (fahrenheit_to_celsius):
# - Parameter name: fahrenheit
# - Type: int or float
# - Description: Temperature in Fahrenheit to convert

# **Outputs:**
# - Function 1 returns: a float rounded up to two decimal places
# - Function 2 returns: a float rounded up to two decimal places

# **Constraints:**
# - Input must be a number (int or float)
# - Input cannot be below absolute zero
# - Must raise TypeError for non-numeric input
# - Must raise ValueError for below absolute zero

# **Questions/Clarifications:**
# all clear

# ---

# ## M - MATCH

# **Similar problems I've solved:**
# using  .ceil to return a float out 2 decimal places

# **Data structures needed:**
# [Just working with numbers - no lists or dicts needed]

# **Techniques needed:**
# - Type checking with isinstance()
# - Raising exceptions
# - Mathematical operations
# - if statement

# **Patterns that might apply:**
# - Input validation pattern: Check if input is valid before processing
#if x < 0:
#   raise Exception("Sorry, no numbers below zero")
# ---

# ## P - PLAN

# **Pseudocode for celsius_to_fahrenheit(celsius):**
# ```
# 1. Check if celsius is an instance of (int, float)
#    - If not, raise TypeError with message
# 2. Check if celsius < -273.15
#    - If yes, raise ValueError with message
# 3. Calculate fahrenheit = (celsius * 9/5) + 32
# 4. Return fahrenheit as float
# ```

# **Pseudocode for fahrenheit_to_celsius(fahrenheit):**
# ```
# 1. Check if fahrenheit is an instance of (int, float)
#    - If not, raise TypeError with message
# 2. Check if fahrenheit< -459.67°
#    - If yes, raise ValueError with message
# 3. Calculate C = (°F - 32) / 1.8
# 4. Return fahrenheit as float

# **Edge cases to handle:**
# - Input is a string (e.g., "hot") → TypeError
# - Input is None → TypeError
# - Input is a list (e.g., [100]) → TypeError
# - Input is below absolute zero in Celsius (-274°C) → ValueError
# - Input is below absolute zero in Fahrenheit (-460°F) → ValueError
# - Input is exactly absolute zero (-273.15°C or -459.67°F) → Should work!

# **Test cases with expected outputs:**
# ```
# # Valid conversions
# Test 1: celsius_to_fahrenheit(0) → Expected: 32.0
# Test 2: celsius_to_fahrenheit(100) → Expected: 212.0
# Test 3: celsius_to_fahrenheit(-40) → Expected: -40.0 (same in both!)
# Test 4: fahrenheit_to_celsius(32) → Expected: 0.0
# Test 5: fahrenheit_to_celsius(212) → Expected: 100.0

# # Absolute zero (should work)
# Test 6: celsius_to_fahrenheit(-273.15) → Expected: -459.67
# Test 7: fahrenheit_to_celsius(-459.67) → Expected: -273.15

# # Below absolute zero (should raise ValueError)
# Test 8: celsius_to_fahrenheit(-300) → Expected: ValueError
# Test 9: fahrenheit_to_celsius(-500) → Expected: ValueError

# # Invalid types (should raise TypeError)
# Test 10: celsius_to_fahrenheit("hot") → Expected: TypeError
# Test 11: celsius_to_fahrenheit(None) → Expected: TypeError
# Test 12: fahrenheit_to_celsius([100]) → Expected: TypeError

# Constants
ABSOLUTE_ZERO_CELSIUS = -273.15
ABSOLUTE_ZERO_FAHRENHEIT = -459.67


def celsius_to_fahrenheit(celsius: float | int ) -> float:
    """Convert Celsius to Fahrenheit.
    
    Args:
        celsius: Temperature in Celsius
        
    Returns:
        Temperature in Fahrenheit
        
    Raises:
        TypeError: If celsius is not a number
        ValueError: If celsius is below absolute zero
    """
 

# 2. Check if celsius < -273.15
#    - If yes, raise ValueError with message
# 3. Calculate fahrenheit = (celsius * 9/5) + 32
# 4. Return fahrenheit as float

    if not isinstance(celsius, (float, int))  :
        raise TypeError("input must be a  float")

    fahrenheit = (celsius * 9/5) + 32

    if fahrenheit > ABSOLUTE_ZERO_FAHRENHEIT:
        return float(fahrenheit)
    else:
        raise ValueError("Result is below absolute zero")




def fahrenheit_to_celsius(fahrenheit: float | int) -> float:
    """Convert Fahrenheit to Celsius.temo
    
    Args:
        fahrenheit: Temperature in Fahrenheit
        
    Returns:
        Temperature in Celsius
        
    Raises:
        TypeError: If fahrenheit is not a number
        ValueError: If fahrenheit is below absolute zero
    """
    # Your implementation here
    pass


# Manual testing
if __name__ == "__main__":
    # Test valid conversions
    print(celsius_to_fahrenheit(0))      # Should be 32.0
    print(celsius_to_fahrenheit(100))    # Should be 212.0
    print(celsius_to_fahrenheit(32))     # Should be 0.0

    # print(fahrenheit_to_celsius(12))     # Should be 0.0
    
    # Test edge cases
    # try:
    #     celsius_to_fahrenheit("hot")
    # except TypeError as e:
    #     print(f"Caught TypeError: {e}")
    
    # try:
    #     celsius_to_fahrenheit(-300)
    # except ValueError as e:
    #     print(f"Caught ValueError: {e}")