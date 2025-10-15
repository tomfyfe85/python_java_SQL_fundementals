# Python Fundamentals Practice - Quick Reference
# ================================================
# Core Python concepts for CrowdComms interview prep
# Focus: Dictionaries, Sets, Counter, deque, Comprehensions

from collections import Counter, deque

# ===========================================================================
# PART 1: DICTIONARY METHODS
# ===========================================================================

"""
DICTIONARIES - Key-Value Mappings
==================================

Use when: You need to look up values by a unique key

Common methods:
- .get(key, default) - Safe retrieval with fallback
- .keys() - All keys
- .values() - All values
- .items() - Key-value pairs for iteration
"""

# METHOD 1: .get(key, default) - Safe Access
# -------------------------------------------
print("=" * 70)
print("DICTIONARY METHOD 1: .get()")
print("=" * 70)

user_data = {'name': 'Alice', 'age': 25}

# ❌ BAD - Crashes if key doesn't exist
# country = user_data['country']  # KeyError!

# ✅ GOOD - Returns None if key doesn't exist
country = user_data.get('country')
print(f"Country (no default): {country}")  # None

# ✅ BEST - Returns custom default
country = user_data.get('country', 'Unknown')
print(f"Country (with default): {country}")  # Unknown

# CRITICAL PATTERN: Counting with .get()
vote_counts = {}
votes = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']

for vote in votes:
    vote_counts[vote] = vote_counts.get(vote, 0) + 1

print(f"Vote counts: {vote_counts}")
# Result: {'apple': 3, 'banana': 2, 'orange': 1}


# METHOD 2: .keys() - All Keys
# -----------------------------
print("\n" + "=" * 70)
print("DICTIONARY METHOD 2: .keys()")
print("=" * 70)

inventory = {'apples': 50, 'bananas': 30, 'oranges': 20}

# Get all keys
print(f"Products: {list(inventory.keys())}")

# Check if key exists
if 'apples' in inventory.keys():  # Can also just use: if 'apples' in inventory
    print("Apples in stock!")


# METHOD 3: .values() - All Values
# ---------------------------------
print("\n" + "=" * 70)
print("DICTIONARY METHOD 3: .values()")
print("=" * 70)

prices = {'apple': 1.50, 'banana': 0.80, 'orange': 1.20}

# Sum all values
total = sum(prices.values())
print(f"Total cost: ${total:.2f}")

# Max/min
print(f"Most expensive: ${max(prices.values()):.2f}")
print(f"Cheapest: ${min(prices.values()):.2f}")


# METHOD 4: .items() - Key-Value Pairs
# -------------------------------------
print("\n" + "=" * 70)
print("DICTIONARY METHOD 4: .items()")
print("=" * 70)

student_scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78}

# Iterate over both keys and values
print("Student scores:")
for name, score in student_scores.items():
    print(f"  {name}: {score}")

# Filter based on values
print("Students who passed (>= 80):")
for name, score in student_scores.items():
    if score >= 80:
        print(f"  {name}: {score}")


# ===========================================================================
# PART 2: DICTIONARY COMPREHENSIONS
# ===========================================================================

print("\n" + "=" * 70)
print("DICTIONARY COMPREHENSIONS")
print("=" * 70)

"""
DICTIONARY COMPREHENSION - Transform/Filter Data
=================================================

Syntax: {key: value for item in items}

Use when: Creating a new dict from existing data
"""

# Example 1: Transform list to dict
tickets = [
    {'ticket_id': 'T001', 'ticket_type': 'VIP'},
    {'ticket_id': 'T002', 'ticket_type': 'General'}
]

# Create ticket_id -> ticket_type mapping
ticket_lookup = {t['ticket_id']: t['ticket_type'] for t in tickets}
print(f"Ticket lookup: {ticket_lookup}")

# Example 2: Filter dictionary
gate_traffic = {'gate_A': 150, 'gate_B': 45, 'gate_C': 200, 'gate_D': 30}
busy_gates = {gate: count for gate, count in gate_traffic.items() if count > 100}
print(f"Busy gates (>100 people): {busy_gates}")

# Example 3: Swap keys and values
ticket_to_user = {'T001': 'U123', 'T002': 'U456', 'T003': 'U789'}
user_to_ticket = {user: ticket for ticket, user in ticket_to_user.items()}
print(f"User to ticket mapping: {user_to_ticket}")


# ===========================================================================
# PART 3: SETS
# ===========================================================================

print("\n" + "=" * 70)
print("SET OPERATIONS")
print("=" * 70)

"""
SETS - Unique Collections with Fast Membership Testing
=======================================================

Use when:
- Need to track unique items (automatic deduplication)
- Need fast membership testing (O(1) instead of O(n))
- Need to compare groups (union, intersection, difference)

Critical for: Tracking who's currently inside a venue
"""

# Creating and adding to sets
attendees = set()
attendees.add('U123')
attendees.add('U456')
attendees.add('U123')  # Duplicate - won't be added again!

print(f"Attendees: {attendees}")  # Only 2 items
print(f"Count: {len(attendees)}")

# Fast membership check (O(1) time)
if 'U123' in attendees:
    print("U123 is in the set!")


# CRITICAL METHODS: add() and discard()
# --------------------------------------
print("\n" + "=" * 70)
print("SET METHODS: add() and discard()")
print("=" * 70)

people_inside = set()

# add() - Add item to set
people_inside.add('U001')
people_inside.add('U002')
print(f"After entries: {people_inside}")

# discard() - Remove item (safe, no error if not present)
people_inside.discard('U001')
print(f"After U001 exits: {people_inside}")

people_inside.discard('U999')  # Not in set - no error!
print(f"After trying to remove U999: {people_inside}")

# ❌ NEVER USE remove() - crashes if item not in set!
# people_inside.remove('U999')  # KeyError!

# ✅ ALWAYS USE discard() - safe for entry/exit tracking


# SET OPERATIONS - Combining/Comparing Sets
# ------------------------------------------
print("\n" + "=" * 70)
print("SET OPERATIONS: Union, Intersection, Difference")
print("=" * 70)

monday_visitors = {'U001', 'U002', 'U003', 'U004'}
tuesday_visitors = {'U003', 'U004', 'U005', 'U006'}

# Union (|) - All items from both sets
all_visitors = monday_visitors | tuesday_visitors
print(f"All visitors (union): {all_visitors}")

# Intersection (&) - Items in BOTH sets
both_days = monday_visitors & tuesday_visitors
print(f"Visited both days (intersection): {both_days}")

# Difference (-) - Items in first set but NOT second
only_monday = monday_visitors - tuesday_visitors
print(f"Only Monday (difference): {only_monday}")

# Symmetric difference (^) - Items in either set but NOT both
one_day_only = monday_visitors ^ tuesday_visitors
print(f"One day only (symmetric diff): {one_day_only}")


# ===========================================================================
# PART 4: COUNTER - Counting Occurrences
# ===========================================================================

print("\n" + "=" * 70)
print("COUNTER - Specialized Counting Tool")
print("=" * 70)

"""
COUNTER - Count Occurrences Efficiently
========================================

Use when:
- Need to count how many times items appear
- Need most common items
- Need frequency analysis

DO NOT use when:
- Need to increment/decrement by 1 (use defaultdict(int) for entry/exit tracking)
"""

from collections import Counter

# Example 1: Count items in a list
scans = ['gate_A', 'gate_B', 'gate_A', 'gate_C', 'gate_A', 'gate_B']
gate_counts = Counter(scans)
print(f"Gate counts: {gate_counts}")

# Example 2: Most common items
print(f"Most common gate: {gate_counts.most_common(1)}")
print(f"Top 2 gates: {gate_counts.most_common(2)}")

# Example 3: Count ticket types
tickets = [
    {'ticket_type': 'VIP'},
    {'ticket_type': 'General'},
    {'ticket_type': 'VIP'},
    {'ticket_type': 'General'},
    {'ticket_type': 'General'}
]

ticket_type_counts = Counter(t['ticket_type'] for t in tickets)
print(f"Ticket type counts: {ticket_type_counts}")


# ===========================================================================
# PART 5: DEQUE - Double-Ended Queue
# ===========================================================================

print("\n" + "=" * 70)
print("DEQUE - Efficient Queues and Sliding Windows")
print("=" * 70)

"""
DEQUE - Double-Ended Queue
===========================

Use when:
- Need FIFO queue (process items in order)
- Need sliding window (last N items)
- Need efficient add/remove from both ends (O(1))

Critical for: Processing recent events, maintaining last N scans
"""

from collections import deque

# Example 1: FIFO queue
scan_queue = deque()
scan_queue.append('T001')
scan_queue.append('T002')
scan_queue.append('T003')

# Process in order
first = scan_queue.popleft()
print(f"Processing: {first}")  # T001

# Example 2: Sliding window (last N items)
recent_scans = deque(maxlen=3)  # Automatically keeps only last 3
recent_scans.append('T001')
recent_scans.append('T002')
recent_scans.append('T003')
recent_scans.append('T004')  # T001 is automatically removed!

print(f"Recent scans (last 3): {list(recent_scans)}")  # ['T002', 'T003', 'T004']

# Example 3: Recent activity tracker
recent_activity = deque(maxlen=5)
events = ['entry', 'entry', 'exit', 'entry', 'entry', 'exit', 'entry']

for event in events:
    recent_activity.append(event)

print(f"Last 5 events: {list(recent_activity)}")


# ===========================================================================
# PART 6: REAL-WORLD PATTERN - Entry/Exit Tracking
# ===========================================================================

print("\n" + "=" * 70)
print("REAL-WORLD PATTERN: Complete Entry/Exit Tracking")
print("=" * 70)

def track_occupancy(events):
    """
    Complete occupancy tracker combining all concepts.

    Uses:
    - Set for current occupancy
    - Dict for counting by gate
    - Counter for total scan patterns
    - deque for recent activity
    """
    currently_inside = set()
    entries_by_gate = {}
    total_entries = 0
    total_exits = 0
    recent_events = deque(maxlen=5)

    for event in events:
        user_id = event['user_id']
        action = event['action']
        gate = event['gate']

        if action == 'entry':
            currently_inside.add(user_id)
            entries_by_gate[gate] = entries_by_gate.get(gate, 0) + 1
            total_entries += 1
        else:
            currently_inside.discard(user_id)
            total_exits += 1

        recent_events.append(f"{user_id} {action}")

    return {
        'current_occupancy': len(currently_inside),
        'currently_inside': currently_inside,
        'total_entries': total_entries,
        'total_exits': total_exits,
        'entries_by_gate': entries_by_gate,
        'recent_activity': list(recent_events)
    }

# Test the function
test_events = [
    {'user_id': 'U001', 'gate': 'A', 'action': 'entry'},
    {'user_id': 'U002', 'gate': 'B', 'action': 'entry'},
    {'user_id': 'U003', 'gate': 'A', 'action': 'entry'},
    {'user_id': 'U001', 'gate': 'A', 'action': 'exit'},
    {'user_id': 'U004', 'gate': 'B', 'action': 'entry'},
    {'user_id': 'U002', 'gate': 'B', 'action': 'exit'},
]

result = track_occupancy(test_events)
print("Occupancy tracking result:")
for key, value in result.items():
    print(f"  {key}: {value}")


# ===========================================================================
# QUICK REFERENCE SUMMARY
# ===========================================================================

print("\n" + "=" * 70)
print("QUICK REFERENCE SUMMARY")
print("=" * 70)

summary = """
DICTIONARIES:
  .get(key, default)     → Safe retrieval with fallback
  .keys()                → All keys
  .values()              → All values
  .items()               → Key-value pairs for iteration
  {k: v for ...}         → Dictionary comprehension

SETS:
  .add(item)             → Add item
  .discard(item)         → Remove item (safe, no error)
  set1 | set2            → Union (all from both)
  set1 & set2            → Intersection (in both)
  set1 - set2            → Difference (in first, not second)

COUNTER:
  Counter(items)         → Count occurrences
  .most_common(n)        → Get top n items

DEQUE:
  deque(maxlen=n)        → Sliding window of last n items
  .append(item)          → Add to right
  .popleft()             → Remove from left (FIFO)

WHEN TO USE WHAT:
  - Lookups by key → dict
  - Unique tracking → set
  - Counting occurrences → Counter
  - Recent N items → deque(maxlen=N)
  - Entry/exit tracking → set (for current) + dict (for stats)
"""

print(summary)

print("\n" + "=" * 70)
print("DONE! You now have a comprehensive Python fundamentals reference.")
print("=" * 70)
