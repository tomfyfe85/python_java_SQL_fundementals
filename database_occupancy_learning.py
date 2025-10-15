# Database-Focused Event Occupancy Learning
# ===========================================
# SQL, PostgreSQL, and database concepts for CrowdComms interview prep
# Focus: SQL vs Python, JOINs, transactions, database design

import psycopg2
import json
from typing import Dict, List
from datetime import datetime


# ===========================================================================
# MOCK DATA - 3-Table Schema (Users, Tickets, Scans)
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
    Generator yielding scan events as JSON strings (realistic API format).

    Key scenarios in this data:
    - T003 enters twice without exiting (duplicate entry - anomaly!)
    - T008 belongs to same user as T001 (U123 has 2 tickets)
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
        '{"ticket_id": "T008", "gate": "A", "timestamp": "2025-09-30T11:25:00", "scan_type": "entry"}',  # U123's 2nd
        '{"ticket_id": "T003", "gate": "B", "timestamp": "2025-09-30T12:00:00", "scan_type": "exit"}',
        '{"ticket_id": "T004", "gate": "C", "timestamp": "2025-09-30T12:05:00", "scan_type": "exit"}',
    ]
    for event_json in events:
        yield event_json


# ===========================================================================
# DATABASE SETUP
# ===========================================================================

def setup_database():
    """
    Create the 3-table schema for event occupancy tracking.
    Run this ONCE to set up your database.

    Creates:
    - users table (who bought tickets)
    - tickets table (what tickets exist)
    - scans table (entry/exit events)
    """
    conn = psycopg2.connect("dbname=occupancy_db_learning2 user=tomfyfe")
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
    conn = psycopg2.connect("dbname=occupancy_db_learning2 user=tomfyfe")
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
    for event_json in mock_scan_stream():
        scan = json.loads(event_json)
        cursor.execute("""
            INSERT INTO scans (ticket_id, gate, scan_type, scan_time)
            VALUES (%s, %s, %s, %s)
        """, (scan['ticket_id'], scan['gate'], scan['scan_type'], scan['timestamp']))

    conn.commit()
    conn.close()
    print("✅ Database populated with mock data!")


# ===========================================================================
# QUESTION 1: CURRENT OCCUPANCY - Python vs SQL
# ===========================================================================

"""
📚 DATABASE LEARNING - QUESTION 1: Current Occupancy
=====================================================

CONCEPT: Database Schema Design with Foreign Keys
--------------------------------------------------

We have THREE related tables instead of one big table:

1. users: Who bought tickets
2. tickets: What tickets exist (each has ONE owner)
3. scans: Entry/exit events (each references ONE ticket)

Why is this better than one table?
- Avoids data duplication (user email stored once, not per scan)
- Enforces relationships (can't scan a ticket that doesn't exist)
- Makes updates easier (change user email in one place)

FOREIGN KEYS: The Key Concept
------------------------------
A foreign key creates a relationship between tables.

In tickets table:
    user_id VARCHAR(10) REFERENCES users(user_id)

This means:
- Every ticket MUST belong to a user that exists
- You CAN'T insert a ticket with user_id='U999' if U999 doesn't exist
- If you DELETE a user, CASCADE deletes their tickets too

Basic Occupancy Query:
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

WHEN TO USE SQL VS PYTHON:
---------------------------
✅ Use SQL when:
- Data is already in database
- Need to filter large datasets before processing
- Aggregating (COUNT, SUM, GROUP BY)
- Joining multiple tables

✅ Use Python when:
- Complex business logic
- Need to call APIs or external services
- Processing real-time streams
- Need Python libraries (ML, date parsing)

For this question:
- SQL is faster if data is in database (no need to load into Python)
- Python is better for real-time streaming (process as events arrive)
"""


def count_current_occupancy_sql() -> int:
    """
    SQL SOLUTION: Find current occupancy using database query.

    Approach:
    1. For each ticket, find the LAST scan event
    2. Count tickets where last scan was 'entry'

    Returns:
        int: Number of tickets currently inside

    Expected: 4 tickets inside
    """
    conn = psycopg2.connect("dbname=occupancy_db_learning2 user=tomfyfe")
    cursor = conn.cursor()

    query = """
    WITH last_scans AS (
        SELECT DISTINCT ON(ticket_id)
            ticket_id,
            scan_type
        FROM scans
        ORDER BY ticket_id, scan_time DESC
    )
    SELECT COUNT(*)
    FROM last_scans
    WHERE scan_type = 'entry';
    """

    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


def count_current_occupancy_python(stream) -> int:
    """
    PYTHON SOLUTION: Process streaming events in real-time.

    Approach:
    - Maintain a set of tickets currently inside
    - Add on entry, remove on exit
    - Return final count

    Returns:
        int: Number of tickets currently inside
    """
    inside = set()

    for event_json in stream:
        event = json.loads(event_json)
        ticket_id = event['ticket_id']
        scan_type = event['scan_type']

        if scan_type == 'entry':
            inside.add(ticket_id)
        else:
            inside.discard(ticket_id)

    return len(inside)


# ===========================================================================
# QUESTION 2: OCCUPANCY AT SPECIFIC TIME - Timestamp Filtering
# ===========================================================================

"""
📚 DATABASE LEARNING - QUESTION 2: Time-Based Queries
======================================================

CONCEPT: Filtering with Timestamps
-----------------------------------

PostgreSQL has excellent timestamp support.

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

Check if index is being used:
    EXPLAIN ANALYZE
    SELECT DISTINCT ON (ticket_id) ticket_id, scan_type
    FROM scans
    ORDER BY ticket_id, scan_time DESC;

Look for "Index Scan" in the output!
"""


def get_occupancy_at_time_sql(target_time: str) -> int:
    """
    SQL SOLUTION: Find occupancy at specific time with timestamp filtering.

    Args:
        target_time: Timestamp string (e.g., '2025-09-30 11:30:00')

    Returns:
        int: Number of tickets inside at that moment

    Expected: At '2025-09-30 11:30:00' -> 6 tickets inside
    """
    conn = psycopg2.connect("dbname=occupancy_db_learning2 user=tomfyfe")
    cursor = conn.cursor()

    query = """
    WITH last_scans_before AS (
        SELECT DISTINCT ON (ticket_id)
            ticket_id,
            scan_type
        FROM scans
        WHERE scan_time <= %s
        ORDER BY ticket_id, scan_time DESC
    )
    SELECT COUNT(*) as occupancy
    FROM last_scans_before
    WHERE scan_type = 'entry';
    """

    cursor.execute(query, (target_time,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


def get_occupancy_at_time_python(stream, target_time: str) -> int:
    """
    PYTHON SOLUTION: Process stream up to target time.

    Args:
        stream: Generator of scan events
        target_time: ISO timestamp string

    Returns:
        int: Number of tickets inside at that moment
    """
    inside = set()
    target_dt = datetime.fromisoformat(target_time)

    for event_json in stream:
        event = json.loads(event_json)
        event_time = datetime.fromisoformat(event['timestamp'])

        # Stop processing events after target time
        if event_time > target_dt:
            break

        ticket_id = event['ticket_id']
        scan_type = event['scan_type']

        if scan_type == 'entry':
            inside.add(ticket_id)
        else:
            inside.discard(ticket_id)

    return len(inside)


# ===========================================================================
# QUESTION 3: DETAILED BREAKDOWN - Aggregation and GROUP BY
# ===========================================================================

"""
📚 DATABASE LEARNING - QUESTION 3: Aggregation
===============================================

CONCEPT: GROUP BY and Multiple Aggregations
--------------------------------------------

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
-- PostgreSQL can return JSON directly!
WITH current_occupancy AS (
    SELECT DISTINCT ON (s.ticket_id)
        s.ticket_id,
        s.gate,
        s.scan_type,
        t.ticket_type
    FROM scans s
    JOIN tickets t ON s.ticket_id = t.ticket_id
    ORDER BY s.ticket_id, s.scan_time DESC
)
SELECT
    json_build_object(
        'total_occupancy', COUNT(*),
        'by_ticket_type', json_agg(
            json_build_object(
                'ticket_type', ticket_type,
                'count', COUNT(*)
            )
        )
    ) as response
FROM current_occupancy
WHERE scan_type = 'entry'
GROUP BY ticket_type;

Interview Tip: PostgreSQL has amazing JSON support!
This is perfect for REST APIs.
"""


def get_detailed_breakdown_sql() -> Dict:
    """
    SQL SOLUTION: Return comprehensive occupancy breakdown.

    Uses JOINs and GROUP BY to create detailed report.

    Returns:
        {
            'total_occupancy': 4,
            'by_gate': {'A': 1, 'B': 1, 'C': 2},
            'by_ticket_type': {'VIP': 1, 'General': 3}
        }
    """
    conn = psycopg2.connect("dbname=occupancy_db_learning2 user=tomfyfe")
    cursor = conn.cursor()

    result = {}

    # Total occupancy
    cursor.execute("""
        WITH last_scans AS (
            SELECT DISTINCT ON (ticket_id)
                ticket_id,
                scan_type
            FROM scans
            ORDER BY ticket_id, scan_time DESC
        )
        SELECT COUNT(*)
        FROM last_scans
        WHERE scan_type = 'entry';
    """)
    result['total_occupancy'] = cursor.fetchone()[0]

    # By gate
    cursor.execute("""
        WITH last_scans AS (
            SELECT DISTINCT ON (ticket_id)
                ticket_id,
                gate,
                scan_type
            FROM scans
            ORDER BY ticket_id, scan_time DESC
        )
        SELECT gate, COUNT(*)
        FROM last_scans
        WHERE scan_type = 'entry'
        GROUP BY gate
        ORDER BY gate;
    """)
    result['by_gate'] = {row[0]: row[1] for row in cursor.fetchall()}

    # By ticket type (needs JOIN)
    cursor.execute("""
        WITH last_scans AS (
            SELECT DISTINCT ON (s.ticket_id)
                s.ticket_id,
                s.scan_type,
                t.ticket_type
            FROM scans s
            JOIN tickets t ON s.ticket_id = t.ticket_id
            ORDER BY s.ticket_id, s.scan_time DESC
        )
        SELECT ticket_type, COUNT(*)
        FROM last_scans
        WHERE scan_type = 'entry'
        GROUP BY ticket_type;
    """)
    result['by_ticket_type'] = {row[0]: row[1] for row in cursor.fetchall()}

    conn.close()
    return result


# ===========================================================================
# QUESTION 4: ANOMALY DETECTION - Window Functions
# ===========================================================================

"""
📚 DATABASE LEARNING - QUESTION 4: Window Functions
====================================================

CONCEPT: LAG and LEAD - Compare with Previous/Next Row
-------------------------------------------------------

Window functions let you access other rows related to the current row.

LAG - look at previous row:
----------------------------
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

Interview Tip: Window functions are powerful for analytics!
They're often faster than self-joins for "compare with previous row" logic.
"""


def detect_anomalies_sql() -> Dict[str, List[str]]:
    """
    SQL SOLUTION: Detect anomalies using window functions.

    Detects:
    - duplicate_entries: Ticket enters twice without exiting
    - exit_without_entry: Ticket exits but never entered

    Returns:
        {
            'duplicate_entries': ['T003'],
            'exit_without_entry': []
        }
    """
    conn = psycopg2.connect("dbname=occupancy_db_learning2 user=tomfyfe")
    cursor = conn.cursor()

    result = {'duplicate_entries': [], 'exit_without_entry': []}

    # Duplicate entries
    cursor.execute("""
        WITH scan_with_previous AS (
            SELECT
                ticket_id,
                scan_type,
                LAG(scan_type) OVER (PARTITION BY ticket_id ORDER BY scan_time) as prev_scan
            FROM scans
        )
        SELECT DISTINCT ticket_id
        FROM scan_with_previous
        WHERE scan_type = 'entry' AND prev_scan = 'entry';
    """)
    result['duplicate_entries'] = [row[0] for row in cursor.fetchall()]

    # Exit without entry
    cursor.execute("""
        WITH scan_with_previous AS (
            SELECT
                ticket_id,
                scan_type,
                LAG(scan_type) OVER (PARTITION BY ticket_id ORDER BY scan_time) as prev_scan
            FROM scans
        )
        SELECT DISTINCT ticket_id
        FROM scan_with_previous
        WHERE scan_type = 'exit' AND (prev_scan IS NULL OR prev_scan = 'exit');
    """)
    result['exit_without_entry'] = [row[0] for row in cursor.fetchall()]

    conn.close()
    return result


# ===========================================================================
# QUESTION 5: CAPACITY MANAGEMENT - Transactions & Constraints
# ===========================================================================

"""
📚 DATABASE LEARNING - QUESTION 5: Transactions & Business Rules
=================================================================

CONCEPT: Database Constraints
------------------------------
Enforce business rules at the database level.

Ensure ticket types are valid:
-------------------------------
ALTER TABLE tickets
ADD CONSTRAINT valid_ticket_type
CHECK (ticket_type IN ('VIP', 'General', 'Staff', 'Press'));

-- Prevent negative prices
ALTER TABLE tickets
ADD CONSTRAINT positive_price
CHECK (price >= 0);

CONCEPT: Transactions (ACID properties)
----------------------------------------
Real systems need atomic operations.

Example: Someone buys a ticket and immediately scans in
--------------------------------------------------------
BEGIN;

-- Insert the ticket
INSERT INTO tickets (ticket_id, user_id, ticket_type, price)
VALUES ('T100', 'U123', 'VIP', 150.00);

-- Record the entry scan
INSERT INTO scans (ticket_id, gate, scan_type, scan_time)
VALUES ('T100', 'A', 'entry', NOW());

-- If either fails, both are rolled back
COMMIT;

Capacity Management with Triggers:
-----------------------------------
CREATE OR REPLACE FUNCTION check_venue_capacity()
RETURNS TRIGGER AS $$
DECLARE
    current_count INTEGER;
    max_cap INTEGER := 100;
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
occupancy = count_current_occupancy_sql()
r.setex('current_occupancy', 10, occupancy)

# Read from cache
cached = r.get('current_occupancy')
if cached:
    return int(cached)
else:
    # Cache miss, query database
    return count_current_occupancy_sql()

This reduces database load for frequently-accessed data!
"""


# ===========================================================================
# COMPLETE INTERVIEW DISCUSSION POINTS
# ===========================================================================

"""
📚 SQL VS PYTHON - When to Use Each
====================================

Decision Tree:
--------------
1. Is data already in a database?
   → YES: Start with SQL
   → NO: Use Python

2. Do you need to process ALL data?
   → YES: SQL (let database optimize)
   → NO: Python with filtering

3. Is it a simple aggregation (COUNT, SUM, GROUP BY)?
   → YES: SQL is faster
   → NO: Python for complex logic

4. Real-time streaming data?
   → Python (process as it arrives)

5. Need to JOIN multiple tables?
   → SQL (optimized for this)

6. Complex business rules or external API calls?
   → Python (more flexible)

Hybrid Approach (Best Practice):
---------------------------------
1. Use SQL to FILTER and AGGREGATE large datasets
2. Load results into Python for complex processing
3. Cache frequently-accessed data in Redis

Example:
-- SQL: Filter down to relevant data
WITH recent_scans AS (
    SELECT * FROM scans WHERE scan_time > NOW() - INTERVAL '1 hour'
)
SELECT * FROM recent_scans;

# Python: Complex business logic
def process_recent_scans(scans):
    # ML predictions, external API calls, complex rules
    ...

Interview Talking Points:
--------------------------
Q: "When would you use SQL vs Python for occupancy tracking?"

A: "For historical queries on stored data, SQL is faster - the database
can use indexes and optimize the query plan. But for real-time streaming
events coming from gate scanners, Python is better since we're processing
events as they arrive. In production, I'd use both: SQL for analytics
queries, Python for real-time processing, and Redis to cache current
occupancy to reduce database load."

Q: "How would you handle concurrent scans at capacity?"

A: "I'd use database transactions with SELECT FOR UPDATE to lock the
occupancy count while checking capacity. This prevents race conditions
where two people scan simultaneously when there's only one spot left.
Alternatively, use Redis atomic counters with INCR/DECR for high-
throughput scenarios."

Q: "What about data integrity?"

A: "Foreign keys prevent invalid scans (can't scan ticket that doesn't
exist). CHECK constraints ensure valid ticket types. Triggers can enforce
business rules like capacity limits. And we'd have audit logs to track
all changes for security and debugging."
"""


# ===========================================================================
# TEST RUNNER
# ===========================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("DATABASE-FOCUSED OCCUPANCY LEARNING - SQL & PostgreSQL")
    print("=" * 70)

    # Set up database
    print("\n📊 Setting up database schema...")
    setup_database()
    populate_database()

    # Test Q1: Current occupancy
    print("\n" + "=" * 70)
    print("QUESTION 1: Current Occupancy - SQL vs Python")
    print("=" * 70)

    sql_result = count_current_occupancy_sql()
    python_result = count_current_occupancy_python(mock_scan_stream())

    print(f"SQL result:    {sql_result}")
    print(f"Python result: {python_result}")
    print(f"Match: {'✅' if sql_result == python_result else '❌'}")

    # Test Q2: Time-based
    print("\n" + "=" * 70)
    print("QUESTION 2: Occupancy at Specific Time")
    print("=" * 70)

    target = '2025-09-30 11:30:00'
    sql_result = get_occupancy_at_time_sql(target)
    python_result = get_occupancy_at_time_python(mock_scan_stream(), '2025-09-30T11:30:00')

    print(f"At {target}:")
    print(f"SQL result:    {sql_result}")
    print(f"Python result: {python_result}")
    print(f"Match: {'✅' if sql_result == python_result else '❌'}")

    # Test Q3: Detailed breakdown
    print("\n" + "=" * 70)
    print("QUESTION 3: Detailed Breakdown with JOINs")
    print("=" * 70)

    breakdown = get_detailed_breakdown_sql()
    print(f"Total occupancy: {breakdown['total_occupancy']}")
    print(f"By gate: {breakdown['by_gate']}")
    print(f"By ticket type: {breakdown['by_ticket_type']}")

    # Test Q4: Anomalies
    print("\n" + "=" * 70)
    print("QUESTION 4: Anomaly Detection with Window Functions")
    print("=" * 70)

    anomalies = detect_anomalies_sql()
    print(f"Duplicate entries: {anomalies['duplicate_entries']}")
    print(f"Exit without entry: {anomalies['exit_without_entry']}")
    print(f"Expected: T003 has duplicate entry - {'✅' if 'T003' in anomalies['duplicate_entries'] else '❌'}")

    print("\n" + "=" * 70)
    print("DONE! Review the code comments for SQL learning concepts.")
    print("=" * 70)
