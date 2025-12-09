# Handover Document - Python CS Fundamentals Course

## Current Status
User is working through a Python CS Fundamentals course, currently in **Module 2: Object-Oriented Programming**.

## Completed Work

### Exercise 2.3: Temperature Class ✓
**File:** `CS_fundamentals/module_2/2.3_temperature_class.py`

- Fully implemented Temperature class with @property decorators
- Stores temperature internally in Celsius (`_celsius`)
- Provides `celsius` and `fahrenheit` properties with getters/setters
- Validates against absolute zero (-273.15°C / -459.67°F)
- All test cases passing

### Challenge 2.1: Shopping Cart System ✓
**File:** `CS_fundamentals/module_2/2.4_shopping_cart.py`

**Product Class** (lines 11-33):
- Constructor with validation (name, price, category)
- Raises ValueError for empty name/category or negative price
- `__str__()` method implemented

**ShoppingCart Class** (lines 36-106):
- `__init__()`: Initializes empty products dict, subtotal=0, calculated_tax=0
- `add_product(product, quantity)`: Uses Product object as dict key, handles quantity increments
- `remove_product(product_name)`: Removes by product name string
- `get_subtotal()`: Resets self.subtotal=0 then calculates (prevents accumulation bug)
- `get_tax()`: Calls get_subtotal() internally, returns 8% tax
- `get_total()`: Returns tax + subtotal
- `__str__()`: Formatted cart display with line items, subtotal, tax, total

**All test cases passing** - Exercise marked complete by user.

## Key Implementation Details

### Important Bug Fixes Made:
1. **get_subtotal()** - Added `self.subtotal = 0` at start to prevent accumulation on multiple calls
2. **get_tax()** - Fixed formula from `DEFAULT_TAX_RATE/subtotal` to `DEFAULT_TAX_RATE * get_subtotal()`
3. **get_tax()** - Now calls `get_subtotal()` internally for independence
4. **Dictionary structure** - Uses Product objects as keys (not product.name), with quantity as value

## User Preferences & Communication Style

**CRITICAL - Read This:**
- User explicitly stated: **"dont tell me what to do"**
- Prefers guidance and questions over direct solutions
- Wants to learn concepts, not just get answers
- Aware of file changes (don't mention system reminders)
- Keep responses concise
- No emojis unless explicitly requested

## Current Task
User just requested help writing a LinkedIn post about the Shopping Cart challenge (keep it under 10 lines). Post was provided.

User is now switching to Opus model and may continue with next exercise in Module 2.

## Next Steps (Likely)
Check course syllabus for next Module 2 exercise:
- Files: `CS_fundamentals/syllabus/complete_course_backup.md` or `complete_python_cs_curriculum.md`
- Continue with next OOP exercise in Module 2

## Repository Structure
```
/Users/tomfyfe/codes/python_cs/
├── CS_fundamentals/
│   ├── module_2/
│   │   ├── 2.3_temperature_class.py (COMPLETE)
│   │   └── 2.4_shopping_cart.py (COMPLETE)
│   └── syllabus/
│       ├── complete_course_backup.md
│       └── complete_python_cs_curriculum.md
```

## Git Status
- Current branch: `main`
- Status: Clean (as of last check)
- Recent commits show progression through exercises

## Constants & Conventions Used
- `DEFAULT_TAX_RATE = 0.08` (8% tax)
- Type hints used throughout (`:str`, `:float`, `:int`, `-> None`)
- Docstrings follow Google style
- Private attributes prefixed with `_` (e.g., `_celsius`)
- Validation via ValueError exceptions

## Test Pattern
Both completed exercises follow same test structure:
- Test basic functionality
- Test validation (ValueError cases)
- Test edge cases
- All tests in `if __name__ == "__main__":` block
