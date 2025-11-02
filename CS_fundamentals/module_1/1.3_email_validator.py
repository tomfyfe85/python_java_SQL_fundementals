"""
Exercise 1.3: Email Validator

Create a function that validates email addresses according to simple rules.

REQUIREMENTS:
Create a function: is_valid_email(email: str) -> bool

Validation Rules:
1. Must contain exactly one '@' symbol
2. Must have at least one character before '@'
3. Must have at least one character after '@'
4. The part after '@' must contain at least one '.'
5. Must have at least one character after the last '.'

Examples:
- is_valid_email("user@example.com")       → True
- is_valid_email("alice@company.co.uk")    → True
- is_valid_email("invalid")                → False (no @)
- is_valid_email("@example.com")           → False (nothing before @)
- is_valid_email("user@")                  → False (nothing after @)
- is_valid_email("user@example")           → False (no . after @)
- is_valid_email("user@example.")          → False (nothing after .)
- is_valid_email("user@@example.com")      → False (multiple @)

YOUR TASK:
1. Use the UMPIRE method to solve this problem
2. Write your understanding of the problem first
3. Plan your approach
4. Implement the function with type hints and docstring
5. Test thoroughly with all the examples above
"""

# ==========================================
# YOUR CODE GOES BELOW
# ==========================================

# TODO: Implement is_valid_email() function here


# ==========================================
# TEST CASES
# ==========================================

if __name__ == "__main__":
    # Test valid emails
    print("Testing valid emails:")
    print(is_valid_email("user@example.com"))       # True
    print(is_valid_email("alice@company.co.uk"))    # True
    print(is_valid_email("test.user@domain.com"))   # True

    print("\nTesting invalid emails:")
    print(is_valid_email("invalid"))                # False (no @)
    print(is_valid_email("@example.com"))           # False (nothing before @)
    print(is_valid_email("user@"))                  # False (nothing after @)
    print(is_valid_email("user@example"))           # False (no . after @)
    print(is_valid_email("user@example."))          # False (nothing after .)
    print(is_valid_email("user@@example.com"))      # False (multiple @)
