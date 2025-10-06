"""
PYTHON DICTIONARY AND SET PRACTICE EXERCISES
=============================================

This file contains explanations and exercises for mastering:
- Dictionary methods: .get(), .keys(), .values(), .items()
- Set operations: add(), discard(), remove(), union, intersection, etc.

Work through each section in order!
"""

# ==============================================================================
# PART 1: DICTIONARY METHODS
# ==============================================================================

print("=" * 70)
print("PART 1: DICTIONARY METHODS")
print("=" * 70)

# ------------------------------------------------------------------------------
# METHOD 1: .get(key, default)
# ------------------------------------------------------------------------------
"""
EXPLANATION:
------------
.get() safely retrieves a value from a dictionary. If the key doesn't exist,
it returns None (or a default value you specify) instead of crashing.

SYNTAX:
    dict.get(key)              # Returns None if key not found
    dict.get(key, default)     # Returns default if key not found

WHY USE IT:
    - Prevents KeyError crashes
    - Essential for safe data access
    - Perfect for counting patterns

EXAMPLE:
"""
# print("\n--- .get() METHOD ---")

# user_data = {'name': 'Alice', 'age': 25, 'city': 'London'}

# # Using bracket notation - RISKY!
# try:
#     country = user_data['country']  # This will crash!
# except KeyError:
#     print("❌ KeyError: 'country' key doesn't exist")

# # Using .get() - SAFE!
# country = user_data.get('country')
# print(f"✓ Country (using .get()): {country}")  # Returns None

# country = user_data.get('country', 'Unknown')
# print(f"✓ Country (with default): {country}")  # Returns 'Unknown'

# # The counting pattern - VERY IMPORTANT!
# vote_counts = {}
# votes = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']

# for vote in votes:
#     vote_counts[vote] = vote_counts.get(vote, 0) + 1

# print(f"✓ Vote counts: {vote_counts}")

print("\n" + "=" * 70)
print("EXERCISE 1: .get() Practice")
print("=" * 70)

# EXERCISE 1.1: Safe Access
print("\nExercise 1.1: Safe Dictionary Access")
event = {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '10:00'}

# TODO: Get the 'user_id' field safely (it doesn't exist!)
# Use .get() and provide 'GUEST' as the default value
user_id = event.get('user_id', 'GUEST')
print(f"User ID: {user_id}")  # Should print: User ID: GUEST


# EXERCISE 1.2: Counting Pattern
print("\nExercise 1.2: Count Item Occurrences")
scans = ['gate_A', 'gate_B', 'gate_A', 'gate_C', 'gate_A', 'gate_B', 'gate_C', 'gate_C']

gate_counts = {}

for scan in scans:
    gate_counts[scan] = gate_counts.get(scan, 0) + 1


print(f"Gate counts: {gate_counts}")
# Expected: {'gate_A': 3, 'gate_B': 2, 'gate_C': 3}


# EXERCISE 1.3: Default Values
# print("\nExercise 1.3: Configuration with Defaults")
config = {'timeout': 30, 'retries': 3}

# TODO: Get these config values, using defaults if missing:
# - 'timeout' (should get 30)
# - 'max_connections' (doesn't exist, use default 100)
# - 'debug_mode' (doesn't exist, use default False)
TIMEOUT = config.get('timeout', 0)
MAX_CONNECTIONS = config.get('max_connections', 100)
DEBUG_MODE = config.get('debug_mode', False)


print(f"Timeout: {TIMEOUT}, Max Connections: {MAX_CONNECTIONS}, Debug: {DEBUG_MODE}")
# Expected: Timeout: 30, Max Connections: 100, Debug: False


# ------------------------------------------------------------------------------
# METHOD 2: .keys()
# ------------------------------------------------------------------------------
"""
EXPLANATION:
------------
.keys() returns a view of all the keys in the dictionary.

SYNTAX:
    dict.keys()

WHY USE IT:
    - Iterate over all keys
    - Check what keys exist
    - Convert to list if needed

EXAMPLE:
"""
print("\n\n--- .keys() METHOD ---")

inventory = {'apples': 50, 'bananas': 30, 'oranges': 20}

# Get all keys
print(f"✓ All products: {inventory.keys()}")

# Iterate over keys
print("✓ Products in stock:")
for product in inventory.keys():
    print(f"  - {product}")

# Convert to list
products_list = list(inventory.keys())
print(f"✓ Products as list: {products_list}")

# Check if key exists
if 'apples' in inventory.keys():  # Can also just use: if 'apples' in inventory
    print("✓ Apples are in stock!")

print("\n" + "=" * 70)
print("EXERCISE 2: .keys() Practice")
print("=" * 70)

# EXERCISE 2.1: List All Keys
print("\nExercise 2.1: Extract User IDs")
user_database = {
    'U001': {'name': 'Alice', 'status': 'active'},
    'U002': {'name': 'Bob', 'status': 'inactive'},
    'U003': {'name': 'Charlie', 'status': 'active'}
}

# TODO: Get all user IDs (keys) as a list
all_user_ids = list(user_database.keys()) # Replace this

print(f"All user IDs: {all_user_ids}")
# Expected: ['U001', 'U002', 'U003']


# EXERCISE 2.2: Find Missing Keys
print("\nExercise 2.2: Find Missing Required Fields")
required_fields = ['ticket_id', 'user_id', 'gate', 'timestamp']
event_data = {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '10:00'}

# TODO: Find which required fields are missing from event_data
# Hint: Check if each required field is in event_data.keys()
missing_fields = [key for key in required_fields if key not in event_data]  # Replace with your code

print(f"Missing fields: {missing_fields}")
# Expected: ['user_id']


# ------------------------------------------------------------------------------
# METHOD 3: .values()
# ------------------------------------------------------------------------------
"""
EXPLANATION:
------------
.values() returns a view of all the values in the dictionary.

SYNTAX:
    dict.values()

WHY USE IT:
    - Iterate over all values
    - Calculate totals/averages
    - Check if a value exists

EXAMPLE:
"""
print("\n\n--- .values() METHOD ---")

prices = {'apple': 1.50, 'banana': 0.80, 'orange': 1.20}

# Get all values
print(f"✓ All prices: {prices.values()}")

# Calculate total
total = sum(prices.values())
print(f"✓ Total cost: ${total:.2f}")

# Check if value exists
if 1.50 in prices.values():
    print("✓ Something costs $1.50")

# Get max/min
print(f"✓ Most expensive: ${max(prices.values()):.2f}")
print(f"✓ Cheapest: ${min(prices.values()):.2f}")

print("\n" + "=" * 70)
print("EXERCISE 3: .values() Practice")
print("=" * 70)

# EXERCISE 3.1: Sum Values
print("\nExercise 3.1: Calculate Total Occupancy")
occupancy_by_gate = {'gate_A': 45, 'gate_B': 32, 'gate_C': 28}

# TODO: Calculate total people across all gates
total_occupancy = sum(occupancy_by_gate.values())

print(f"Total people in venue: {total_occupancy}")
# Expected: 105


# EXERCISE 3.2: Count Specific Values
print("\nExercise 3.2: Count 'Entry' Statuses")
ticket_status = {
    'T001': 'exit',
    'T002': 'entry',
    'T003': 'entry',
    'T004': 'exit',
    'T005': 'entry'
}

# TODO: Count how many tickets have 'entry' status
# Hint: Use .values() and count
entry_count = list(ticket_status.values()).count('entry')

print(f"Tickets with 'entry' status: {entry_count}")
# Expected: 3


# EXERCISE 3.3: Find Average
print("\nExercise 3.3: Calculate Average Age")
user_ages = {'Alice': 25, 'Bob': 30, 'Charlie': 22, 'Diana': 28}

# TODO: Calculate the average age
# Hint: sum() and len()
average_age = sum(user_ages.values())/len(user_ages)


print(f"Average age: {average_age:.1f}")
# Expected: 26.2


# ------------------------------------------------------------------------------
# METHOD 4: .items()
# ------------------------------------------------------------------------------
"""
EXPLANATION:
------------
.items() returns a view of all key-value pairs as tuples.

SYNTAX:
    dict.items()

WHY USE IT:
    - Iterate over both keys and values together
    - Most common way to loop through dictionaries
    - Essential for processing dictionary data

EXAMPLE:
"""
print("\n\n--- .items() METHOD ---")

student_scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78}

# Iterate over key-value pairs
print("✓ Student scores:")
for name, score in student_scores.items():
    print(f"  {name}: {score}")

# Filter based on values
print("✓ Students who passed (>= 80):")
for name, score in student_scores.items():
    if score >= 80:
        print(f"  {name}: {score}")

# Create new dict with transformation
doubled_scores = {name: score * 2 for name, score in student_scores.items()}
print(f"✓ Doubled scores: {doubled_scores}")

print("\n" + "=" * 70)
print("EXERCISE 4: .items() Practice")
print("=" * 70)

# EXERCISE 4.1: Filter Dictionary
print("\nExercise 4.1: Find Busy Gates")
gate_traffic = {'gate_A': 150, 'gate_B': 45, 'gate_C': 200, 'gate_D': 30}

# TODO: Create a new dict with only gates that have more than 100 people
# Use .items() to iterate
busy_gates = {gate: people for gate, people in gate_traffic.items() if people > 100}

print(f"Busy gates (>100 people): {busy_gates}")
# Expected: {'gate_A': 150, 'gate_C': 200}


# EXERCISE 4.2: Convert Values
print("\nExercise 4.2: Convert Ticket Status to Boolean")
ticket_status = {'T001': 'entry', 'T002': 'exit', 'T003': 'entry'}

# TODO: Create new dict where 'entry' = True and 'exit' = False
# Use .items()
is_inside = {ticket: True if status == 'entry' else False
             for ticket, status in ticket_status.items()}

print(f"Is inside status: {is_inside}")
# Expected: {'T001': True, 'T002': False, 'T003': True}


# EXERCISE 4.3: Swap Keys and Values
print("\nExercise 4.3: Reverse Mapping")
ticket_to_user = {'T001': 'U123', 'T002': 'U456', 'T003': 'U789'}

# TODO: Create a dict that maps user_id to ticket_id (swap keys and values)
user_to_ticket = {v:k for k,v in ticket_to_user.items()}  # Replace this

print(f"User to ticket mapping: {user_to_ticket}")
# Expected: {'U123': 'T001', 'U456': 'T002', 'U789': 'T003'}


# # ==============================================================================
# # PART 2: SET OPERATIONS
# # ==============================================================================

# print("\n\n")
# print("=" * 70)
# print("PART 2: SET OPERATIONS")
# print("=" * 70)

# # ------------------------------------------------------------------------------
# # OPERATION 1: Creating Sets and add()
# # ------------------------------------------------------------------------------
# """
# EXPLANATION:
# ------------
# Sets store UNIQUE items with no duplicates. Use add() to insert items.

# SYNTAX:
#     my_set = set()           # Create empty set
#     my_set = {1, 2, 3}       # Create with items
#     my_set.add(item)         # Add single item

# WHY USE SETS:
#     - Automatic duplicate removal
#     - Fast membership checking (O(1))
#     - Track unique items
#     - Perfect for "who's inside" tracking

# EXAMPLE:
# """
# print("\n--- add() METHOD ---")

# attendees = set()

# # Adding items
# attendees.add('U123')
# attendees.add('U456')
# attendees.add('U123')  # Duplicate - won't be added again!

# print(f"✓ Attendees: {attendees}")  # Only 2 items
# print(f"✓ Count: {len(attendees)}")

# # Fast membership check
# if 'U123' in attendees:
#     print("✓ U123 is in the set!")

# print("\n" + "=" * 70)
# print("EXERCISE 5: add() Practice")
# print("=" * 70)

# # EXERCISE 5.1: Track Unique Visitors
# print("\nExercise 5.1: Count Unique Daily Visitors")
# daily_scans = ['U001', 'U002', 'U001', 'U003', 'U002', 'U001', 'U004']

# # TODO: Find how many unique users visited
# # Use a set!
# unique_visitors = set()  # Add your code

# print(f"Unique visitors: {len(unique_visitors)}")
# # Expected: 4


# # EXERCISE 5.2: Detect First-Time vs Returning
# print("\nExercise 5.2: Identify First-Time Visitors")
# known_users = {'U001', 'U002', 'U003'}
# today_scans = ['U001', 'U004', 'U002', 'U005']

# # TODO: Find which users are visiting for the first time
# # Hint: Check if each scan is NOT in known_users
# first_time_visitors = set()  # Add your code

# print(f"First-time visitors: {first_time_visitors}")
# # Expected: {'U004', 'U005'}


# # ------------------------------------------------------------------------------
# # OPERATION 2: discard() and remove()
# # ------------------------------------------------------------------------------
# """
# EXPLANATION:
# ------------
# Remove items from a set. ALWAYS prefer discard() over remove()!

# SYNTAX:
#     my_set.discard(item)     # Safe - no error if item not in set
#     my_set.remove(item)      # Unsafe - crashes if item not in set

# WHY USE discard():
#     - Doesn't crash if item doesn't exist
#     - Perfect for entry/exit tracking
#     - More robust code

# EXAMPLE:
# """
# print("\n\n--- discard() vs remove() ---")

# people_inside = {'U123', 'U456', 'U789'}

# # Using discard - SAFE
# people_inside.discard('U123')  # Removes U123
# print(f"✓ After U123 exits: {people_inside}")

# people_inside.discard('U999')  # Not in set - no error!
# print(f"✓ After trying to remove U999: {people_inside}")

# # Using remove - RISKY
# try:
#     people_inside.remove('U999')  # Crashes!
# except KeyError:
#     print("❌ remove() crashed because U999 not in set!")

# print("\n" + "=" * 70)
# print("EXERCISE 6: discard() Practice")
# print("=" * 70)

# # EXERCISE 6.1: Track Entry/Exit
# print("\nExercise 6.1: Track Venue Occupancy")
# currently_inside = set()

# events = [
#     {'user_id': 'U001', 'action': 'entry'},
#     {'user_id': 'U002', 'action': 'entry'},
#     {'user_id': 'U001', 'action': 'exit'},
#     {'user_id': 'U003', 'action': 'entry'},
#     {'user_id': 'U002', 'action': 'exit'},
# ]

# # TODO: Process events to track who's currently inside
# # Use add() for entries and discard() for exits
# for event in events:
#     pass  # Replace with your code

# print(f"Currently inside: {currently_inside}")
# # Expected: {'U003'}


# # EXERCISE 6.2: Safe Removal
# print("\nExercise 6.2: Clean Up Old Users")
# active_users = {'U001', 'U002', 'U003', 'U004'}
# users_to_remove = ['U002', 'U005', 'U003', 'U006']  # Some don't exist!

# # TODO: Remove all users in users_to_remove from active_users
# # Use discard() so it doesn't crash on missing users
# # Your code here

# print(f"Active users after cleanup: {active_users}")
# # Expected: {'U001', 'U004'}


# # ------------------------------------------------------------------------------
# # OPERATION 3: Set Operations (union, intersection, difference)
# # ------------------------------------------------------------------------------
# """
# EXPLANATION:
# ------------
# Combine or compare sets using mathematical set operations.

# SYNTAX:
#     set1 | set2              # Union (all items from both)
#     set1 & set2              # Intersection (items in both)
#     set1 - set2              # Difference (items in set1 but not set2)
#     set1 ^ set2              # Symmetric difference (items in either but not both)

# WHY USE THEM:
#     - Find common visitors
#     - Find unique visitors
#     - Compare groups

# EXAMPLE:
# """
# print("\n\n--- SET OPERATIONS ---")

# monday_visitors = {'U001', 'U002', 'U003', 'U004'}
# tuesday_visitors = {'U003', 'U004', 'U005', 'U006'}

# # Union - all visitors across both days
# all_visitors = monday_visitors | tuesday_visitors
# print(f"✓ All visitors (union): {all_visitors}")

# # Intersection - visitors on both days
# both_days = monday_visitors & tuesday_visitors
# print(f"✓ Visited both days (intersection): {both_days}")

# # Difference - only Monday, not Tuesday
# only_monday = monday_visitors - tuesday_visitors
# print(f"✓ Only Monday (difference): {only_monday}")

# # Symmetric difference - visited exactly one day
# one_day_only = monday_visitors ^ tuesday_visitors
# print(f"✓ One day only (symmetric diff): {one_day_only}")

# print("\n" + "=" * 70)
# print("EXERCISE 7: Set Operations Practice")
# print("=" * 70)

# # EXERCISE 7.1: Find Regular Visitors
# print("\nExercise 7.1: Find People Who Attended All 3 Days")
# day1_visitors = {'U001', 'U002', 'U003', 'U004', 'U005'}
# day2_visitors = {'U002', 'U003', 'U005', 'U006'}
# day3_visitors = {'U003', 'U005', 'U007'}

# # TODO: Find visitors who came all 3 days
# # Use intersection (&)
# regular_visitors = set()  # Replace this

# print(f"Attended all 3 days: {regular_visitors}")
# # Expected: {'U003', 'U005'}


# # EXERCISE 7.2: Find New Visitors
# print("\nExercise 7.2: Find Today's New Visitors")
# previous_visitors = {'U001', 'U002', 'U003', 'U004'}
# today_visitors = {'U003', 'U004', 'U005', 'U006', 'U007'}

# # TODO: Find who visited today but never before
# # Use difference (-)
# new_today = set()  # Replace this

# print(f"New visitors today: {new_today}")
# # Expected: {'U005', 'U006', 'U007'}


# # EXERCISE 7.3: Find VIP and Regular Split
# print("\nExercise 7.3: Categorize Ticket Types")
# vip_ticket_holders = {'U001', 'U002', 'U003'}
# all_attendees = {'U001', 'U002', 'U003', 'U004', 'U005', 'U006'}

# # TODO: Find who has regular (non-VIP) tickets
# # Use difference (-)
# regular_ticket_holders = set()  # Replace this

# print(f"VIP tickets: {vip_ticket_holders}")
# print(f"Regular tickets: {regular_ticket_holders}")
# # Expected Regular: {'U004', 'U005', 'U006'}


# # ==============================================================================
# # PART 3: COMBINED CHALLENGES
# # ==============================================================================

# print("\n\n")
# print("=" * 70)
# print("PART 3: COMBINED CHALLENGES - Using Dicts AND Sets Together")
# print("=" * 70)

# # CHALLENGE 1: Real-World Occupancy Tracker
# print("\nCHALLENGE 1: Complete Occupancy System")
# print("-" * 70)

# def process_venue_events(events):
#     """
#     Process a stream of entry/exit events and return statistics.
    
#     Args:
#         events: List of dicts with 'user_id', 'gate', 'action' ('entry'/'exit')
    
#     Returns:
#         dict with:
#             - 'currently_inside': set of user_ids currently in venue
#             - 'total_entries': total entry count
#             - 'total_exits': total exit count
#             - 'entries_by_gate': dict of gate -> entry count
#             - 'peak_occupancy': highest number of people inside at once
#     """
#     # TODO: Implement this function
#     # You'll need: sets for tracking who's inside, dicts for counting
    
#     currently_inside = set()
#     total_entries = 0
#     total_exits = 0
#     entries_by_gate = {}
#     peak_occupancy = 0
    
#     # Your code here
    
#     return {
#         'currently_inside': currently_inside,
#         'total_entries': total_entries,
#         'total_exits': total_exits,
#         'entries_by_gate': entries_by_gate,
#         'peak_occupancy': peak_occupancy
#     }

# # Test data
# test_events = [
#     {'user_id': 'U001', 'gate': 'A', 'action': 'entry'},
#     {'user_id': 'U002', 'gate': 'B', 'action': 'entry'},
#     {'user_id': 'U003', 'gate': 'A', 'action': 'entry'},
#     {'user_id': 'U001', 'gate': 'A', 'action': 'exit'},
#     {'user_id': 'U004', 'gate': 'B', 'action': 'entry'},
#     {'user_id': 'U002', 'gate': 'B', 'action': 'exit'},
# ]

# result = process_venue_events(test_events)
# print(f"Result: {result}")
# # Expected: {
# #     'currently_inside': {'U003', 'U004'},
# #     'total_entries': 4,
# #     'total_exits': 2,
# #     'entries_by_gate': {'A': 2, 'B': 2},
# #     'peak_occupancy': 3
# # }


# # CHALLENGE 2: Anomaly Detection
# print("\n\nCHALLENGE 2: Detect Suspicious Activity")
# print("-" * 70)

# def detect_suspicious_scans(events):
#     """
#     Find suspicious scanning patterns:
#     - Users who exited without entering
#     - Users who tried to enter while already inside
    
#     Args:
#         events: List of dicts with 'user_id' and 'action'
    
#     Returns:
#         dict with 'exit_without_entry' and 'double_entry' sets
#     """
#     # TODO: Implement this
#     # Hint: Track who's inside, check for invalid transitions
    
#     currently_inside = set()
#     exit_without_entry = set()
#     double_entry = set()
    
#     # Your code here
    
#     return {
#         'exit_without_entry': exit_without_entry,
#         'double_entry': double_entry
#     }

# # Test data
# suspicious_events = [
#     {'user_id': 'U001', 'action': 'entry'},
#     {'user_id': 'U002', 'action': 'exit'},      # Suspicious: exit without entry
#     {'user_id': 'U001', 'action': 'entry'},     # Suspicious: already inside
#     {'user_id': 'U003', 'action': 'entry'},
#     {'user_id': 'U003', 'action': 'exit'},
# ]

# suspicious_result = detect_suspicious_scans(suspicious_events)
# print(f"Suspicious activity: {suspicious_result}")
# Expected: {
#     'exit_without_entry': {'U002'},
#     'double_entry': {'U001'}
# }


# ==============================================================================
# SOLUTIONS (Uncomment to see answers)
# ==============================================================================

# """
# SOLUTIONS - Try the exercises first before looking!

# # Exercise 1.1
# user_id = event.get('user_id', 'GUEST')

# # Exercise 1.2
# for scan in scans:
#     gate_counts[scan] = gate_counts.get(scan, 0) + 1

# # Exercise 1.3
# timeout = config.get('timeout')
# max_connections = config.get('max_connections', 100)
# debug_mode = config.get('debug_mode', False)

# # Exercise 2.1
# all_user_ids = list(user_database.keys())

# # Exercise 2.2
# missing_fields = [field for field in required_fields if field not in event_data.keys()]

# # Exercise 3.1
# total_occupancy = sum(occupancy_by_gate.values())

# # Exercise 3.2
# entry_count = sum(1 for status in ticket_status.values() if status == 'entry')
# # OR: entry_count = list(ticket_status.values()).count('entry')

# # Exercise 3.3
# average_age = sum(user_ages.values()) / len(user_ages)

# # Exercise 4.1
# busy_gates = {gate: count for gate, count in gate_traffic.items() if count > 100}

# # Exercise 4.2
# is_inside = {ticket: (status == 'entry') for ticket, status in ticket_status.items()}

# # Exercise 4.3
# user_to_ticket = {user: ticket for ticket, user in ticket_to_user.items()}

# # Exercise 5.1
# for user in daily_scans:
#     unique_visitors.add(user)

# # Exercise 5.2
# for user in today_scans:
#     if user not in known_users:
#         first_time_visitors.add(user)

# # Exercise 6.1
# for event in events:
#     if event['action'] == 'entry':
#         currently_inside.add(event['user_id'])
#     elif event['action'] == 'exit':
#         currently_inside.discard(event['user_id'])

# # Exercise 6.2
# for user in users_to_remove:
#     active_users.discard(user)

# # Exercise 7.1
# regular_visitors = day1_visitors & day2_visitors & day3_visitors

# # Exercise 7.2
# new_today = today_visitors - previous_visitors

# # Exercise 7.3
# regular_ticket_holders = all_attendees - vip_ticket_holders

# # Challenge 1
# for event in events:
#     user_id = event['user_id']
#     gate = event['gate']
#     action = event['action']
    
#     if action == 'entry':
#         currently_inside.add(user_id)
#         total_entries += 1
#         entries_by_gate[gate] = entries_by_gate.get(gate, 0) + 1
#     elif action == 'exit':
#         currently_inside.discard(user_id)
#         total_exits += 1
    
#     # Track peak
#     peak_occupancy = max(peak_occupancy, len(currently_inside))

# # Challenge 2
# for event in events:
#     user_id = event['user_id']
#     action = event['action']
    
#     if action == 'entry':
#         if user_id in currently_inside:
#             double_entry.add(user_id)
#         currently_inside.add(user_id)
#     elif action == 'exit':
#         if user_id not in currently_inside:
#             exit_without_entry.add(user_id)
#         currently_inside.discard(user_id)
# """

print("\n\n" + "=" * 70)
print("EXERCISES COMPLETE!")
print("=" * 70)
print("\nTry solving all exercises before checking the solutions at the bottom.")
print("Good luck with your tech test! 🚀")