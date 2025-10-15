# Python Cheat Sheet - CrowdComms Interview Prep
Quick reference for Python concepts with real-world event system scenarios

---

## Table of Contents
1. [Data Structures](#data-structures)
2. [Dictionary Methods](#dictionary-methods)
3. [Set Operations](#set-operations)
4. [Collections Module](#collections-module)
5. [List Comprehensions](#list-comprehensions)
6. [Common Patterns](#common-patterns)
7. [DateTime Operations](#datetime-operations)
8. [JSON Handling](#json-handling)
9. [Interview Talking Points](#interview-talking-points)

---

## Data Structures

### When to Use What

| Data Structure | Use When | Example Scenario |
|---------------|----------|------------------|
| **list** | Ordered collection, duplicates allowed | Store scan events in order |
| **dict** | Need key-value lookups | Map ticket_id → ticket_type |
| **set** | Track unique items, fast membership | Track who's currently inside |
| **tuple** | Immutable data, dict keys | Store coordinates, config |

### Time Complexity Quick Reference

| Operation | List | Dict | Set |
|-----------|------|------|-----|
| Access by index/key | O(1) | O(1) | N/A |
| Search (in) | O(n) | O(1) | O(1) |
| Insert | O(1)* | O(1) | O(1) |
| Delete | O(n) | O(1) | O(1) |

*append is O(1), insert at position is O(n)

---

## Dictionary Methods

### `.get(key, default)`
**Real-world scenarios:**
- Safe access to optional fields in API responses
- Counting patterns (vote tallying, gate traffic)
- Configuration with fallback defaults

**Interview answer:** "I use .get() instead of bracket notation because it prevents KeyError crashes when keys might not exist, which is common when processing variable API responses."

```python
# ❌ BAD - Crashes if 'country' doesn't exist
country = user_data['country']

# ✅ GOOD - Returns None if not found
country = user_data.get('country')

# ✅ BEST - Returns custom default
country = user_data.get('country', 'Unknown')

# CRITICAL PATTERN: Counting
gate_counts = {}
for scan in scans:
    gate = scan['gate']
    gate_counts[gate] = gate_counts.get(gate, 0) + 1
```

### `.keys()`
**Real-world scenarios:**
- Check what fields are present in event data
- Validate required fields before processing
- Iterate over all user IDs

```python
tickets = {'T001': {...}, 'T002': {...}}

# Get all keys as list
ticket_ids = list(tickets.keys())

# Check what fields exist
required = ['ticket_id', 'user_id', 'gate']
missing = [f for f in required if f not in event.keys()]
```

### `.values()`
**Real-world scenarios:**
- Calculate totals (sum occupancy across gates)
- Find max/min (busiest gate, peak time)
- Check if a value exists anywhere

```python
occupancy_by_gate = {'A': 45, 'B': 32, 'C': 28}

total = sum(occupancy_by_gate.values())  # 105
busiest = max(occupancy_by_gate.values())  # 45
```

### `.items()`
**Real-world scenarios:**
- Most common way to iterate over dictionaries
- Filter dict based on values
- Transform dict to new dict

**Interview answer:** "I use .items() when I need both the key and value together, which is most of the time when processing dictionaries."

```python
gate_traffic = {'A': 150, 'B': 45, 'C': 200}

# Iterate over key-value pairs
for gate, count in gate_traffic.items():
    print(f"Gate {gate}: {count} people")

# Filter dictionary
busy_gates = {g: c for g, c in gate_traffic.items() if c > 100}
```

---

## Set Operations

### Basic Operations

```python
inside = set()

# Add item
inside.add('T001')

# Remove item (SAFE - no error if not present)
inside.discard('T001')

# ❌ NEVER USE - crashes if not present
inside.remove('T001')  # KeyError if not in set!

# Check membership (O(1) - very fast!)
if 'T001' in inside:
    print("T001 is inside")

# Count items
occupancy = len(inside)
```

**Interview answer:** "I always use discard() over remove() for entry/exit tracking because discard won't crash if someone tries to exit without entering - it's more robust for real-world scenarios."

### Set Mathematics

```python
monday = {'U001', 'U002', 'U003', 'U004'}
tuesday = {'U003', 'U004', 'U005', 'U006'}

# Union (|) - All visitors across both days
all_visitors = monday | tuesday
# Result: {'U001', 'U002', 'U003', 'U004', 'U005', 'U006'}

# Intersection (&) - Visitors on BOTH days (regulars!)
regulars = monday & tuesday
# Result: {'U003', 'U004'}

# Difference (-) - Only Monday, not Tuesday
only_monday = monday - tuesday
# Result: {'U001', 'U002'}

# Symmetric Difference (^) - Visited exactly ONE day
one_day_only = monday ^ tuesday
# Result: {'U001', 'U002', 'U005', 'U006'}
```

**Real-world scenarios:**
- Find regular attendees (intersection)
- Find new visitors (difference)
- Find VIP vs General split (difference)
- Detect ticket sharing (compare across days)

---

## Collections Module

### Counter - Counting Occurrences

**Real-world scenarios:**
- Count scans per gate
- Analyze ticket type distribution
- Find most common scan patterns
- Frequency analysis

**When to use:** Need to count how many times items appear
**When NOT to use:** Need to increment/decrement (use defaultdict(int) instead)

```python
from collections import Counter

# Count items in list
scans = ['gate_A', 'gate_B', 'gate_A', 'gate_C', 'gate_A']
gate_counts = Counter(scans)
# Result: Counter({'gate_A': 3, 'gate_B': 1, 'gate_C': 1})

# Most common items
top_gate = gate_counts.most_common(1)
# Result: [('gate_A', 3)]

top_2_gates = gate_counts.most_common(2)
# Result: [('gate_A', 3), ('gate_B', 1)]

# Count from generator/comprehension
ticket_types = Counter(t['ticket_type'] for t in tickets)
```

**Interview answer:** "Counter is perfect when I need to tally occurrences, especially with .most_common() for analytics. But for entry/exit tracking where I need to decrement, I use defaultdict(int) instead."

### defaultdict - Auto-Initializing Dictionaries

**Real-world scenarios:**
- Track occupancy changes (+1 entry, -1 exit)
- Build nested structures (gate → list of users)
- Avoid KeyError when building dicts

```python
from collections import defaultdict

# For counting with +/- operations
occupancy_by_gate = defaultdict(int)
for scan in scans:
    gate = scan['gate']
    if scan['type'] == 'entry':
        occupancy_by_gate[gate] += 1  # Auto-creates with 0
    else:
        occupancy_by_gate[gate] -= 1

# For grouping
users_by_gate = defaultdict(list)
for scan in scans:
    users_by_gate[scan['gate']].append(scan['user_id'])
```

**Default factories:**
- `defaultdict(int)` → 0
- `defaultdict(list)` → []
- `defaultdict(set)` → set()
- `defaultdict(dict)` → {}

### deque - Double-Ended Queue

**Real-world scenarios:**
- Process scans in FIFO order
- Keep last N events (sliding window)
- Real-time activity feed
- Memory-efficient streaming

**Interview answer:** "deque is perfect for sliding windows - like tracking the last 100 scans for anomaly detection. The maxlen parameter automatically removes old items, so memory stays constant even with infinite streams."

```python
from collections import deque

# FIFO queue (process in order)
scan_queue = deque()
scan_queue.append('T001')
scan_queue.append('T002')
first = scan_queue.popleft()  # O(1) - very fast!

# Sliding window (last N items)
recent_scans = deque(maxlen=100)
for scan in infinite_stream:
    recent_scans.append(scan)  # Auto-removes oldest when full

    # Always contains last 100 scans
    if anomaly_detected(recent_scans):
        alert_security()
```

---

## List Comprehensions

### Basic Syntax

```python
# [expression for item in iterable if condition]

# Get all ticket IDs
ticket_ids = [t['ticket_id'] for t in tickets]

# Filter active tickets
active = [t for t in tickets if t['is_valid']]

# Transform data
prices = [t['price'] * 1.1 for t in tickets]  # 10% increase
```

### Dictionary Comprehension

**Real-world scenarios:**
- Build lookup tables (ticket_id → ticket_type)
- Filter dictionaries (only busy gates)
- Transform keys/values

```python
# Build lookup dict
tickets = [
    {'ticket_id': 'T001', 'ticket_type': 'VIP'},
    {'ticket_id': 'T002', 'ticket_type': 'General'}
]

ticket_lookup = {t['ticket_id']: t['ticket_type'] for t in tickets}
# Result: {'T001': 'VIP', 'T002': 'General'}

# Filter dictionary
busy_gates = {g: c for g, c in gates.items() if c > 100}

# Swap keys and values
reversed_dict = {v: k for k, v in original.items()}
```

**Interview answer:** "Dictionary comprehensions are great for building lookup tables before processing a stream - since you can't rewind a generator, I create the lookup first."

---

## Common Patterns

### Entry/Exit Tracking

```python
# Track current occupancy
currently_inside = set()

for event in stream:
    ticket_id = event['ticket_id']

    if event['scan_type'] == 'entry':
        currently_inside.add(ticket_id)
    else:
        currently_inside.discard(ticket_id)

current_occupancy = len(currently_inside)
```

**Real-world scenario:** Gate scanner → FastAPI endpoint → This code

### Counting with Dict

```python
# Count entries per gate
entries_by_gate = {}

for scan in scans:
    gate = scan['gate']
    entries_by_gate[gate] = entries_by_gate.get(gate, 0) + 1
```

### Building Lookup Tables

```python
# Build ticket_id → ticket_type lookup
# (Do this BEFORE processing stream!)
tickets_lookup = {t['ticket_id']: t for t in get_tickets()}

# Now use in stream processing
for event in stream:
    ticket_type = tickets_lookup[event['ticket_id']]['ticket_type']
```

**Interview answer:** "I build lookup tables before processing streams because generators can only be iterated once - you can't go back."

### Peak Tracking

```python
current_occupancy = set()
peak_occupancy = 0

for event in stream:
    # ... update current_occupancy ...

    peak_occupancy = max(peak_occupancy, len(current_occupancy))
```

### Anomaly Detection Pattern

```python
inside = set()
anomalies = {
    'duplicate_entries': set(),
    'exit_without_entry': set()
}

for event in stream:
    ticket = event['ticket_id']

    if event['scan_type'] == 'entry':
        if ticket in inside:
            anomalies['duplicate_entries'].add(ticket)
        else:
            inside.add(ticket)
    else:  # exit
        if ticket not in inside:
            anomalies['exit_without_entry'].add(ticket)
        else:
            inside.discard(ticket)
```

---

## DateTime Operations

### Parsing and Comparing

```python
from datetime import datetime, timedelta

# Parse ISO format string
timestamp_str = '2025-09-30T10:00:00'
dt = datetime.fromisoformat(timestamp_str)

# Compare datetimes
time1 = datetime.fromisoformat('2025-09-30T10:00:00')
time2 = datetime.fromisoformat('2025-09-30T11:00:00')

if time1 < time2:
    print("time1 is earlier")
```

**Real-world scenario:** Filter scans up to a specific time for historical queries

### Time Differences

```python
# Calculate time difference
exit_time = datetime.fromisoformat('2025-09-30T10:00:00')
entry_time = datetime.fromisoformat('2025-09-30T10:03:00')

time_diff = entry_time - exit_time  # timedelta object
seconds = time_diff.total_seconds()  # 180.0

# Check if within time window
if time_diff < timedelta(minutes=5):
    print("Rapid re-entry detected!")
```

**Real-world scenario:** Detect passback fraud (exit and re-enter within 5 minutes)

### Common Operations

```python
from datetime import datetime, timedelta

# Current time
now = datetime.now()

# Time arithmetic
one_hour_ago = now - timedelta(hours=1)
tomorrow = now + timedelta(days=1)

# Format as string
formatted = now.strftime('%Y-%m-%d %H:%M:%S')

# Parse custom format
dt = datetime.strptime('30/09/2025 10:00', '%d/%m/%Y %H:%M')
```

---

## JSON Handling

### Parsing JSON Strings

```python
import json

# Parse JSON string to Python dict
json_string = '{"ticket_id": "T001", "gate": "A"}'
event = json.loads(json_string)

# event is now a dict: {'ticket_id': 'T001', 'gate': 'A'}
ticket_id = event['ticket_id']
```

**Real-world scenario:** Gate scanners send JSON via HTTP POST, WebSocket streams deliver JSON messages

### Converting Python to JSON

```python
import json

# Python dict to JSON string
event = {'ticket_id': 'T001', 'gate': 'A'}
json_string = json.dumps(event)

# Pretty print for debugging
json_string = json.dumps(event, indent=2)
```

### Handling JSON in Streams

```python
def mock_scan_stream():
    """Generator yielding JSON strings (realistic API format)"""
    events = [
        '{"ticket_id": "T001", "gate": "A", "scan_type": "entry"}',
        '{"ticket_id": "T002", "gate": "B", "scan_type": "entry"}',
    ]
    for event_json in events:
        yield event_json

# Process stream
for event_json in mock_scan_stream():
    event = json.loads(event_json)  # Parse JSON to dict
    ticket_id = event['ticket_id']
    # ... process event ...
```

**Interview answer:** "In production, FastAPI automatically parses JSON into Pydantic models, but understanding json.loads() is important for testing and debugging."

---

## Interview Talking Points

### Why Use Sets for Occupancy?

**Answer:** "Sets are perfect for tracking who's inside because:
1. O(1) membership testing - fast to check 'is this person inside?'
2. Automatic deduplication - can't add same ticket twice
3. Memory efficient for large venues
4. Natural mapping to the problem - you're either in the set or not"

### Counter vs defaultdict(int)?

**Answer:** "I use Counter when I'm counting occurrences and need .most_common(), like 'what are the busiest gates?' But for entry/exit tracking where I need to decrement on exit, defaultdict(int) is better because Counter is meant for tallying, not state management."

### Why Pre-build Lookup Dicts?

**Answer:** "When processing a stream/generator, you can only iterate through it once - you can't rewind. So I build lookup tables (like ticket_id → ticket_type) before processing the stream. In production, these lookups would be cached in Redis."

### Dict.get() vs Bracket Notation?

**Answer:** "I use .get() when processing variable API responses where fields might not exist. It prevents KeyError crashes and lets me provide sensible defaults. The .get(key, 0) + 1 pattern is especially common for counting."

### Sets vs Lists for "Who's Inside"?

**Answer:** "Sets are O(1) for membership testing, lists are O(n). With 10,000 people at an event, checking 'is ticket T001 inside?' would scan through the whole list every time. Sets make this instant. Plus, sets automatically prevent the same ticket being added twice."

### Handling Out-of-Order Events?

**Answer:** "In a real system, you'd need to sort events by timestamp before processing, or use a database to store events and query in order. For a technical test where data arrives in order, processing linearly is fine, but I'd mention this edge case in the interview."

### Python vs SQL for This?

**Answer:** "If data is already in a database and you're doing historical queries, SQL is faster - it uses indexes and optimizes the query. But for real-time streaming from gate scanners, Python processes events as they arrive. In production, I'd use both: Python for real-time, SQL for analytics, Redis for caching current occupancy."

### Memory Efficiency for Large Streams?

**Answer:** "For infinite streams or very large datasets:
1. Use generators (yield) instead of loading all data into memory
2. Use deque with maxlen for sliding windows
3. Batch database writes instead of one-by-one
4. Use sets instead of lists for tracking state
5. Stream processing frameworks like Kafka for production scale"

---

## Quick Syntax Reference

```python
# DICTIONARIES
d = {'key': 'value'}
d.get('key', default)
d.keys()
d.values()
d.items()
{k: v for k, v in d.items() if condition}

# SETS
s = set()
s.add(item)
s.discard(item)  # SAFE
item in s  # O(1)
s1 | s2  # union
s1 & s2  # intersection
s1 - s2  # difference

# COUNTER
from collections import Counter
c = Counter(items)
c.most_common(n)

# DEQUE
from collections import deque
q = deque(maxlen=100)
q.append(item)
q.popleft()

# DATETIME
from datetime import datetime, timedelta
dt = datetime.fromisoformat(string)
diff = dt2 - dt1
if diff < timedelta(minutes=5): ...

# JSON
import json
d = json.loads(json_string)
s = json.dumps(python_dict)
```

---

## Practice Before Interview

1. **Can you explain when to use a set vs a list?**
   - Sets: unique items, fast membership, no order needed
   - Lists: order matters, duplicates allowed, need indexing

2. **How would you count entries per gate?**
   - Dict with .get(gate, 0) + 1 pattern
   - Or Counter if just need final counts

3. **How do you track who's currently inside?**
   - Set of ticket IDs
   - Add on entry, discard on exit

4. **What if someone scans twice without exiting?**
   - Set handles it automatically (can't add duplicate)
   - But should detect and flag as anomaly

5. **How would you find the busiest hour?**
   - Counter with datetime.hour as key
   - Or defaultdict(int) if need to process in order

Good luck with your interview! 🚀
