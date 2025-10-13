# Advanced Event Occupancy System - Tech Interview Prep
# ======================================================
# Practice for CrowdComms Junior API Developer Role
# Focus: Streaming data, database design, real-world event scenarios
from datetime import datetime
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Set
import psycopg2


# ===========================================================================
# MOCK DATA - Proper 3-Table Schema
# ===========================================================================

def get_mock_users():
    """User table data."""
    return [
        {'user_id': 'U123', 'email': 'alice@example.com', 'phone': '555-0001', 'name': 'Alice'},
        {'user_id': 'U456', 'email': 'bob@example.com', 'phone': '555-0002', 'name': 'Bob'},
        {'user_id': 'U789', 'email': 'charlie@example.com', 'phone': '555-0003', 'name': 'Charlie'},
        {'user_id': 'U111', 'email': 'diana@example.com', 'phone': '555-0004', 'name': 'Diana'},
        {'user_id': 'U222', 'email': 'eve@example.com', 'phone': '555-0005', 'name': 'Eve'},
        {'user_id': 'U333', 'email': 'frank@example.com', 'phone': '555-0006', 'name': 'Frank'},
        {'user_id': 'U444', 'email': 'grace@example.com', 'phone': '555-0007', 'name': 'Grace'},
    ]


def get_mock_tickets():
    """
    Ticket table data.
    Note: U123 has TWO tickets (T001 and T008) - realistic scenario!
    """
    return [
        {'ticket_id': 'T001', 'user_id': 'U123', 'ticket_type': 'VIP', 'price': 150.00},
        {'ticket_id': 'T002', 'user_id': 'U456', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T003', 'user_id': 'U789', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T004', 'user_id': 'U111', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T005', 'user_id': 'U222', 'ticket_type': 'VIP', 'price': 150.00},
        {'ticket_id': 'T006', 'user_id': 'U333', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T007', 'user_id': 'U444', 'ticket_type': 'General', 'price': 50.00},
        {'ticket_id': 'T008', 'user_id': 'U123', 'ticket_type': 'General', 'price': 50.00},  # U123's 2nd ticket
    ]


def mock_scan_stream():
    """
    Generator yielding scan events (entry/exit).

    Key scenarios in this data:
    - T003 enters twice without exiting (duplicate entry - anomaly!)
    - T008 belongs to same user as T001 (U123 has 2 tickets)
    - Mixed VIP and General tickets
    """
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
        {'ticket_id': 'T003', 'gate': 'B', 'timestamp': '2025-09-30T10:02:00', 'scan_type': 'entry'},
        {'ticket_id': 'T004', 'gate': 'C', 'timestamp': '2025-09-30T10:03:00', 'scan_type': 'entry'},
        {'ticket_id': 'T005', 'gate': 'B', 'timestamp': '2025-09-30T10:05:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T11:00:00', 'scan_type': 'exit'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T11:05:00', 'scan_type': 'entry'},

        {'ticket_id': 'T006', 'gate': 'A', 'timestamp': '2025-09-30T11:05:00', 'scan_type': 'entry'},
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T11:10:00', 'scan_type': 'exit'},
        {'ticket_id': 'T003', 'gate': 'B', 'timestamp': '2025-09-30T11:15:00', 'scan_type': 'entry'},  # DUPLICATE!
        {'ticket_id': 'T007', 'gate': 'C', 'timestamp': '2025-09-30T11:20:00', 'scan_type': 'entry'},
        {'ticket_id': 'T008', 'gate': 'A', 'timestamp': '2025-09-30T11:25:00', 'scan_type': 'entry'},  # U123's 2nd
        {'ticket_id': 'T003', 'gate': 'B', 'timestamp': '2025-09-30T12:00:00', 'scan_type': 'exit'},
        {'ticket_id': 'T004', 'gate': 'C', 'timestamp': '2025-09-30T12:05:00', 'scan_type': 'exit'},
    ]
    for event in events:
        yield event


# ===========================================================================
# DATABASE SETUP
# ===========================================================================

def setup_database():
    """
    Create the 3-table schema for event occupancy tracking.
    Run this ONCE to set up your database.
    """
    conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
    cursor = conn.cursor()

    # Drop existing tables (fresh start)
    cursor.execute("DROP TABLE IF EXISTS scans CASCADE")
    cursor.execute("DROP TABLE IF EXISTS tickets CASCADE")
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")

    # Create users table
    cursor.execute("""
        CREATE TABLE users (
            user_id VARCHAR(10) PRIMARY KEY,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20),
            name VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create tickets table with foreign key to users
    cursor.execute("""
        CREATE TABLE tickets (
            ticket_id VARCHAR(10) PRIMARY KEY,
            user_id VARCHAR(10) NOT NULL,
            ticket_type VARCHAR(20) NOT NULL,
            price DECIMAL(10, 2),
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_valid BOOLEAN DEFAULT true,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    """)

    # Create scans table with foreign key to tickets
    cursor.execute("""
        CREATE TABLE scans (
            scan_id SERIAL PRIMARY KEY,
            ticket_id VARCHAR(10) NOT NULL,
            gate VARCHAR(1) NOT NULL,
            scan_type VARCHAR(5) NOT NULL CHECK (scan_type IN ('entry', 'exit')),
            scan_time TIMESTAMP NOT NULL,
            flagged_suspicious BOOLEAN DEFAULT false,
            FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id) ON DELETE CASCADE
        )
    """)

    # Create indexes for performance
    cursor.execute("CREATE INDEX idx_scans_ticket_time ON scans(ticket_id, scan_time)")
    cursor.execute("CREATE INDEX idx_scans_gate ON scans(gate)")
    cursor.execute("CREATE INDEX idx_tickets_user ON tickets(user_id)")

    conn.commit()
    conn.close()
    print("✅ Database schema created successfully!")
    

def populate_database():
    """
    Populate all 3 tables with mock data.
    Run this AFTER setup_database().
    """
    conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute("DELETE FROM scans")
    cursor.execute("DELETE FROM tickets")
    cursor.execute("DELETE FROM users")

    # Insert users
    for user in get_mock_users():
        cursor.execute("""
            INSERT INTO users (user_id, email, phone, name)
            VALUES (%s, %s, %s, %s)
        """, (user['user_id'], user['email'], user['phone'], user['name']))

    # Insert tickets
    for ticket in get_mock_tickets():
        cursor.execute("""
            INSERT INTO tickets (ticket_id, user_id, ticket_type, price)
            VALUES (%s, %s, %s, %s)
        """, (ticket['ticket_id'], ticket['user_id'], ticket['ticket_type'], ticket['price']))

    # Insert scans
    for scan in mock_scan_stream():
        cursor.execute("""
            INSERT INTO scans (ticket_id, gate, scan_type, scan_time)
            VALUES (%s, %s, %s, %s)
        """, (scan['ticket_id'], scan['gate'], scan['scan_type'], scan['timestamp']))

    conn.commit()
    conn.close()
    print("✅ Database populated with mock data!")


"""
🐍 PYTHON LEARNING - QUESTION 1: Sets and Streaming
====================================================

CONCEPT: What is a Generator/Stream?
-------------------------------------
A generator is a function that yields values one at a time (lazy evaluation).
This is memory-efficient - you don't load all events into memory at once!

Example:
    def count_to_three():
        yield 1
        yield 2
        yield 3

    for num in count_to_three():
        print(num)  # Prints 1, then 2, then 3

Our mock_scan_stream() is a generator - it yields events one by one.
In production, this could be reading from a file, API, or Kafka stream!

CONCEPT: Sets - Fast Membership Testing
-----------------------------------------
A set is an unordered collection with NO DUPLICATES.
Sets are FAST for checking membership (O(1) vs O(n) for lists).

Operations:
    tickets_inside = set()          # Create empty set
    tickets_inside.add('T001')      # Add element
    tickets_inside.add('T001')      # Adding again does nothing (already in set)
    tickets_inside.discard('T001')  # Remove element (no error if not present)
    tickets_inside.remove('T001')   # Remove element (ERROR if not present)

    'T001' in tickets_inside        # Check membership - O(1) constant time!
    len(tickets_inside)             # Count elements

Why use sets here?
- Fast to check "is this ticket already inside?"
- Automatically handles duplicates (can't add same ticket twice)
- Easy to add/remove as people enter/exit

Example - Basic Occupancy Tracking:
------------------------------------
    def track_occupancy(events):
        inside = set()

        for event in events:
            ticket = event['ticket_id']

            if event['scan_type'] == 'entry':
                inside.add(ticket)      # Person enters
            else:
                inside.discard(ticket)  # Person exits

        return len(inside)

Key Points:
- We iterate through stream ONCE (you can't "rewind" a generator)
- Sets automatically prevent duplicates
- discard() is safer than remove() - won't crash if ticket not in set
- This tracks by TICKET_ID not user_id (one user can have multiple tickets!)

Interview Tip:
If they ask "why not use a list?", explain:
- Sets are O(1) for membership testing vs O(n) for lists
- Sets automatically prevent duplicate additions
- For large event streams, this performance difference matters!
"""


# ===========================================================================
# QUESTION 1: Basic Streaming Occupancy (EASY)
# ===========================================================================
# Interview Tip: This is the baseline - they expect you to get this quickly
# ===========================================================================

def count_current_occupancy(stream) -> int:
    """
    Count how many tickets are currently inside the venue.

    Args:
        stream: Generator yielding scan events

    Returns:
        int: Number of tickets currently inside

    Expected: 4 tickets inside at the end
    """
    current_tickets_inside = set()
    
    for event in stream:
        scan_type = event['scan_type']
        ticket_id = event['ticket_id']
        
        if scan_type == 'entry':
            current_tickets_inside.add(ticket_id)
        else:
            current_tickets_inside.discard(ticket_id)
    return len(current_tickets_inside)

"""
📚 DATABASE LEARNING - QUESTION 1
==================================

CONCEPT: Database Schema Design with Foreign Keys
--------------------------------------------------

We now have THREE related tables instead of one big table:

1. users: Who bought tickets
2. tickets: What tickets exist (each has ONE owner)
3. scans: Entry/exit events (each references ONE ticket)

Why is this better than one table?
- Avoids data duplication (user email stored once, not per scan)
- Enforces relationships (can't scan a ticket that doesn't exist)
- Makes updates easier (change user email in one place)

Setting up the tables:
----------------------
$ createdb event_venue
$ psql event_venue

Then run setup_database() in Python to create tables.

FOREIGN KEYS: The Key Concept
------------------------------
A foreign key creates a relationship between tables.

In tickets table:
    user_id VARCHAR(10) REFERENCES users(user_id)

This means:
- Every ticket MUST belong to a user that exists
- You CAN'T insert a ticket with user_id='U999' if U999 doesn't exist
- If you DELETE a user, what happens to their tickets? (CASCADE!)

Try this experiment:
-------------------
-- This will FAIL (no user U999):
INSERT INTO tickets (ticket_id, user_id, ticket_type, price)
VALUES ('T999', 'U999', 'General', 50.00);

-- This will work:
INSERT INTO tickets (ticket_id, user_id, ticket_type, price)
VALUES ('T999', 'U123', 'General', 50.00);


Basic Queries Across Tables:
-----------------------------
-- Get all scans
SELECT * FROM scans;

-- Get all tickets and their owners
SELECT t.ticket_id, t.ticket_type, u.name, u.email
FROM tickets t
JOIN users u ON t.user_id = u.user_id;

-- Count scans by type
SELECT scan_type, COUNT(*)
FROM scans
GROUP BY scan_type;

Simple Occupancy Query:
-----------------------
-- For each ticket, find its LAST scan
SELECT DISTINCT ON (ticket_id)
    ticket_id,
    scan_type,
    scan_time
FROM scans
ORDER BY ticket_id, scan_time DESC;

-- Now count how many have last scan = 'entry'
WITH last_scans AS (
    SELECT DISTINCT ON (ticket_id)
        ticket_id,
        scan_type
    FROM scans
    ORDER BY ticket_id, scan_time DESC
)
SELECT COUNT(*) as current_occupancy
FROM last_scans
WHERE scan_type = 'entry';

Interview Tip: DISTINCT ON is PostgreSQL-specific!
Other databases use ROW_NUMBER() with a window function.
"""


def count_current_occupancy_db() -> int:
    """
    DATABASE CHALLENGE 1: Find current occupancy using SQL

    Write a query that:
    1. For each ticket, finds the LAST scan event
    2. Counts tickets where last scan was 'entry'

    Hint: Use DISTINCT ON or window functions
    """
    conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
    cursor = conn.cursor()

    query = """
    WITH last_scan AS (
        SELECT DISTINCT ON(ticket_id)
            ticket_id,
            scan_type
        FROM scans
        ORDER BY ticket_id, scan_time DESC
        )
    SELECT COUNT(*)
    FROM last_scan
    WHERE scan_type = 'entry';
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


"""
🐍 PYTHON LEARNING - QUESTION 2: Working with Timestamps
=========================================================

CONCEPT: Parsing and Comparing Timestamps
------------------------------------------
Events often have timestamps. Python's datetime module helps work with them.

Parsing ISO format strings:
    from datetime import datetime

    time_str = '2025-09-30T10:00:00'
    dt = datetime.fromisoformat(time_str)
    # Result: datetime object you can compare

Comparing datetimes:
    time1 = datetime.fromisoformat('2025-09-30T10:00:00')
    time2 = datetime.fromisoformat('2025-09-30T11:00:00')

    time1 < time2   # True
    time1 == time2  # False
    time2 > time1   # True

String vs DateTime:
    # BAD - comparing strings (works but less reliable):
    '2025-09-30T10:00:00' < '2025-09-30T11:00:00'  # True (lucky!)

    # GOOD - comparing datetime objects:
    datetime.fromisoformat('2025-09-30T10:00:00') < datetime.fromisoformat('2025-09-30T11:00:00')

CHALLENGE: Occupancy at a Specific Time
----------------------------------------
You need to find who was inside at 11:30am.
Only process events BEFORE or AT target time!

Example:
    Events:
    - T001 enters at 10:00
    - T002 enters at 10:30
    - T001 exits at 11:00
    - T003 enters at 12:00  <-- IGNORE this (after 11:30)

    At 11:30am: T002 is inside (T001 left, T003 hasn't arrived)

Approach:
    def occupancy_at_time(events, target_time_str):
        target = datetime.fromisoformat(target_time_str)
        inside = set()

        for event in events:
            event_time = datetime.fromisoformat(event['timestamp'])

            # Only process events up to target time
            if event_time <= target:
                if event['scan_type'] == 'entry':
                    inside.add(event['ticket_id'])
                else:
                    inside.discard(event['ticket_id'])

        return len(inside)

Key Insight:
- Convert timestamps ONCE per event (not repeatedly)
- Use <= for comparison (include events AT target time)
- Stop processing or skip events after target time

Interview Discussion Points:
- "What if timestamps are in different timezones?" (use timezone-aware datetime)
- "What if events arrive out of order?" (need to sort first)
- "What if stream is infinite?" (can't answer historical queries, need database)

Time Deltas (for next question):
---------------------------------
    from datetime import timedelta

    time1 = datetime.fromisoformat('2025-09-30T10:00:00')
    time2 = datetime.fromisoformat('2025-09-30T10:05:00')

    diff = time2 - time1              # timedelta(minutes=5)
    diff.total_seconds()              # 300.0 seconds

    # Check if less than 5 minutes apart:
    if diff < timedelta(minutes=5):
        print("Less than 5 minutes!")
"""


# ===========================================================================
# QUESTION 2: Occupancy with Time Windows (MEDIUM)
# ===========================================================================
# Interview Tip: Shows you can handle more complex requirements
# ===========================================================================

def get_occupancy_at_time(stream, target_time: str) -> int:
    """
    Find occupancy at a specific point in time.

    Args:
        stream: Generator yielding scan events
        target_time: ISO timestamp string (e.g., '2025-09-30T11:30:00')

    Returns:
        int: Number of tickets inside at that moment

    Expected: At '2025-09-30T11:30:00' -> 6 tickets inside

    Key insight: Only process events BEFORE target_time!
    """
    # import date from datetime
    # convert strings to iso format, inc the target_time arg
    # store valid events in a set, remove with exit scans
    # if scan time > tagert_time - return length of the set
    
    
    target = datetime.fromisoformat(target_time)
    tickets_inside = set()

    for scan in stream:
        timestamp = datetime.fromisoformat(scan['timestamp'])
        ticket_id = scan['ticket_id']
        scan_type = scan['scan_type']

        if target >= timestamp:
            if scan_type == 'entry':
                tickets_inside.add(ticket_id)
            else:
                tickets_inside.discard(ticket_id)
        else:
             break
    return len(tickets_inside)

"""
📚 DATABASE LEARNING - QUESTION 2
==================================

CONCEPT: Filtering with Timestamps and JOINs
---------------------------------------------

Timestamps are crucial for event systems. PostgreSQL has great time support.

Basic timestamp queries:
------------------------
-- Events after 11am
SELECT * FROM scans
WHERE scan_time > '2025-09-30 11:00:00';

-- Events in a time range
SELECT * FROM scans
WHERE scan_time BETWEEN '2025-09-30 10:00:00' AND '2025-09-30 11:00:00';

-- Count scans per hour
SELECT
    DATE_TRUNC('hour', scan_time) as hour,
    COUNT(*) as scan_count
FROM scans
GROUP BY hour
ORDER BY hour;

Occupancy at specific time:
---------------------------
-- Find last scan for each ticket BEFORE 11:30am
WITH last_scans_before AS (
    SELECT DISTINCT ON (ticket_id)
        ticket_id,
        scan_type
    FROM scans
    WHERE scan_time <= '2025-09-30 11:30:00'
    ORDER BY ticket_id, scan_time DESC
)
SELECT COUNT(*) as occupancy_at_1130
FROM last_scans_before
WHERE scan_type = 'entry';

JOINing to get user info:
--------------------------
-- Who was inside at 11:30am?
WITH last_scans_before AS (
    SELECT DISTINCT ON (s.ticket_id)
        s.ticket_id,
        s.scan_type,
        t.user_id
    FROM scans s
    JOIN tickets t ON s.ticket_id = t.ticket_id
    WHERE s.scan_time <= '2025-09-30 11:30:00'
    ORDER BY s.ticket_id, s.scan_time DESC
)
SELECT
    ls.ticket_id,
    u.name,
    u.email
FROM last_scans_before ls
JOIN tickets t ON ls.ticket_id = t.ticket_id
JOIN users u ON t.user_id = u.user_id
WHERE ls.scan_type = 'entry';

Performance tip: Indexes!
--------------------------
Notice we created this index:
    CREATE INDEX idx_scans_ticket_time ON scans(ticket_id, scan_time);

This makes our "last scan per ticket" queries MUCH faster.
Without it, database does full table scan.

Check if index is being used:
    EXPLAIN ANALYZE
    SELECT DISTINCT ON (ticket_id) ticket_id, scan_type
    FROM scans
    ORDER BY ticket_id, scan_time DESC;

Look for "Index Scan" in the output!
"""


def get_occupancy_at_time_db(target_time: str) -> int:
    """
    DATABASE CHALLENGE 2: Find occupancy at specific time

    Write a query with timestamp filtering.

    Bonus: Join with users table to get names of people inside!
    """
    conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
    cursor = conn.cursor()

    query = """
    -- TODO: Write query with timestamp filter
    """

    cursor.execute(query, (target_time,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


"""
🐍 PYTHON LEARNING - QUESTION 3: Dictionaries and defaultdict
==============================================================

CONCEPT: Dictionaries - Key-Value Mappings
-------------------------------------------
Dictionaries map keys to values. Perfect for lookups!

Basic operations:
    ticket_types = {}                          # Empty dict
    ticket_types['T001'] = 'VIP'              # Add key-value pair
    ticket_types['T002'] = 'General'

    ticket_type = ticket_types['T001']        # Get value -> 'VIP'
    ticket_type = ticket_types.get('T999')    # Safe get -> None (no error)
    ticket_type = ticket_types.get('T999', 'Unknown')  # With default

    'T001' in ticket_types                    # Check if key exists -> True
    len(ticket_types)                         # Count entries -> 2

Building lookup dictionaries:
    # From list of ticket dicts, create ticket_id -> ticket_type mapping
    tickets = [
        {'ticket_id': 'T001', 'ticket_type': 'VIP'},
        {'ticket_id': 'T002', 'ticket_type': 'General'}
    ]

    lookup = {t['ticket_id']: t['ticket_type'] for t in tickets}
    # Result: {'T001': 'VIP', 'T002': 'General'}

This is called a "dictionary comprehension" - very Pythonic!

CONCEPT: defaultdict - Auto-Initializing Dictionaries
------------------------------------------------------
Regular dict throws error if key doesn't exist.
defaultdict automatically creates missing keys!

From collections import defaultdict:
    from collections import defaultdict

    # Regular dict - need to check before incrementing
    counts = {}
    for gate in ['A', 'B', 'A', 'C', 'A']:
        if gate in counts:
            counts[gate] += 1
        else:
            counts[gate] = 1
    # Result: {'A': 3, 'B': 1, 'C': 1}

    # defaultdict - cleaner!
    counts = defaultdict(int)  # int() returns 0
    for gate in ['A', 'B', 'A', 'C', 'A']:
        counts[gate] += 1      # Auto-creates key with value 0 first time
    # Result: defaultdict(<class 'int'>, {'A': 3, 'B': 1, 'C': 1})

Common default factories:
    defaultdict(int)      # Missing keys start at 0
    defaultdict(list)     # Missing keys start as []
    defaultdict(set)      # Missing keys start as set()
    defaultdict(dict)     # Missing keys start as {}

CHALLENGE: Track Multiple Breakdowns
-------------------------------------
Real APIs return rich data. You need to track:
- Total occupancy
- Occupancy by gate
- Occupancy by ticket type
- Entry/exit counts

Approach:
    from collections import defaultdict

    def track_details(events):
        # Build ticket lookup first!
        tickets = {t['ticket_id']: t for t in get_mock_tickets()}

        inside = set()                      # Who's currently inside
        by_gate = defaultdict(int)          # Count per gate
        by_type = defaultdict(int)          # Count per ticket type
        total_entries = 0
        total_exits = 0

        for event in events:
            ticket_id = event['ticket_id']
            gate = event['gate']
            ticket_type = tickets[ticket_id]['ticket_type']

            if event['scan_type'] == 'entry':
                inside.add(ticket_id)
                by_gate[gate] += 1
                by_type[ticket_type] += 1
                total_entries += 1
            else:
                inside.discard(ticket_id)
                by_gate[gate] -= 1
                by_type[ticket_type] -= 1
                total_exits += 1

        return {
            'total_occupancy': len(inside),
            'by_gate': dict(by_gate),       # Convert to regular dict
            'by_ticket_type': dict(by_type),
            'total_entries': total_entries,
            'total_exits': total_exits
        }

Key Insights:
- Pre-build lookups before processing stream (can't rewind!)
- Use defaultdict for counting
- Convert defaultdict to dict for cleaner output
- Track LAST gate used (increment on entry, decrement on exit)

Interview Tips:
- Explain why you pre-build the ticket lookup
- Mention you could cache this in Redis in production
- Discuss how this would map to a REST API response
"""


# ===========================================================================
# QUESTION 3: Real-time Occupancy Tracking with Metadata (MEDIUM-HARD)
# ===========================================================================
# Interview Tip: This shows you understand real-world API requirements
# ===========================================================================

def track_occupancy_with_details(stream) -> Dict:
    """
    Track detailed occupancy information including per-gate breakdown.

    This is more realistic for an API endpoint that needs to return rich data.

    Returns:
        {
            'total_occupancy': 5,
            'by_gate': {'A': 2, 'B': 2, 'C': 1},
            'by_ticket_type': {'VIP': 2, 'General': 3},
            'total_entries': 8,
            'total_exits': 3
        }

    Challenge: You need to track ticket types, but stream doesn't include them!
    Solution: Use get_mock_tickets() to build a lookup dictionary.

    Data structures to use:
    - defaultdict for counting
    - Regular dict for lookups
    """
    # Hint 1: Build a ticket_id -> ticket_type lookup dict first
    # Hint 2: Track which gate each ticket last used
    # Hint 3: Use defaultdict(int) for counting
    
    ticket_type_usage = {t['ticket_id']: t['ticket_type'] for t in get_mock_tickets()}
    
    total_occupancy = set()
    by_gate =  defaultdict(int)   
    by_ticket_type = defaultdict(int)
    total_entries = 0
    total_exits = 0

    for event in stream:
        ticket_id = event['ticket_id']
        gate = event['gate']
        scan_type = event['scan_type']

        if scan_type == 'entry' and ticket_id not in total_occupancy:
                total_occupancy.add(ticket_id)
                total_entries += 1
                by_gate[gate] +=1
                by_ticket_type[ticket_type_usage[ticket_id]] += 1

        elif scan_type == 'exit':
            total_occupancy.discard(ticket_id)
            total_exits +=1
            by_gate[gate] -=1
            by_ticket_type[ticket_type_usage[ticket_id]] -= 1


    return {
            'total_occupancy': len(total_occupancy),
            'by_gate': dict(by_gate),
            'by_ticket_type': dict(by_ticket_type),
            'total_entries': total_entries,
            'total_exits': total_exits
        }


"""
📚 DATABASE LEARNING - QUESTION 3
==================================

CONCEPT: Aggregation and GROUP BY
----------------------------------

Real APIs need to return aggregated statistics.

Basic GROUP BY:
---------------
-- Count tickets by type
SELECT ticket_type, COUNT(*) as count
FROM tickets
GROUP BY ticket_type;

-- Result:
--  ticket_type | count
-- -------------+-------
--  VIP         |     2
--  General     |     6

Multiple aggregations:
----------------------
SELECT
    ticket_type,
    COUNT(*) as ticket_count,
    SUM(price) as total_revenue,
    AVG(price) as avg_price
FROM tickets
GROUP BY ticket_type;

Joining and Grouping:
---------------------
-- Occupancy breakdown by ticket type
WITH current_occupancy AS (
    SELECT DISTINCT ON (s.ticket_id)
        s.ticket_id,
        s.scan_type,
        t.ticket_type
    FROM scans s
    JOIN tickets t ON s.ticket_id = t.ticket_id
    ORDER BY s.ticket_id, s.scan_time DESC
)
SELECT
    ticket_type,
    COUNT(*) as count
FROM current_occupancy
WHERE scan_type = 'entry'
GROUP BY ticket_type;

Occupancy by gate (last gate used):
-----------------------------------
WITH current_occupancy AS (
    SELECT DISTINCT ON (ticket_id)
        ticket_id,
        gate,
        scan_type
    FROM scans
    ORDER BY ticket_id, scan_time DESC
)
SELECT
    gate,
    COUNT(*) as occupancy
FROM current_occupancy
WHERE scan_type = 'entry'
GROUP BY gate
ORDER BY gate;

HAVING clause (filtering after GROUP BY):
------------------------------------------
-- Find gates with more than 2 people
SELECT
    gate,
    COUNT(*) as occupancy
FROM current_occupancy
WHERE scan_type = 'entry'
GROUP BY gate
HAVING COUNT(*) > 2;

Real-world API response:
------------------------
-- This is what your API might return as JSON
WITH current_occupancy AS (
    SELECT DISTINCT ON (s.ticket_id)
        s.ticket_id,
        s.gate,
        s.scan_type,
        t.ticket_type,
        u.name
    FROM scans s
    JOIN tickets t ON s.ticket_id = t.ticket_id
    JOIN users u ON t.user_id = u.user_id
    ORDER BY s.ticket_id, s.scan_time DESC
)
SELECT
    json_build_object(
        'total_occupancy', COUNT(*),
        'breakdown', json_agg(
            json_build_object(
                'ticket_id', ticket_id,
                'name', name,
                'gate', gate,
                'ticket_type', ticket_type
            )
        )
    ) as response
FROM current_occupancy
WHERE scan_type = 'entry';

Interview Tip: PostgreSQL has amazing JSON support!
This is perfect for REST APIs.
"""


def track_occupancy_with_details_db() -> Dict:
    """
    DATABASE CHALLENGE 3: Return detailed occupancy breakdown

    Use JOINs and GROUP BY to create a comprehensive report:
    - Total occupancy
    - Breakdown by gate
    - Breakdown by ticket type
    - Total entries/exits

    Bonus: Return as JSON directly from PostgreSQL!
    """
    conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
    cursor = conn.cursor()

    # TODO: Write multiple queries or one complex query

    conn.close()
    return {}


"""
🐍 PYTHON LEARNING - QUESTION 4: State Tracking and Time Calculations
======================================================================

CONCEPT: Tracking Multiple States Simultaneously
-------------------------------------------------
Complex problems need multiple data structures working together.

For anomaly detection, we need to track:
1. Who's currently inside (set)
2. Last exit time per ticket (dict)
3. Anomalies found (sets)

Example structure:
    inside = set()                    # Currently inside tickets
    last_exit = {}                    # ticket_id -> datetime of last exit
    anomalies = {
        'duplicate_entries': set(),
        'exit_without_entry': set(),
        'rapid_reentry': set()
    }

CONCEPT: Time Delta Calculations
---------------------------------
Check if events happened within a certain time period.

    from datetime import datetime, timedelta

    exit_time = datetime.fromisoformat('2025-09-30T10:00:00')
    entry_time = datetime.fromisoformat('2025-09-30T10:03:00')

    time_diff = entry_time - exit_time  # timedelta object
    time_diff.total_seconds()           # 180.0 seconds (3 minutes)

    # Check if less than 5 minutes
    if time_diff < timedelta(minutes=5):
        print("Rapid re-entry detected!")

CHALLENGE: Detect Three Types of Anomalies
-------------------------------------------
1. Duplicate entry: Ticket enters twice without exiting
2. Exit without entry: Ticket exits but was never inside
3. Rapid re-entry: Ticket exits then re-enters within 5 minutes

Approach:
    from datetime import datetime, timedelta

    def detect_anomalies(events):
        inside = set()
        last_exit_time = {}  # ticket_id -> datetime

        anomalies = {
            'duplicate_entries': set(),
            'exit_without_entry': set(),
            'rapid_reentry': set()
        }

        for event in events:
            ticket_id = event['ticket_id']
            scan_type = event['scan_type']
            timestamp = datetime.fromisoformat(event['timestamp'])

            if scan_type == 'entry':
                # Check for duplicate entry
                if ticket_id in inside:
                    anomalies['duplicate_entries'].add(ticket_id)
                else:
                    # Check for rapid re-entry
                    if ticket_id in last_exit_time:
                        time_since_exit = timestamp - last_exit_time[ticket_id]
                        if time_since_exit < timedelta(minutes=5):
                            anomalies['rapid_reentry'].add(ticket_id)

                    inside.add(ticket_id)

            else:  # exit
                # Check for exit without entry
                if ticket_id not in inside:
                    anomalies['exit_without_entry'].add(ticket_id)
                else:
                    inside.remove(ticket_id)
                    last_exit_time[ticket_id] = timestamp

        return anomalies

Logic Flow for Entry:
1. Is ticket already inside? → Duplicate entry!
2. If not, check if they exited recently (< 5 min) → Rapid re-entry!
3. Add to inside set

Logic Flow for Exit:
1. Is ticket NOT inside? → Exit without entry!
2. Otherwise, remove from inside and record exit time

Key Insights:
- Need to track state (inside) AND history (last_exit_time)
- Parse timestamps to datetime objects for comparison
- Use timedelta for time arithmetic
- Sets allow adding same ticket multiple times (if multiple anomalies)

Edge Cases to Consider:
- What if ticket has multiple anomalies? (Add to multiple sets)
- What if ticket exits twice? (Second exit is "exit without entry")
- What if data is out of chronological order? (Would need to sort first)

Interview Discussion:
- "How would you handle out-of-order events?" (Sort by timestamp first)
- "What other anomalies might you detect?" (Long stays, impossible travel)
- "How would you alert security in real-time?" (WebSockets, message queue)
"""


# ===========================================================================
# QUESTION 4: Detect Anomalies in Streaming Data (HARD)
# ===========================================================================
# Interview Tip: This tests your ability to handle edge cases
# ===========================================================================

def detect_scan_anomalies(stream) -> Dict[str, Set[str]]:
    """
    Detect suspicious patterns in real-time as events stream in.

    Detect:
    1. duplicate_entries: Ticket enters twice without exiting
    2. exit_without_entry: Ticket exits but never entered
    3. rapid_reentry: Ticket exits and re-enters within 5 minutes (suspicious!)

    Returns:
        {
            'duplicate_entries': {'T003'},
            'exit_without_entry': set(),
            'rapid_reentry': set()
        }

    Challenge: Need to track timing for rapid re-entry!
    Data structures:
    - Set for currently inside tickets
    - Dict mapping ticket_id -> last_exit_time for rapid detection
    - datetime parsing for time calculations
    """
    # Hint: Use datetime.fromisoformat() to parse timestamps
    # Hint: Store last exit time per ticket
    # Hint: Check if (entry_time - last_exit_time) < 5 minutes
    
    # 1)
    # current_occupancy set() and duplicate set()
    # Use If,elif,else
    # if scan_type is entry ticket_id is in current_occupancy then add to duplicate
    # elif scan_type is entry then add to current_occupancy() - sets wont allow duplication,
    # no need too specify ticket
    # else  ie scan_type is exit then we can discard the ticket_id from the current_occupancy list

    # 2)
    #  'exit_without_entry' set()
    #  elif - scan_type is 'exit' and ticket_id is not in current_occupancy
    #  add ticket_id to 'exit_without_entry'
    # this should go aftetr the first elif

    # 3
    # 'rapid_re_entry': set()
    # 're-entry_under_5_mins' dict()
    # I need to track if a ticket_id has exite and I need to track the exit times.
    # add dict to else 
    # I need to convert the time stamps from iso strings to datetime objects   
    # I need to map the converted strings and thier ticket_ids to hash for comparison later
    # I need to look up how to comrpare a datatime object to an arbitary amount of time - use timedelta
    
    # In the loop - add to the first elif (nested if?)- it's not fraduelent, and they should be let in, but we want to 
    # ...keep track of them
    # I need to check IF the incoming ticket_ids have previosly exited
    # if ticket_id is in the hash, get the exit time and find the difference between that and the reentry time
    #ill use dedefault dict- from collection import defaultdict 
    # If they have then I'll compare the exit time to the entry time - find the difference
    # if it's less than 5 mins, add to the rapid_reentry set


    current_occupancy = set()
    duplicates = set()
    exit_without_entry = set()
    re_entry_under_5_mins_tracker = dict()
    rapid_re_entry = set()

    for scan in stream:
        ticket_id = scan['ticket_id']
        scan_type = scan['scan_type']
        scan_time = datetime.fromisoformat(scan['timestamp'])


        if scan_type == 'entry' and ticket_id in current_occupancy:
            duplicates.add(ticket_id)

        elif scan_type == 'entry':
            current_occupancy.add(ticket_id)
            if ticket_id in re_entry_under_5_mins_tracker:
                if (scan_time - re_entry_under_5_mins_tracker[ticket_id]) <= timedelta(minutes= 5):
                    rapid_re_entry.add(ticket_id)

        elif scan_type == 'exit' and ticket_id not in current_occupancy:
            exit_without_entry.add(ticket_id)

        else:
            current_occupancy.discard(ticket_id)
            re_entry_under_5_mins_tracker[ticket_id] = scan_time


    return {
        'duplicate_entries': duplicates,
        'exit_without_entry': exit_without_entry,
        'rapid_re_entry': rapid_re_entry
    }



"""
📚 DATABASE LEARNING - QUESTION 4
==================================

CONCEPT: Window Functions and Advanced Analytics
-------------------------------------------------

Window functions let you perform calculations across rows related to the current row.

Basic window function:
----------------------
-- Add row numbers to scans
SELECT
    scan_id,
    ticket_id,
    scan_time,
    ROW_NUMBER() OVER (ORDER BY scan_time) as scan_number
FROM scans;

Partition by ticket:
--------------------
-- Number scans per ticket
SELECT
    ticket_id,
    scan_type,
    scan_time,
    ROW_NUMBER() OVER (PARTITION BY ticket_id ORDER BY scan_time) as scan_number
FROM scans
ORDER BY ticket_id, scan_time;

LAG and LEAD (look at previous/next row):
------------------------------------------
-- For each scan, show the previous scan type
SELECT
    ticket_id,
    scan_type,
    scan_time,
    LAG(scan_type) OVER (PARTITION BY ticket_id ORDER BY scan_time) as previous_scan
FROM scans;

Detecting duplicate entries:
----------------------------
WITH scan_with_previous AS (
    SELECT
        ticket_id,
        scan_type,
        scan_time,
        LAG(scan_type) OVER (PARTITION BY ticket_id ORDER BY scan_time) as prev_scan
    FROM scans
)
SELECT ticket_id, scan_time
FROM scan_with_previous
WHERE scan_type = 'entry' AND prev_scan = 'entry';
-- Result: T003 at 11:15 (entered twice!)

Exit without entry:
-------------------
WITH scan_with_previous AS (
    SELECT
        ticket_id,
        scan_type,
        scan_time,
        LAG(scan_type) OVER (PARTITION BY ticket_id ORDER BY scan_time) as prev_scan
    FROM scans
)
SELECT ticket_id, scan_time
FROM scan_with_previous
WHERE scan_type = 'exit' AND (prev_scan IS NULL OR prev_scan = 'exit');

Time-based anomalies (rapid re-entry):
---------------------------------------
WITH scan_with_timing AS (
    SELECT
        ticket_id,
        scan_type,
        scan_time,
        LAG(scan_time) OVER (PARTITION BY ticket_id ORDER BY scan_time) as prev_time,
        LAG(scan_type) OVER (PARTITION BY ticket_id ORDER BY scan_time) as prev_scan
    FROM scans
)
SELECT
    ticket_id,
    scan_time,
    prev_time,
    scan_time - prev_time as time_diff
FROM scan_with_timing
WHERE scan_type = 'entry'
  AND prev_scan = 'exit'
  AND scan_time - prev_time < INTERVAL '5 minutes';

Comprehensive anomaly report:
------------------------------
-- Create a view for security monitoring
CREATE OR REPLACE VIEW anomaly_report AS
WITH scan_with_context AS (
    SELECT
        s.ticket_id,
        s.scan_type,
        s.scan_time,
        t.ticket_type,
        u.name,
        u.email,
        LAG(s.scan_type) OVER (PARTITION BY s.ticket_id ORDER BY s.scan_time) as prev_scan,
        LAG(s.scan_time) OVER (PARTITION BY s.ticket_id ORDER BY s.scan_time) as prev_time
    FROM scans s
    JOIN tickets t ON s.ticket_id = t.ticket_id
    JOIN users u ON t.user_id = u.user_id
)
SELECT
    ticket_id,
    name,
    email,
    scan_time,
    CASE
        WHEN scan_type = 'entry' AND prev_scan = 'entry' THEN 'Duplicate Entry'
        WHEN scan_type = 'exit' AND (prev_scan IS NULL OR prev_scan = 'exit') THEN 'Exit Without Entry'
        WHEN scan_type = 'entry' AND prev_scan = 'exit' AND scan_time - prev_time < INTERVAL '5 minutes' THEN 'Rapid Re-entry'
        ELSE 'Normal'
    END as anomaly_type
FROM scan_with_context
WHERE scan_type = 'entry' AND prev_scan = 'entry'
   OR scan_type = 'exit' AND (prev_scan IS NULL OR prev_scan = 'exit')
   OR (scan_type = 'entry' AND prev_scan = 'exit' AND scan_time - prev_time < INTERVAL '5 minutes');

-- Now you can query it easily:
SELECT * FROM anomaly_report;

Interview Tip: Views are saved queries that act like tables!
Perfect for complex reports you run often.
"""


def detect_scan_anomalies_db() -> Dict[str, List[str]]:
    """
    DATABASE CHALLENGE 4: Detect anomalies using window functions

    Use LAG() to compare each scan with the previous scan.

    Return:
    {
        'duplicate_entries': ['T003'],
        'exit_without_entry': [],
        'rapid_reentry': []
    }

    Bonus: Create a VIEW for the security team to monitor!
    """
    conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
    cursor = conn.cursor()

    # TODO: Implement using window functions

    conn.close()
    return {}


"""
🐍 PYTHON LEARNING - QUESTION 5: Complex State Management
==========================================================

CONCEPT: Managing Multiple Constraints
---------------------------------------
Production systems have business rules and limits.
This question combines EVERYTHING you've learned!

You need to:
1. Track who's inside (set)
2. Enforce capacity limits (conditional logic)
3. Allow VIP exceptions (lookup ticket types)
4. Track rejected entries (list)
5. Calculate theoretical occupancy (parallel tracking)
6. Count capacity events (counter)

This is the FULL picture of a real event management system!

CONCEPT: Conditional Business Logic
------------------------------------
Not all entries are equal - VIPs bypass capacity!

    if current_occupancy >= max_capacity:
        if ticket_type == 'VIP':
            # Allow VIP to enter anyway
            vip_override_count += 1
        else:
            # Reject general ticket
            rejected_entries.append(ticket_id)
            continue  # Don't add to inside set!

CHALLENGE: Implement Capacity Management
-----------------------------------------
Real venues have fire safety limits!

Requirements:
- Track actual occupancy (with capacity limits enforced)
- Track "would-be" occupancy (what if no limits?)
- Reject general tickets when at capacity
- Always allow VIPs (override capacity)
- Count how many times we hit capacity
- Track rejected ticket IDs

Data Structures Needed:
    tickets_lookup = {t['ticket_id']: t for t in get_mock_tickets()}
    inside_actual = set()           # Who's actually inside
    inside_theoretical = set()      # Who would be inside (no limits)
    rejected = []                   # Rejected ticket IDs
    vip_overrides = 0              # VIPs who entered at capacity
    times_at_capacity = 0          # How many times we hit limit

Approach:
    from collections import defaultdict

    def manage_capacity(events, max_cap=6):
        # Pre-build ticket lookup
        tickets = {t['ticket_id']: t for t in get_mock_tickets()}

        inside_actual = set()
        inside_theoretical = set()
        rejected = []
        vip_overrides = 0
        times_at_capacity = 0
        total_entries = 0
        total_exits = 0

        for event in events:
            ticket_id = event['ticket_id']
            scan_type = event['scan_type']
            ticket_type = tickets[ticket_id]['ticket_type']

            # Track theoretical occupancy (always)
            if scan_type == 'entry':
                inside_theoretical.add(ticket_id)
                total_entries += 1
            else:
                inside_theoretical.discard(ticket_id)
                total_exits += 1

            # Track actual occupancy (with capacity check)
            if scan_type == 'entry':
                current_count = len(inside_actual)

                # Check if at capacity
                if current_count >= max_cap:
                    times_at_capacity += 1

                    if ticket_type == 'VIP':
                        # VIP override
                        inside_actual.add(ticket_id)
                        vip_overrides += 1
                    else:
                        # Reject entry
                        rejected.append(ticket_id)
                        # Don't add to inside_actual!
                else:
                    # Under capacity, allow entry
                    inside_actual.add(ticket_id)

            else:  # exit
                inside_actual.discard(ticket_id)

        return {
            'final_occupancy': len(inside_actual),
            'times_at_capacity': times_at_capacity,
            'rejected_entries': rejected,
            'would_be_occupancy': len(inside_theoretical),
            'vip_override_count': vip_overrides
        }

Key Logic Points:
1. Check capacity BEFORE allowing entry
2. VIP check happens AFTER capacity check
3. Track theoretical separately (always add/remove)
4. Only rejected tickets don't get added to inside_actual
5. Exits always work (no capacity check needed)

Tricky Parts:
- Need to track TWO occupancy states simultaneously
- Capacity check uses current count, not theoretical
- VIPs entering at capacity still counts as "at capacity"
- Rejected tickets still count toward theoretical

Interview Discussion Points:
- "How would you handle capacity per area/zone?" (Multiple counters)
- "What if we have different capacity for different ticket types?"
- "How would you notify security when capacity reached?"
- "Should exits be allowed when at capacity?" (Yes - fire safety!)
- "What about group tickets (one ticket, 4 people)?" (Track people count)

Real-World Considerations:
- Database would store rejected scans for analytics
- Redis would cache current occupancy count
- WebSocket would push updates to dashboard
- API endpoint: POST /api/scans would check capacity before inserting
- Message queue (Celery) would trigger alerts at 90% capacity

This is production-level thinking!
"""


# ===========================================================================
# QUESTION 5: Real-time Capacity Management (VERY HARD)
# ===========================================================================
# Interview Tip: This simulates a production system with constraints
# ===========================================================================

def manage_capacity_realtime(stream, max_capacity: int = 6,
                              vip_gate: str = 'A') -> Dict:
    """
    Real-world scenario: Venue has capacity limits!

    Requirements:
    1. Track when venue hits capacity
    2. VIP ticket holders can always enter (even at capacity)
    3. General tickets blocked when at capacity
    4. Track rejected entry attempts
    5. Calculate "would-be occupancy" if no limits existed

    Args:
        stream: Scan events
        max_capacity: Maximum allowed occupancy for general tickets
        vip_gate: Gate reserved for VIPs

    Returns:
        {
            'final_occupancy': 5,
            'times_at_capacity': 2,  # How many times we hit the limit
            'rejected_entries': ['T007'],  # Tickets rejected due to capacity
            'would_be_occupancy': 6,  # What occupancy would be without limits
            'vip_override_count': 1  # Times VIPs entered at capacity
        }

    Advanced concepts:
    - Need ticket type lookup (VIP vs General)
    - Track multiple states simultaneously
    - Handle conditional logic based on ticket type

    """
    
    # 1 get final occupancy - int
    #  max occupancy is 6
    #  current_occupents = set() - handles dupes - use len for current_occupents
    #  either standard or vip can enter up to max occupancy
    #  when max occupancy is reached only vips can enter

    # need to create a lookup to see which ticket ID: tickt_type
    # use a dictionary comprehension
    # tickt_id_ticket_type

    # use a for loop
    # if scan_type == "entry"
    # nested ?
    # if len(current_occupents) < 6
    # current_occupents.add(ticket_id)
    # if len(current_occupents) > 6 and ticket_type == VIP
    # current_occupents.add(ticket_id)
    # else:
    # current_occupents.discard(ticket_id)

    # return len(current_occupents)

    #2 times at capacity
    # make a counter to track every time  len(current_occupents) > 6
    # make a boolen to control addition to the counter
    # over_max = "False" 
    
    # if len(current_occupents) >= max and not over_max:
    # counter +=1 
    # over_max = True
    # if len(current_occupents) <= max:
    # over_max = False


    current_occupents = set()
    ticket_id_ticket_type = {t['ticket_id']: t['ticket_type'] for t in get_mock_tickets()}
    over_max = False
    times_at_capacity = 0

    for scan in stream:
        scan_type = scan['scan_type']
        ticket_id = scan['ticket_id']
        ticket_type = ticket_id_ticket_type[ticket_id]


        if scan_type == 'entry':
            if len(current_occupents) < max_capacity:
                current_occupents.add(ticket_id)
            elif ticket_type == 'VIP' and len(current_occupents) > max_capacity:
                current_occupents.add(ticket_id)
                
            if len(current_occupents) >= max_capacity and not over_max:
                times_at_capacity +=1
                over_max = True
            elif len(current_occupents) <= max_capacity:
                    over_max = False
        else:
            current_occupents.discard(ticket_id)

    return {'final_occupancy': len(current_occupents), 'times_at_capacity': times_at_capacity}


"""
📚 DATABASE LEARNING - QUESTION 5
==================================

CONCEPT: Transactions, Constraints, and Real-time Systems
----------------------------------------------------------

In a real event system, you need to enforce business rules at the database level.

Database Constraints:
---------------------
-- Ensure ticket types are valid
ALTER TABLE tickets
ADD CONSTRAINT valid_ticket_type
CHECK (ticket_type IN ('VIP', 'General', 'Staff', 'Press'));

-- Prevent negative prices
ALTER TABLE tickets
ADD CONSTRAINT positive_price
CHECK (price >= 0);

-- Ensure scan types are valid (we already did this!)
ALTER TABLE scans
ADD CONSTRAINT valid_scan_type
CHECK (scan_type IN ('entry', 'exit'));

Capacity Management with Triggers:
-----------------------------------
This is advanced but VERY relevant for event systems!

-- Function to check capacity before insert
CREATE OR REPLACE FUNCTION check_venue_capacity()
RETURNS TRIGGER AS $$
DECLARE
    current_count INTEGER;
    max_cap INTEGER := 100;  -- Set your max capacity
    ticket_type_val VARCHAR(20);
BEGIN
    -- Only check for entry scans
    IF NEW.scan_type = 'entry' THEN
        -- Get current occupancy
        SELECT COUNT(*) INTO current_count
        FROM (
            SELECT DISTINCT ON (ticket_id) ticket_id, scan_type
            FROM scans
            WHERE scan_time <= NEW.scan_time
            ORDER BY ticket_id, scan_time DESC
        ) AS latest
        WHERE scan_type = 'entry';

        -- Get ticket type
        SELECT t.ticket_type INTO ticket_type_val
        FROM tickets t
        WHERE t.ticket_id = NEW.ticket_id;

        -- Check capacity (VIPs bypass)
        IF current_count >= max_cap AND ticket_type_val != 'VIP' THEN
            RAISE EXCEPTION 'Venue at capacity. Entry denied for ticket %', NEW.ticket_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger
CREATE TRIGGER enforce_capacity
BEFORE INSERT ON scans
FOR EACH ROW
EXECUTE FUNCTION check_venue_capacity();

-- Now try to insert a scan when at capacity:
INSERT INTO scans (ticket_id, gate, scan_type, scan_time)
VALUES ('T999', 'A', 'entry', NOW());
-- Will fail if at capacity!

Transactions (ACID properties):
-------------------------------
Real systems need atomic operations.

-- Example: Someone buys a ticket and immediately scans in
BEGIN;

-- Insert the ticket
INSERT INTO tickets (ticket_id, user_id, ticket_type, price)
VALUES ('T100', 'U123', 'VIP', 150.00);

-- Record the entry scan
INSERT INTO scans (ticket_id, gate, scan_type, scan_time)
VALUES ('T100', 'A', 'entry', NOW());

-- If either fails, both are rolled back
COMMIT;

-- Rollback example:
BEGIN;
INSERT INTO tickets (ticket_id, user_id, ticket_type, price)
VALUES ('T101', 'INVALID_USER', 'VIP', 150.00);
-- This fails due to foreign key constraint
ROLLBACK;  -- Undo everything in this transaction

Occupancy tracking query with capacity info:
---------------------------------------------
WITH current_occupancy AS (
    SELECT DISTINCT ON (s.ticket_id)
        s.ticket_id,
        s.scan_type,
        t.ticket_type
    FROM scans s
    JOIN tickets t ON s.ticket_id = t.ticket_id
    ORDER BY s.ticket_id, s.scan_time DESC
)
SELECT
    COUNT(*) as total_occupancy,
    COUNT(*) FILTER (WHERE ticket_type = 'VIP') as vip_count,
    COUNT(*) FILTER (WHERE ticket_type = 'General') as general_count,
    100 as max_capacity,
    100 - COUNT(*) as available_spots
FROM current_occupancy
WHERE scan_type = 'entry';

Real-time monitoring query:
---------------------------
-- This could power a live dashboard
SELECT
    DATE_TRUNC('minute', scan_time) as minute,
    COUNT(*) FILTER (WHERE scan_type = 'entry') as entries,
    COUNT(*) FILTER (WHERE scan_type = 'exit') as exits,
    SUM(COUNT(*) FILTER (WHERE scan_type = 'entry')) OVER (ORDER BY DATE_TRUNC('minute', scan_time)) -
    SUM(COUNT(*) FILTER (WHERE scan_type = 'exit')) OVER (ORDER BY DATE_TRUNC('minute', scan_time)) as running_occupancy
FROM scans
GROUP BY minute
ORDER BY minute;

Interview Tip: CrowdComms likely has real-time dashboards!
Understanding how to structure queries for live updates is valuable.

Redis for Caching (mentioned in job description):
--------------------------------------------------
In Python, you'd combine PostgreSQL with Redis:

import redis
r = redis.Redis()

# Cache current occupancy (expires in 10 seconds)
occupancy = count_current_occupancy_db()
r.setex('current_occupancy', 10, occupancy)

# Read from cache
cached = r.get('current_occupancy')
if cached:
    return int(cached)
else:
    # Cache miss, query database
    return count_current_occupancy_db()

This reduces database load for frequently-accessed data!
"""


def manage_capacity_realtime_db(max_capacity: int = 6) -> Dict:
    """
    DATABASE CHALLENGE 5: Implement capacity management

    Create:
    1. A function to check current occupancy vs capacity
    2. A trigger that prevents entries when at capacity (except VIPs)
    3. A query to show rejected scans (you'd need a rejected_scans table)
    4. A view for real-time dashboard

    This is production-level complexity!
    """
    conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
    cursor = conn.cursor()

    # TODO: Implement capacity management system

    conn.close()
    return {}


# ===========================================================================
# BONUS: Performance Optimization
# ===========================================================================

def count_occupancy_optimized_for_large_stream(stream) -> int:
    """
    INTERVIEW DISCUSSION POINT: What if stream has millions of events?

    Considerations:
    1. Memory usage - can't store everything in memory
    2. Processing speed - need efficient data structures
    3. Database load - need caching strategy

    Optimization techniques:
    - Use deque for fixed-size buffers
    - Use Counter for efficient counting
    - Batch database operations
    - Use Redis for caching
    - Use database indexes properly

    This is a great discussion topic for the interview!
    """
    # For very large streams, you might process in batches
    from collections import deque

    # Keep only last N events in memory
    recent_events = deque(maxlen=1000)
    current_inside = set()

    for event in stream:
        recent_events.append(event)
        ticket_id = event['ticket_id']

        if event['scan_type'] == 'entry':
            current_inside.add(ticket_id)
        else:
            current_inside.discard(ticket_id)

    return len(current_inside)


"""
📚 INTERVIEW PREPARATION CHECKLIST
===================================

Topics to be comfortable discussing:

1. Python Data Structures:
   ✓ sets (fast membership testing)
   ✓ defaultdict (auto-initialization)
   ✓ Counter (counting occurrences)
   ✓ deque (efficient queues)
   ✓ heapq (priority queues)

2. SQL Fundamentals:
   ✓ SELECT, INSERT, UPDATE, DELETE
   ✓ WHERE clauses and filtering
   ✓ JOINs (INNER, LEFT, RIGHT)
   ✓ GROUP BY and aggregations
   ✓ ORDER BY and DISTINCT

3. Advanced SQL:
   ✓ Window functions (ROW_NUMBER, LAG, LEAD)
   ✓ CTEs (Common Table Expressions) with WITH
   ✓ Subqueries
   ✓ DISTINCT ON (PostgreSQL-specific)
   ✓ Indexes and performance

4. Database Design:
   ✓ Foreign keys and relationships
   ✓ Constraints (CHECK, UNIQUE, NOT NULL)
   ✓ One-to-many relationships
   ✓ Normalization basics

5. Real-world Concepts:
   ✓ Streaming data processing
   ✓ Timestamp handling
   ✓ Anomaly detection
   ✓ Capacity management
   ✓ Caching strategies (Redis)

6. API Design (for discussion):
   ✓ REST endpoints for occupancy data
   ✓ Real-time updates (WebSockets)
   ✓ Rate limiting
   ✓ Error handling

Example API Endpoints you might discuss:
-----------------------------------------
GET  /api/occupancy/current
GET  /api/occupancy/at/{timestamp}
GET  /api/occupancy/by-gate
GET  /api/tickets/{ticket_id}/scans
POST /api/scans (record new scan)
GET  /api/anomalies
GET  /api/users/{user_id}/tickets

Questions to Ask Them:
----------------------
1. "How do you handle real-time updates to clients?" (WebSockets?)
2. "What's your caching strategy for high-traffic events?" (Redis?)
3. "How do you handle time zones for international events?"
4. "Do you batch database writes or write immediately?"
5. "How do you monitor for anomalies in production?"

Good luck with your interview! 🚀
"""


# ===========================================================================
# TEST RUNNER
# ===========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ADVANCED EVENT OCCUPANCY SYSTEM - CROWDCOMMS INTERVIEW PREP")
    print("=" * 70)

    # Uncomment to set up database:
    setup_database()
    populate_database()

    print("\n📊 Testing Python functions with mock stream...\n")

    # Test basic occupancy
    result1 = count_current_occupancy(mock_scan_stream())
    print(f"Q1 - Current occupancy: {result1}")
    print(f"     Expected: 4 tickets inside")
    print(f"     Expected: 4 tickets inside")


    # Test time-based occupancy
    result2 = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T11:30:00')
    print(f"\nQ2 - Occupancy at 11:30am: {result2}")
    print(f"     Expected: 6 tickets inside")

    # Test detailed tracking
    result3 = track_occupancy_with_details(mock_scan_stream())
    print(f"\nQ3 - Detailed tracking: {result3}")

    # Test anomaly detection
    result4 = detect_scan_anomalies(mock_scan_stream())
    print(f"\nQ4 - Anomalies detected: {result4}")
    print(f"     Expected: T003 has duplicate entry")

    # Test capacity management
    result5 = manage_capacity_realtime(mock_scan_stream(), max_capacity=6)
    print(f"\nQ5 - Capacity management: {result5}")

    # ===========================================================================
    # DATABASE QUERY TESTS - Test your SQL solutions!
    # ===========================================================================

    print("\n" + "=" * 70)
    print("DATABASE QUERY TESTS - Testing your SQL solutions")
    print("=" * 70)

    # TEST DB QUESTION 1: Current occupancy using SQL
    print("\n🗄️  DATABASE Q1 - Current Occupancy")
    print("-" * 50)
    try:
        db_result1 = count_current_occupancy_db()
        py_result1 = count_current_occupancy(mock_scan_stream())
        print(f"Your SQL query result: {db_result1}")
        print(f"Python result (correct): {py_result1}")
        if db_result1 == py_result1:
            print("✅ CORRECT! Your query works!")
        else:
            print(f"❌ INCORRECT - Expected {py_result1}, got {db_result1}")
    except Exception as e:
        print(f"❌ ERROR in your query: {e}")

    # TEST DB QUESTION 2: Occupancy at specific time
    print("\n🗄️  DATABASE Q2 - Occupancy at 11:30am")
    print("-" * 50)
    try:
        db_result2 = get_occupancy_at_time_db('2025-09-30 11:30:00')
        py_result2 = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T11:30:00')
        print(f"Your SQL query result: {db_result2}")
        print(f"Python result (correct): {py_result2}")
        if db_result2 == py_result2:
            print("✅ CORRECT! Your query works!")
        else:
            print(f"❌ INCORRECT - Expected {py_result2}, got {db_result2}")
    except Exception as e:
        print(f"❌ ERROR in your query: {e}")

    # TEST DB QUESTION 3: Detailed occupancy breakdown
    print("\n🗄️  DATABASE Q3 - Detailed Occupancy Breakdown")
    print("-" * 50)
    try:
        db_result3 = track_occupancy_with_details_db()
        py_result3 = track_occupancy_with_details(mock_scan_stream())
        print(f"Your SQL query result: {db_result3}")
        print(f"Python result (correct): {py_result3}")
        if db_result3:
            print("✅ Query executed! Check if data looks reasonable")
            print("   Expected keys: total_occupancy, by_gate, by_ticket_type")
        else:
            print("❌ Query returned empty result")
    except Exception as e:
        print(f"❌ ERROR in your query: {e}")

    # TEST DB QUESTION 4: Anomaly detection
    print("\n🗄️  DATABASE Q4 - Anomaly Detection")
    print("-" * 50)
    try:
        db_result4 = detect_scan_anomalies_db()
        py_result4 = detect_scan_anomalies(mock_scan_stream())
        print(f"Your SQL query result: {db_result4}")
        print(f"Python result (correct): {py_result4}")
        if 'duplicate_entries' in db_result4 and 'T003' in str(db_result4['duplicate_entries']):
            print("✅ CORRECT! Found T003 duplicate entry!")
        else:
            print("❌ INCORRECT - Should find T003 as duplicate entry")
    except Exception as e:
        print(f"❌ ERROR in your query: {e}")

    # TEST DB QUESTION 5: Capacity management
    print("\n🗄️  DATABASE Q5 - Capacity Management")
    print("-" * 50)
    try:
        db_result5 = manage_capacity_realtime_db(max_capacity=6)
        py_result5 = manage_capacity_realtime(mock_scan_stream(), max_capacity=6)
        print(f"Your SQL query result: {db_result5}")
        print(f"Python result (correct): {py_result5}")
        if db_result5:
            print("✅ Query executed! Check if logic matches Python result")
        else:
            print("❌ Query returned empty result")
    except Exception as e:
        print(f"❌ ERROR in your query: {e}")

    print("\n" + "=" * 70)
    print("DONE! All tests complete.")
    print("Alternatively, run: pytest test_occupancy_advanced.py")
    print("=" * 70)




# JOINS: Combining Data from Multiple Tables
# -------------------------------------------
# JOINs are ESSENTIAL for APIs that return rich data from normalized databases.

# 1. INNER JOIN - Only matched rows (most common)
# ------------------------------------------------
# -- Get tickets WITH their user info (excludes orphaned tickets)
# SELECT t.ticket_id, t.ticket_type, u.name, u.email
# FROM tickets t
# INNER JOIN users u ON t.user_id = u.user_id;

# Result: Only tickets that have a valid user.

# When to use: "I need data from both tables, skip rows without matches"
# API use case: GET /api/tickets - show ticket details with user names

# 2. LEFT JOIN - All from left table + optional right
# ----------------------------------------------------
# -- Get ALL tickets, include user info IF it exists
# SELECT t.ticket_id, t.ticket_type, u.name, u.email
# FROM tickets t
# LEFT JOIN users u ON t.user_id = u.user_id;

# Result: ALL tickets. If user deleted, name/email will be NULL.

# When to use: "I want all of A, include B if available"
# API use case: GET /api/tickets - show all tickets even if user was deleted

# 3. RIGHT JOIN - All from right table + optional left
# -----------------------------------------------------
# -- Get ALL users, show tickets IF they bought any
# SELECT u.user_id, u.name, t.ticket_id, t.ticket_type
# FROM tickets t
# RIGHT JOIN users u ON t.user_id = u.user_id;

# Result: ALL users. If user bought no tickets, ticket columns are NULL.

# When to use: "I want all of B, include A if available"
# API use case: GET /api/users - show all users even if no purchases

# Note: RIGHT JOIN is rare - usually rewrite as LEFT JOIN for clarity.

# 4. Multi-table JOINs - Chain multiple tables
# ---------------------------------------------
# -- Get scans with ticket info AND user info (3 tables!)
# SELECT
#     s.scan_id,
#     s.scan_time,
#     s.scan_type,
#     t.ticket_id,
#     t.ticket_type,
#     u.name,
#     u.email
# FROM scans s
# INNER JOIN tickets t ON s.ticket_id = t.ticket_id
# INNER JOIN users u ON t.user_id = u.user_id;

# API use case: GET /api/scans - return complete scan history with context

# 5. Mixing INNER and LEFT JOINs
# -------------------------------
# -- Get all scans with ticket info, but user info is optional
# SELECT
#     s.scan_id,
#     s.scan_time,
#     t.ticket_id,
#     u.name  -- This might be NULL if user deleted
# FROM scans s
# INNER JOIN tickets t ON s.ticket_id = t.ticket_id
# LEFT JOIN users u ON t.user_id = u.user_id;

# When to use: Required vs optional relationships

# 6. JOINs with Aggregation
# --------------------------
# -- Count tickets per user
# SELECT
#     u.user_id,
#     u.name,
#     COUNT(t.ticket_id) as ticket_count
# FROM users u
# LEFT JOIN tickets t ON u.user_id = t.user_id
# GROUP BY u.user_id, u.name;

# Result:
# U123 - Alice - 2
# U456 - Bob - 1
# U789 - Charlie - 0  ← LEFT JOIN includes users with 0 tickets!

# If we used INNER JOIN, Charlie would be excluded!

# 7. Self-JOIN - Compare rows in same table
# ------------------------------------------
# -- Find tickets purchased by the same user
# SELECT
#     t1.ticket_id as ticket1,
#     t2.ticket_id as ticket2,
#     t1.user_id
# FROM tickets t1
# INNER JOIN tickets t2 ON t1.user_id = t2.user_id
#                       AND t1.ticket_id < t2.ticket_id;

# Result: Pairs of tickets owned by same person
# (t1.ticket_id < t2.ticket_id prevents duplicates)

# QUIZ EXERCISES - Try these queries yourself!
# ---------------------------------------------

# Exercise 1: Find all users who have NEVER bought a ticket
# Hint: Use LEFT JOIN and check for NULL

# Exercise 2: Count total scans per user (not per ticket!)
# Hint: Join scans → tickets → users, then GROUP BY user

# Exercise 3: Find VIP ticket holders who have scanned in today
# Hint: Join tickets → users, filter ticket_type = 'VIP' and scan_type = 'entry'

# Exercise 4: List users with their total spending
# Hint: LEFT JOIN users → tickets, SUM(price)

# Exercise 5: Find tickets that have NEVER been scanned
# Hint: LEFT JOIN tickets → scans, WHERE scan_id IS NULL

# SOLUTIONS (try before looking!)
# --------------------------------

# -- Exercise 1: Users who never bought tickets
# SELECT u.user_id, u.name
# FROM users u
# LEFT JOIN tickets t ON u.user_id = t.user_id
# WHERE t.ticket_id IS NULL;

# -- Exercise 2: Total scans per user
# SELECT
#     u.user_id,
#     u.name,
#     COUNT(s.scan_id) as total_scans
# FROM users u
# LEFT JOIN tickets t ON u.user_id = t.user_id
# LEFT JOIN scans s ON t.ticket_id = s.ticket_id
# GROUP BY u.user_id, u.name;

# -- Exercise 3: VIP holders who scanned in
# SELECT DISTINCT
#     u.user_id,
#     u.name,
#     t.ticket_id
# FROM users u
# INNER JOIN tickets t ON u.user_id = t.user_id
# INNER JOIN scans s ON t.ticket_id = s.ticket_id
# WHERE t.ticket_type = 'VIP'
#   AND s.scan_type = 'entry';

# -- Exercise 4: Total spending per user
# SELECT
#     u.user_id,
#     u.name,
#     COALESCE(SUM(t.price), 0) as total_spent
# FROM users u
# LEFT JOIN tickets t ON u.user_id = t.user_id
# GROUP BY u.user_id, u.name;

# -- Exercise 5: Tickets never scanned
# SELECT t.ticket_id, t.ticket_type, u.name
# FROM tickets t
# INNER JOIN users u ON t.user_id = u.user_id
# LEFT JOIN scans s ON t.ticket_id = s.ticket_id
# WHERE s.scan_id IS NULL;

# JOIN Performance Tips:
# ----------------------
# - ALWAYS index foreign key columns (we did this!)
#   CREATE INDEX idx_tickets_user ON tickets(user_id)

# - INNER JOIN is faster than LEFT JOIN (fewer rows)

# - Put smaller table first when possible

# - Use EXPLAIN ANALYZE to check if indexes are used

# Interview Discussion Points:
# -----------------------------
# Q: "When would you use LEFT JOIN vs INNER JOIN in an API?"
# A: LEFT JOIN when optional data (user preferences), INNER JOIN when required (tickets must have users)

# Q: "How do JOINs affect API performance?"
# A: Without indexes, JOINs can be slow. Always index foreign keys. Consider caching frequently-joined data in Redis.

# Q: "What's N+1 query problem?"
# A: Fetching users in a loop, then tickets for each user separately.
#    BAD: SELECT * FROM users; then loop: SELECT * FROM tickets WHERE user_id = ?
#    GOOD: Single query with JOIN!
