"""
Exercise 1.2: Refactoring Practice

Your task: Refactor the code below to follow clean code principles.

Requirements:
1. Meaningful function and variable names
2. Type hints on all functions
3. Docstrings for all functions
4. Replace magic numbers with named constants
5. Clear, readable logic

Run the original code first to understand what it does, then refactor!
"""

# ==========================================
# BAD CODE - DO NOT MODIFY THIS SECTION
# ==========================================

def f(x, y, z):
    a = x + y
    b = a * z
    if b > 100:
        return b - 10
    else:
        return b

def proc(data):
    r = []
    for d in data:
        if d > 0:
            r.append(d * 2)
    return r

x = 50
y = 30
result = x * 0.15
print(result)


# ==========================================
# YOUR REFACTORED CODE GOES BELOW
# ==========================================

# TODO: Refactor the code above here

