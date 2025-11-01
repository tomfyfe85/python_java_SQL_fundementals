"""
Both functions must use type hints
Validate that input is a number (int or float)
Validate that temperature is not below absolute zero
Absolute zero in Celsius: -273.15°C
Absolute zero in Fahrenheit: -459.67°
Raise appropriate exceptions for invalid inputs
Return float value  
"""
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
    if not isinstance(fahrenheit, (float, int))  :
        raise TypeError("input must be a  float")

    celsius = (celsius * 9/5) + 32

    if fahrenheit > ABSOLUTE_ZERO_FAHRENHEIT:
        return float(fahrenheit)
    else:
        raise ValueError("Result is below absolute zero"


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