# Python Occupancy Practice - Tech Interview Prep
# ===============================================
# Complete practice module for CrowdComms Junior API Developer interview
#
# Focus: Python data structures, streaming data, JSON parsing
# Time: ~2-3 hours to complete all 5 questions
#
# Progress through Q1 → Q2 → Q3 → Q4 → Q5 (increasing difficulty)

import json
from collections import defaultdict, Counter, deque
from typing import Dict, List, Set
from datetime import datetime, timedelta

# ===========================================================================
# MOCK DATA - Simulates Real Event System
# ===========================================================================

def get_mock_tickets():
    """
    Ticket table data.
    In production: SELECT * FROM tickets
    """
    return [
        {'ticket_id': 'T001', 'user_id': 'U123', 'ticket_type': 'VIP', 'price': 150.00},
        {'ticket_id': 'T002', 'user_id': 'U456', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T003', 'user_id': 'U789', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T004', 'user_id': 'U111', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T005', 'user_id': 'U222', 'ticket_type': 'VIP', 'price': 150.00},
        {'ticket_id': 'T006', 'user_id': 'U333', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T007', 'user_id': 'U444', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T008', 'user_id': 'U123', 'ticket_type': 'General', 'price': 50.00},
    ]


def mock_scan_stream():
    """
    Generator yielding scan events as JSON strings (realistic API format).

    Simulates:
    - Gate scanners sending JSON via HTTP POST
    - Message queues delivering JSON events
    - WebSocket streaming JSON

    Key test scenarios:
    - T003 enters twice without exiting (duplicate - should be ignored)
    - T008 same user as T001 (one user, multiple tickets - both valid)
    - Mixed VIP and General tickets
    """
    events = [
        '{"ticket_id": "T001", "gate": "A", "timestamp": "2025-09-30T10:00:00", "scan_type": "entry"}',
        '{"ticket_id": "T002", "gate": "A", "timestamp": "2025-09-30T10:01:00", "scan_type": "entry"}',
        '{"ticket_id": "T003", "gate": "B", "timestamp": "2025-09-30T10:02:00", "scan_type": "entry"}',
        '{"ticket_id": "T004", "gate": "C", "timestamp": "2025-09-30T10:03:00", "scan_type": "entry"}',
        '{"ticket_id": "T005", "gate": "B", "timestamp": "2025-09-30T10:05:00", "scan_type": "entry"}',
        '{"ticket_id": "T001", "gate": "A", "timestamp": "2025-09-30T11:00:00", "scan_type": "exit"}',
        '{"ticket_id": "T006", "gate": "A", "timestamp": "2025-09-30T11:05:00", "scan_type": "entry"}',
        '{"ticket_id": "T002", "gate": "A", "timestamp": "2025-09-30T11:10:00", "scan_type": "exit"}',
        '{"ticket_id": "T003", "gate": "B", "timestamp": "2025-09-30T11:15:00", "scan_type": "entry"}',  # DUPLICATE!
        '{"ticket_id": "T007", "gate": "C", "timestamp": "2025-09-30T11:20:00", "scan_type": "entry"}',
        '{"ticket_id": "T008", "gate": "A", "timestamp": "2025-09-30T11:25:00", "scan_type": "entry"}',
        '{"ticket_id": "T003", "gate": "B", "timestamp": "2025-09-30T12:00:00", "scan_type": "exit"}',
        '{"ticket_id": "T004", "gate": "C", "timestamp": "2025-09-30T12:05:00", "scan_type": "exit"}',
    ]
    for event_json in events:
        yield event_json


# ===========================================================================
# QUESTION 1: Basic Occupancy Tracking (EASY)
# ===========================================================================

"""
🎯 LEARNING OBJECTIVE: Sets and streaming data
===============================================

SCENARIO: Track how many people are currently inside the venue

KEY CONCEPTS:
- Sets for automatic duplicate handling
- Streaming data processing (can't rewind!)
- JSON parsing with json.loads()
- Generator pattern

DATA STRUCTURES:
- set() for O(1) lookups and automatic deduplication
- .add() to add items
- .discard() to remove (safe - no error if missing)

INTERVIEW TIP:
Talk through your approach:
"I'll use a set because it gives O(1) membership testing and automatically
prevents duplicates. I'll parse each JSON event, add ticket IDs on entry,
and remove them on exit."
"""

def count_current_occupancy(stream) -> int:
    """
    Count how many people are currently inside the venue.

    Args:
        stream: Generator yielding JSON strings of scan events

    Returns:
        int: Final occupancy count

    Example:
        >>> count_current_occupancy(mock_scan_stream())
        5

    Interview discussion points:
    - Why set over list? O(1) vs O(n) lookup
    - Why .discard() over .remove()? Safe for exits without entry
    - How to handle duplicates? Set ignores them automatically
    """
#  first ill handle any imports i need, in this case just the JSON lib.

# Ill set up any datastructures or variables next
# so a set in this case and ill name is appropriatly - current_occupancy seems right

# I'll need to run checks on each scan.
# For this ill use a for loop

# first each scan will need to be converted to a python dict from the JSON string - googles this ....
# https://docs.python.org - searches JSON

# I can use json.loads(scan) and save as a variable
# I should keep a record of the ticket_ids. 

# I can use an if statement in the for loop

# if scan_type == 'entry'
#    .add it to the set
# else 
#  .discard from set

# I'll use use disgard here as itwont though an error if the id isnt in the set.

# if a dupe comes, the ticket_id wont be added.

# and if the scan type isn't entry' it must 'exit' so then I can remove the ticket_id from the set

# The function is expecting to return an integer.
# so I'll use len() on the set to get the final number of tickets currently in the event

#use set to store ticket_ids
#loop through checking each scan
#convert each scan from json to a dict
#in the loop - set up variable names
#use if statement - 
# if scan_type == 'entry' - set.add(ticket_id)
# else set.discard(ticket_id)
#return len(set)

    current_occupancy = set()
    
    for json_scan in stream:
        scan = json.loads(json_scan)
        ticket_id = scan['ticket_id']
        scan_type = scan['scan_type']
        
        if scan_type == 'entry':
            current_occupancy.add(ticket_id)
        else:
            current_occupancy.discard(ticket_id)
        
    return len(current_occupancy)

# ===========================================================================
# QUESTION 2: Time-Based Occupancy (MEDIUM)
# ===========================================================================

"""
🎯 LEARNING OBJECTIVE: DateTime filtering
==========================================

SCENARIO: "How many people were inside at 11:30am?"

KEY CONCEPTS:
- datetime.fromisoformat() to parse ISO timestamps
- Comparing datetime objects
- Early loop termination with break
- Time-based filtering

INTERVIEW TIP:
"I'll parse timestamps to datetime objects so I can compare them. I'll use
break to stop processing once we pass the target time - this is efficient
because we don't process unnecessary future events."
"""

def get_occupancy_at_time(stream, target_time: str) -> int:
    """
    Get occupancy count at a specific point in time.

    Args:
        stream: Generator yielding JSON strings
        target_time: ISO format timestamp (e.g., '2025-09-30T11:30:00')

    Returns:
        int: Occupancy at target time

    Example:
        >>> get_occupancy_at_time(mock_scan_stream(), '2025-09-30T11:30:00')
        6

    Edge cases to discuss:
    - What if target_time is before all events? Return 0
    - What if target_time is after all events? Return final occupancy
    - What if no scan at exact target time? Use >= to stop at first scan after
    """
    current_occupancy = set()
    
    target_time_dt = datetime.fromisoformat(target_time)

    for json_scan in stream:
        scan = json.loads(json_scan)
        ticket_id = scan['ticket_id']
        scan_type = scan['scan_type']
        timestamp = datetime.fromisoformat(scan['timestamp'])
        
        if timestamp > target_time_dt:
            break

        if scan_type == 'entry':
            current_occupancy.add(ticket_id)
        else:
            current_occupancy.discard(ticket_id)

    return len(current_occupancy)


# ===========================================================================
# QUESTION 3: Detailed Tracking with Multiple Metrics (MEDIUM-HARD)
# ===========================================================================

"""
🎯 LEARNING OBJECTIVE: Dictionary comprehension, defaultdict, multiple counters
================================================================================

SCENARIO: API endpoint needs rich data - occupancy by gate, by ticket type, etc.

KEY CONCEPTS:
- defaultdict(int) for auto-initializing counters
- Dictionary comprehension for fast lookups
- Tracking multiple metrics simultaneously
- Increment AND decrement patterns

DATA STRUCTURES:
- defaultdict(int) - auto-initializes to 0
- dict comprehension - {key: value for item in list}
- set - for current occupancy

INTERVIEW TIP:
"I need ticket types but the stream doesn't include them. I'll build a lookup
dictionary from the tickets table using a dict comprehension, then use it for
O(1) lookups as I process the stream."
"""

def track_occupancy_with_details(stream) -> Dict:
    """
    Track detailed occupancy metrics.

    Returns:
        {
            'total_occupancy': 4,
            'by_gate': {'A': 2, 'B': 2, 'C': 1},
            'by_ticket_type': {'VIP': 2, 'General': 3},
            'total_entries': 8,
            'total_exits': 4
        }

    Key insight:
    - by_gate and by_ticket_type need BOTH increment AND decrement
    - total_entries only counts valid entries (check if already inside first)
    """
    total_occupancy = set()
    total_entries = 0
    total_exits = 0
    gate_count = defaultdict(int)
    total_ticket_type = defaultdict(int)
    
    id_to_ticket_type = {t['ticket_id']: t['ticket_type'] for t in get_mock_tickets()}
    
    for json_scan in stream:
        scan = json.loads(json_scan)
        ticket_id = scan['ticket_id']
        scan_type = scan['scan_type']
        gate = scan['gate']

       
        
        if scan_type == "entry" and ticket_id not in total_occupancy:
            gate_count[gate] += 1
            total_occupancy.add(ticket_id)
            total_entries += 1
            total_ticket_type[id_to_ticket_type[ticket_id]] += 1
            
        elif scan_type == 'exit':

            total_occupancy.discard(ticket_id)
            total_exits += 1
            total_ticket_type[id_to_ticket_type[ticket_id]] -= 1
            
    return {
        'total_occupancy': len(total_occupancy),
        'by_gate': dict(gate_count),
        'by_ticket_type': dict(total_ticket_type),
        'total_entries': total_entries,
        'total_exits': total_exits,
        
    }

# ===========================================================================
# QUESTION 4: Anomaly Detection (HARD)
# ===========================================================================

"""
🎯 LEARNING OBJECTIVE: Complex state tracking, timedelta, multiple conditions
==============================================================================

SCENARIO: Security needs to detect suspicious scan patterns

ANOMALIES TO DETECT:
1. Duplicate entries - trying to enter when already inside
2. Exit without entry - trying to exit when not inside
3. Rapid re-entry - re-entering within 5 minutes of exit

KEY CONCEPTS:
- Tracking multiple states (inside, last_exit_time)
- timedelta for time differences
- Multiple sets for different anomaly types
- Explicit condition checking (avoid else for clarity)

INTERVIEW TIP:
"I'll track who's inside with a set, and last exit times with a dict. For each
scan, I'll check the appropriate anomaly condition before processing normally."
"""

def detect_scan_anomalies(stream) -> Dict[str, Set[str]]:
    """
    Detect suspicious scan patterns.

    Returns:
        {
            'duplicate_entries': {'T003'},
            'exit_without_entry': set(),
            'rapid_reentry': set()
        }

    Time complexity discussion:
    - Set membership: O(1)
    - Dict lookup: O(1)
    - Overall: O(n) where n = number of scans
    """
    # TODO: Implement this function
    pass


# ===========================================================================
# QUESTION 5: Capacity Management (VERY HARD)
# ===========================================================================

"""
🎯 LEARNING OBJECTIVE: All concepts combined + business logic
==============================================================

SCENARIO: Venue has capacity limits, VIPs get priority

BUSINESS RULES:
- Standard + VIP can enter up to max_capacity
- Once at max_capacity, ONLY VIPs can enter
- Track rejections for analytics
- Calculate "would-be occupancy" without limits

This combines everything:
✓ Sets (current occupancy)
✓ Dict lookup (ticket types)
✓ Multiple counters
✓ Complex conditional logic
✓ Multiple simultaneous states

INTERVIEW TIP:
"I'll track actual occupancy separately from theoretical occupancy. I'll check
capacity before allowing entry, with special handling for VIPs when at capacity."
"""

def manage_capacity_realtime(stream, max_capacity: int = 6) -> Dict:
    """
    Enforce capacity limits with VIP priority.

    Args:
        stream: Scan events
        max_capacity: Max occupancy for general admission

    Returns:
        {
            'final_occupancy': 5,
            'times_at_capacity': 2,
            'rejected_entries': ['T007'],
            'would_be_occupancy': 6,
            'vip_override_count': 1
        }

    Discussion points:
    - What about race conditions? (Use database transactions in production)
    - What if capacity changes mid-event? (Could use time-based capacity)
    - How to notify rejected users? (Return rejection in API response)
    """
    # TODO: Implement this function
    pass


# ===========================================================================
# BONUS: Counter Examples (Counting vs Tracking State)
# ===========================================================================

"""
🎯 WHEN TO USE COUNTER
======================

Counter is perfect for COUNTING occurrences (not tracking current state).

Use Counter when:
- Counting "how many times X happened"
- Finding most common items
- Don't need to decrement

Don't use Counter when:
- Tracking current state with +1/-1 (use defaultdict)
- Need to know "who's inside now" (use set)
"""

def analyze_scan_patterns(stream) -> Dict:
    """
    Use Counter for analytics - counting total scans.

    Returns:
        {
            'scans_per_gate': Counter({'A': 6, 'B': 4, 'C': 2}),
            'busiest_gates': [('A', 6), ('B', 4)],
            'entries_by_type': Counter({'General': 5, 'VIP': 3})
        }
    """
    # TODO: Implement this function
    pass


# ===========================================================================
# BONUS: Deque Examples (Sliding Window / Recent Events)
# ===========================================================================

"""
🎯 WHEN TO USE DEQUE
====================

Deque (double-ended queue) is perfect for:
- FIFO queues (appendleft/pop)
- Sliding windows (maxlen parameter)
- Recent N items tracking

Use deque when:
- Need fast operations at BOTH ends (O(1))
- Want automatic size limiting (maxlen)
- Building queues or sliding windows

Don't use deque when:
- Need random access by index (use list)
- Need to search/lookup (use set/dict)
"""

def track_recent_activity(stream, window_size: int = 100) -> Dict:
    """
    Keep only the last N scans in memory (sliding window).

    Real-world use case:
    - "Show last 100 scans" dashboard widget
    - Recent activity feed
    - Memory-efficient for infinite streams

    Returns:
        {
            'recent_scans': deque of last 100 events,
            'current_occupancy': 5,
            'recent_entry_count': 45
        }
    """
    # TODO: Implement this function
    pass


# ===========================================================================
# TEST RUNNER
# ===========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PYTHON OCCUPANCY PRACTICE - TEST RESULTS")
    print("=" * 70)

    # Q1: Basic Occupancy
    result1 = count_current_occupancy(mock_scan_stream())
    print(f"\nQ1 - Current occupancy: {result1}")
    print(f"     Expected: 5 tickets inside")

    # Q2: Time-Based
    result2 = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T11:30:00')
    print(f"\nQ2 - Occupancy at 11:30am: {result2}")
    print(f"     Expected: 6 tickets inside")

    # Q3: Detailed Tracking
    result3 = track_occupancy_with_details(mock_scan_stream())
    print(f"\nQ3 - Detailed metrics:")
    for key, value in result3.items():
        print(f"     {key}: {value}")

    # # Q4: Anomaly Detection
    # result4 = detect_scan_anomalies(mock_scan_stream())
    # print(f"\nQ4 - Anomalies detected:")
    # for anomaly_type, tickets in result4.items():
    #     print(f"     {anomaly_type}: {tickets}")

    # # Q5: Capacity Management
    # result5 = manage_capacity_realtime(mock_scan_stream(), max_capacity=6)
    # print(f"\nQ5 - Capacity management:")
    # for key, value in result5.items():
    #     print(f"     {key}: {value}")

    # # Bonus: Counter
    # result6 = analyze_scan_patterns(mock_scan_stream())
    # print(f"\nBONUS - Scan patterns (Counter):")
    # print(f"     Busiest gates: {result6['busiest_gates']}")
    # print(f"     Entries by type: {result6['entries_by_type']}")

    # # Bonus: Deque
    # result7 = track_recent_activity(mock_scan_stream(), window_size=5)
    # print(f"\nBONUS - Recent activity (deque):")
    # print(f"     Last 5 scans: {[s['ticket_id'] for s in result7['recent_scans']]}")
    # print(f"     Current occupancy: {result7['current_occupancy']}")

    # print("\n" + "=" * 70)
    # print("ALL TESTS COMPLETE!")
    # print("=" * 70)
