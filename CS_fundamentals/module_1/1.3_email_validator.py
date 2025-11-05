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

def is_valid_email(email: str) -> bool:
    """Validate emails to these rules:
        1. Must contain exactly one '@' symbol
        2. Must have at least one character before '@'
        3. Must have at least one character after '@'
        4. The part after '@' must contain at least one '.'
        5. Must have at least one character after the last '.'

    Args:
        email: An email in string format.

    Returns:
        boolean - if the email doesn't fit the rules, return False
    """


    if not isinstance(email, str):
        raise TypeError("Email should be a string")

    if email.count('@') != 1:
        return False
    
    at_index = email.index("@")
    email_from_at_sign = email[at_index:]

    if email[0] == '@' or email[-1] == '@':
        return False
    elif email[-1] == '.':
        return False
    elif '.' not in email_from_at_sign:
        return False
    else:
        return True

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
