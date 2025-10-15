# Python Search Guide for Tech Interview
Quick reference for Googling Python concepts during your test

## 🔍 How to Use This Guide

**In the interview when you need help:**
1. Find the concept you need below
2. Use the "Google this" search term
3. Look for official Python docs or specific resource links provided

**Pro tips:**
- Add "python 3" to searches for current syntax
- Add "example" to get code snippets
- Official docs (docs.python.org) are always safe and accurate

---

## 📊 Data Structures

### Sets
**What:** Unordered collection, no duplicates, O(1) membership testing

**Google this:**
- `python set add remove`
- `python set vs list performance`
- `python check if in set`

**Direct resources:**
- Official docs: https://docs.python.org/3/tutorial/datastructures.html#sets
- Set operations: https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

**Common operations you'll need:**
```python
my_set = set()          # Create empty set
my_set.add('item')      # Add item
my_set.discard('item')  # Remove (no error if missing)
my_set.remove('item')   # Remove (raises error if missing)
if 'item' in my_set:    # Check membership O(1)
len(my_set)             # Get size
```

**When to use in occupancy problems:**
- Tracking who's currently inside (automatic duplicate handling)
- Detecting duplicates
- Fast lookups

---

### Counter (from collections)
**What:** Dict subclass for counting hashable objects

**Google this:**
- `python Counter examples`
- `python Counter most_common`
- `python count occurrences Counter`

**Direct resources:**
- Official docs: https://docs.python.org/3/library/collections.html#collections.Counter
- Real Python tutorial: https://realpython.com/python-counter/

**Common operations you'll need:**
```python
from collections import Counter

# Create and count
counter = Counter(['a', 'b', 'a', 'c'])  # Counter({'a': 2, 'b': 1, 'c': 1})
counter['a']          # Get count (returns 0 if not found, not error)
counter['a'] += 1     # Increment
counter.most_common(3)  # Get top 3 [(key, count), ...]
counter.update(['a'])   # Add more items

# From dict
counter = Counter({'VIP': 5, 'General': 10})
```

**When to use in occupancy problems:**
- Counting scans per gate
- Counting by ticket type
- Finding most frequent entries

---

### defaultdict (from collections)
**What:** Dict that provides default value for missing keys

**Google this:**
- `python defaultdict int`
- `python defaultdict list`
- `python defaultdict vs dict`

**Direct resources:**
- Official docs: https://docs.python.org/3/library/collections.html#collections.defaultdict
- Real Python: https://realpython.com/python-defaultdict/

**Common operations you'll need:**
```python
from collections import defaultdict

# Auto-initialize to 0
counts = defaultdict(int)
counts['gate_A'] += 1  # No KeyError! Starts at 0

# Auto-initialize to empty list
entries_by_gate = defaultdict(list)
entries_by_gate['A'].append('T001')  # No KeyError!

# Auto-initialize to set
occupancy_by_gate = defaultdict(set)
occupancy_by_gate['A'].add('T001')
```

**When to use in occupancy problems:**
- Counting without checking if key exists first
- Grouping data (defaultdict(list))
- Tracking occupancy by category (defaultdict(set))

**Regular dict vs defaultdict:**
```python
# Regular dict - manual checking
regular = {}
if 'gate_A' not in regular:
    regular['gate_A'] = 0
regular['gate_A'] += 1

# defaultdict - automatic!
auto = defaultdict(int)
auto['gate_A'] += 1  # Just works!
```

---

### deque (from collections)
**What:** Double-ended queue, O(1) append/pop from both ends

**Google this:**
- `python deque append popleft`
- `python deque vs list performance`
- `python queue deque`

**Direct resources:**
- Official docs: https://docs.python.org/3/library/collections.html#collections.deque
- GeeksforGeeks: https://www.geeksforgeeks.org/deque-in-python/

**Common operations you'll need:**
```python
from collections import deque

queue = deque()
queue.append('item')        # Add to right (like list)
queue.appendleft('item')    # Add to left O(1)
queue.pop()                 # Remove from right
queue.popleft()             # Remove from left O(1)
len(queue)                  # Get size
if queue:                   # Check if not empty

# Initialize with items
queue = deque(['a', 'b', 'c'])

# Max length (auto-removes oldest)
recent = deque(maxlen=100)  # Only keeps last 100 items
```

**When to use in occupancy problems:**
- FIFO queue (first in, first out) for processing scans in order
- Sliding window (last N events)
- Recent activity tracking
- **NOT for occupancy tracking** - use set instead!

**List vs deque:**
- List: Fast at end (append/pop), slow at beginning
- Deque: Fast at BOTH ends
- Use deque when you need `popleft()` or `appendleft()`

---

### Dictionary Comprehension
**What:** Create dict in one line

**Google this:**
- `python dictionary comprehension`
- `python dict comprehension from list`
- `python create dict from two lists`

**Direct resources:**
- Official docs: https://docs.python.org/3/tutorial/datastructures.html#dictionaries
- Real Python: https://realpython.com/iterate-through-dictionary-python/#using-comprehensions

**Common patterns you'll need:**
```python
# From list of dicts
tickets = [
    {'ticket_id': 'T001', 'ticket_type': 'VIP'},
    {'ticket_id': 'T002', 'ticket_type': 'General'}
]
lookup = {t['ticket_id']: t['ticket_type'] for t in tickets}
# Result: {'T001': 'VIP', 'T002': 'General'}

# With condition
vip_only = {t['ticket_id']: t['ticket_type']
            for t in tickets
            if t['ticket_type'] == 'VIP'}

# From two lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
result = {k: v for k, v in zip(keys, values)}
```

**When to use in occupancy problems:**
- Create ticket_id → ticket_type lookup (for fast O(1) access)
- Transform data structures
- Filter and map in one step

---

## ⏰ Date and Time

### datetime module
**What:** Working with dates, times, and timestamps

**Google this:**
- `python datetime fromisoformat`
- `python timedelta examples`
- `python datetime subtract`
- `python parse iso timestamp`

**Direct resources:**
- Official docs: https://docs.python.org/3/library/datetime.html
- strftime.org: https://strftime.org/ (format codes)
- Real Python: https://realpython.com/python-datetime/

**Common operations you'll need:**
```python
from datetime import datetime, timedelta

# Parse ISO format string
timestamp = datetime.fromisoformat('2025-09-30T10:00:00')

# Compare times
time1 = datetime.fromisoformat('2025-09-30T10:00:00')
time2 = datetime.fromisoformat('2025-09-30T11:00:00')
if time1 < time2:  # Can compare directly
    print("time1 is earlier")

# Time difference
difference = time2 - time1  # Returns timedelta
print(difference)  # 1:00:00

# Check if within X minutes
if (time2 - time1) <= timedelta(minutes=5):
    print("Within 5 minutes")

# Get current time
now = datetime.now()

# Format to string
timestamp.strftime('%Y-%m-%d %H:%M:%S')  # '2025-09-30 10:00:00'
```

**When to use in occupancy problems:**
- Parse timestamp strings from scans
- Compare scan times
- Detect rapid re-entry (< 5 minutes)
- Filter by time ranges

---

### timedelta
**What:** Represents duration/difference between times

**Google this:**
- `python timedelta minutes hours`
- `python check time difference`

**Direct resources:**
- Official docs: https://docs.python.org/3/library/datetime.html#timedelta-objects

**Common operations you'll need:**
```python
from datetime import timedelta

# Create durations
five_minutes = timedelta(minutes=5)
one_hour = timedelta(hours=1)
two_days = timedelta(days=2)

# Use in comparisons
time_diff = exit_time - entry_time
if time_diff <= timedelta(minutes=5):
    print("Re-entered within 5 minutes")

# Get total seconds
time_diff.total_seconds()  # 300.0 for 5 minutes
```

---

## 🔤 String Operations

### String comparison
**What:** Comparing strings in Python

**Google this:**
- `python string comparison == vs is`
- `python compare strings`

**Direct resources:**
- Official docs: https://docs.python.org/3/reference/expressions.html#comparisons

**Important for interview:**
```python
# CORRECT: Use == for value comparison
if scan_type == 'entry':  # ✅ Compares values

# WRONG: Using 'is' for strings
if scan_type is 'entry':  # ❌ Compares object identity (may work by accident!)

# 'is' is for identity, not equality
if x is None:  # ✅ Correct use of 'is'
```

---

## 🔄 Control Flow

### if/elif/else
**What:** Conditional branching

**Google this:**
- `python if elif else`
- `python multiple conditions if`
- `python nested if statements`

**Direct resources:**
- Official docs: https://docs.python.org/3/tutorial/controlflow.html#if-statements

**Common patterns you'll need:**
```python
# Basic
if condition:
    # code
elif other_condition:
    # code
else:
    # code

# Only ONE block executes, then exits
if scan_type == 'entry':
    handle_entry()  # If this runs...
elif scan_type == 'exit':
    handle_exit()   # ...this NEVER runs

# Multiple independent checks
if scan_type == 'entry':
    handle_entry()

if len(occupancy) > 5:  # Separate check, always runs
    check_capacity()
```

**When to use in occupancy problems:**
- Branch logic for entry vs exit
- Handle duplicates vs valid entries
- Capacity checks

---

### continue statement
**What:** Skip rest of loop iteration, go to next one

**Google this:**
- `python continue statement`
- `python skip loop iteration`

**Direct resources:**
- Official docs: https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops

**Common usage:**
```python
for scan in scans:
    if scan['ticket_id'] in already_inside:
        continue  # Skip to next scan, don't run code below

    # Only runs if continue didn't execute
    process_scan(scan)

# vs break
for scan in scans:
    if scan['time'] > target_time:
        break  # Exit loop entirely
```

**When to use in occupancy problems:**
- Skip duplicate entries
- Ignore invalid scans
- Stop processing after target time (use `break` instead)

---

## 📝 Function Parameters

### Default parameters
**What:** Function arguments with default values

**Google this:**
- `python default function parameters`
- `python optional arguments`

**Direct resources:**
- Official docs: https://docs.python.org/3/tutorial/controlflow.html#default-argument-values

**Common patterns:**
```python
def manage_capacity(stream, max_capacity=6, vip_gate='A'):
    # max_capacity defaults to 6 if not provided
    # vip_gate defaults to 'A' if not provided
    pass

# Call without defaults
manage_capacity(my_stream)  # Uses 6 and 'A'

# Call with custom values
manage_capacity(my_stream, max_capacity=10)
manage_capacity(my_stream, max_capacity=10, vip_gate='B')
```

---

## 🎯 Common Patterns

### Iterating with for loops
**Google this:**
- `python for loop dictionary`
- `python iterate list of dicts`
- `python for loop multiple variables`

**Direct resources:**
- Official tutorial: https://docs.python.org/3/tutorial/controlflow.html#for-statements

```python
# List
for item in my_list:
    print(item)

# Dict
for key, value in my_dict.items():
    print(key, value)

# List of dicts
for event in events:
    ticket_id = event['ticket_id']
    scan_type = event['scan_type']

# Enumerate (index + value)
for index, item in enumerate(my_list):
    print(f"Item {index}: {item}")
```

---

### Type hints
**Google this:**
- `python type hints`
- `python Dict List Set types`
- `python typing module`

**Direct resources:**
- Official docs: https://docs.python.org/3/library/typing.html
- Real Python: https://realpython.com/python-type-checking/

```python
from typing import Dict, List, Set, Optional

def process_scans(stream) -> Dict:
    # Return type is Dict
    pass

def get_occupancy(stream, max_capacity: int = 6) -> int:
    # max_capacity must be int, returns int
    pass

# Common types
ticket_lookup: Dict[str, str]  # Dict with string keys and values
occupancy: Set[str]            # Set of strings
rejected: List[str]            # List of strings
count: Optional[int]           # int or None
```

---

## 🗄️ JSON

### json.loads() - Parse JSON string
**Google this:**
- `python parse json string`
- `python json.loads example`
- `python json to dict`

**Direct resources:**
- Official docs: https://docs.python.org/3/library/json.html
- Real Python: https://realpython.com/python-json/

```python
import json

# Parse JSON string to Python dict
json_string = '{"ticket_id": "T001", "scan_type": "entry"}'
scan_dict = json.loads(json_string)
print(scan_dict['ticket_id'])  # 'T001'

# Handle errors
try:
    data = json.loads(json_string)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

**When to use in occupancy problems:**
- Parse JSON scan events from API/stream
- FastAPI receives JSON automatically, but raw Python needs json.loads()

---

## 📚 Quick Reference Sites

### Official Python Documentation
**URL:** https://docs.python.org/3/
**Best for:** Accurate, complete reference
**Tip:** Search "python [concept] docs" to go straight there

### Real Python
**URL:** https://realpython.com/
**Best for:** Tutorials with examples
**Tip:** Great for understanding WHY and WHEN to use something

### Stack Overflow
**URL:** https://stackoverflow.com/
**Best for:** Specific error messages and edge cases
**Tip:** Look for answers with green checkmarks and high votes
**Search format:** `[python] [your question]`

### Python Module Index
**URL:** https://docs.python.org/3/py-modindex.html
**Best for:** Finding what module has what function
**Tip:** Ctrl+F to search for "collections", "datetime", etc.

---

## 🎯 Interview Search Strategy

### When you're stuck:

**1. Know what you need but forgot syntax?**
```
Google: "python [operation] [data structure]"
Example: "python add to set"
Example: "python count items Counter"
```

**2. Error message?**
```
Google the EXACT error message in quotes
Example: "TypeError: 'generator' object is not subscriptable"
Add "python" if needed
```

**3. Need to know which data structure?**
```
Google: "python best data structure for [task]"
Example: "python best data structure for checking membership"
Example: "python fast lookup by key"
```

**4. Know the concept in English?**
```
Google: "python how to [describe what you want]"
Example: "python how to get last item per group"
Example: "python how to count duplicates"
```

**5. Time pressure - need quick example?**
```
Add "example" to any search
Example: "python datetime timedelta example"
Example: "python defaultdict example"
```

---

## ⚡ Speed Tips for the Interview

1. **Start with official docs** - Most reliable, usually has examples
2. **Ctrl+F is your friend** - Don't read entire pages, search for keywords
3. **Look at code examples first** - Skip prose, find the code block
4. **Copy-paste is OK** - Modify example code to your needs
5. **Test in REPL first** - Quick `python3` terminal to test syntax
6. **Bookmark these**:
   - https://docs.python.org/3/library/collections.html (Counter, defaultdict, deque)
   - https://docs.python.org/3/library/datetime.html (datetime, timedelta)
   - https://docs.python.org/3/tutorial/datastructures.html (sets, dicts, lists)

---

## 🔥 Most Likely Searches for Your Interview

Based on your occupancy problems, you'll probably Google:

1. **"python set add remove discard"** - For tracking who's inside
2. **"python datetime fromisoformat"** - For parsing timestamps
3. **"python timedelta minutes"** - For time comparisons
4. **"python dictionary comprehension"** - For ticket lookups
5. **"python defaultdict int"** - For counting by category
6. **"python Counter most_common"** - For analytics
7. **"python json loads"** - For parsing JSON events
8. **"python == vs is"** - For string comparison
9. **"python continue vs break"** - For loop control
10. **"python type hints Dict"** - For function signatures

**Print this list out or have it open in a tab!**

---

## 💡 Practice Tips

Before the interview:
1. **Google these terms** now and bookmark the official doc pages
2. **Try the examples** in a Python REPL to get familiar
3. **Note which sites you find helpful** - everyone has preferences
4. **Practice searching with a timer** - get fast at finding answers

During the interview:
1. **Don't memorize** - they EXPECT you to look things up
2. **Talk while you search** - "Let me check the syntax for timedelta..."
3. **Skim fast** - find the code example, adapt it
4. **Test immediately** - don't assume it works, run it

Good luck! 🚀
