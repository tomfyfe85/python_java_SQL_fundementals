# SQL Basics Learning Module
# ==========================
# Time estimate: ~1 hour
# Prerequisites: Database 'occupancy_db_learning2' must exist with scans and tickets tables
#
# SETUP: Run this first to populate the database
# python3 occupancy_db_learning2.py

"""
📚 HOW TO USE THIS MODULE
=========================

1. Read each learning section
2. Write the SQL query to answer the question
3. Test your query in psql or using the test functions below
4. Check your answer against the expected output
5. Move to the next section

REFER TO: sql_cheat_sheet.md for all commands and syntax

CONNECT TO DATABASE:
$ psql occupancy_db_learning2

TEST YOUR QUERIES:
Use the test functions at the bottom of this file
"""

import psycopg2

# ===========================================================================
# SECTION 1: Basic SELECT and WHERE
# ===========================================================================

"""
📖 LEARNING: Basic Queries
===========================

The most fundamental SQL operation is SELECT - retrieving data from tables.

Syntax:
    SELECT column1, column2 FROM table_name;
    SELECT * FROM table_name;  -- * means "all columns"
    SELECT column1 FROM table_name WHERE condition;

WHERE clause filters rows based on conditions:
    WHERE column = 'value'    -- Exact match
    WHERE column != 'value'   -- Not equal
    WHERE column > 10         -- Greater than (works with numbers/dates)

Real-world example:
    SELECT * FROM scans WHERE scan_type = 'entry';

This would be used in your FastAPI endpoint to show only entry scans.
"""

# QUESTION 1.1: Get all scans
# ============================
# Write a query to select ALL columns from the scans table.
#
# Expected output: All 12 rows from scans table with columns:
# scan_id | ticket_id | gate | scan_type | scan_time | flagged_suspicious | user_id
#
# HINT: Use SELECT * FROM...

QUESTION_1_1 = """
SELECT * FROM scans;
"""

# QUESTION 1.2: Get specific columns
# ===================================
# Write a query to get ONLY ticket_id, scan_type, and scan_time from scans.
#
# Expected output: 12 rows with only these 3 columns
#
# Real-world use: API responses - only send the data the frontend needs

QUESTION_1_2 = """
SELECT ticket_id, scan_type, scan_time FROM scans
"""

# QUESTION 1.3: Filter by scan type
# ==================================
# Write a query to get all entry scans (scan_type = 'entry').
#
# Expected output: 8 rows (all entry scans)
#
# Real-world use: "Show me only people entering" for capacity calculation

QUESTION_1_3 = """
SELECT * FROM scans 
WHERE scan_type = 'entry'
"""

# QUESTION 1.4: Filter by gate
# =============================
# Write a query to get all scans at Gate A.
#
# Expected output: 6 rows (scans where gate = 'A')
#
# Real-world use: "How busy is the main entrance?"

QUESTION_1_4 = """
SELECT * FROM scans WHERE gate = 'A'
"""

# ===========================================================================
# SECTION 2: Counting and Aggregates
# ===========================================================================

"""
📖 LEARNING: COUNT and Aggregates
===================================

Aggregate functions perform calculations on multiple rows:
    COUNT(*) - Count all rows
    COUNT(column) - Count non-NULL values in column
    COUNT(DISTINCT column) - Count unique values
    MAX(column) - Get highest value
    MIN(column) - Get lowest value

Syntax:
    SELECT COUNT(*) FROM scans;
    SELECT COUNT(DISTINCT ticket_id) FROM scans;
    SELECT MAX(scan_time) FROM scans;

Real-world example:
    SELECT COUNT(*) FROM scans WHERE scan_type = 'entry';

This tells you how many entry scans happened (for dashboard metrics).
"""

# QUESTION 2.1: Count all scans
# ==============================
# Write a query to count the total number of scans in the database.
#
# Expected output: 12
#
# Real-world use: "Total activity today" metric

QUESTION_2_1 = """
SELECT COUNT (*) FROM scans
"""

# QUESTION 2.2: Count entry scans
# ================================
# Write a query to count only entry scans.
#
# Expected output: 8
#
# Real-world use: "How many people entered today?"

QUESTION_2_2 = """
SELECT COUNT (*) FROM scans
WHERE scan_type = 'entry'
"""

# QUESTION 2.3: Count unique tickets
# ===================================
# Write a query to count how many UNIQUE tickets were scanned.
#
# Expected output: 7 (T001 through T007, even though some scanned multiple times)
#
# HINT: Use COUNT(DISTINCT ticket_id)
# Real-world use: "Unique visitors" (not total scans)

QUESTION_2_3 = """
SELECT COUNT(DISTINCT ticket_id) FROM scans
"""

# QUESTION 2.4: Latest scan time
# ===============================
# Write a query to find the timestamp of the most recent scan.
#
# Expected output: 2025-09-30 12:05:00
#
# Real-world use: "When was last activity?" for system health monitoring

QUESTION_2_4 = """
SELECT MAX (scan_time) FROM scans;
"""

# ===========================================================================
# SECTION 3: GROUP BY - Counting by Category
# ===========================================================================

"""
📖 LEARNING: GROUP BY
======================

GROUP BY groups rows with the same value and lets you count/aggregate each group.

Syntax:
    SELECT column, COUNT(*)
    FROM table
    GROUP BY column;

Example:
    SELECT gate, COUNT(*)
    FROM scans
    GROUP BY gate;

    Result:
    gate | count
    -----|------
    A    | 6
    B    | 4
    C    | 2

Real-world use: "How many scans per gate?" to determine which entrance is busiest.

IMPORTANT: Any column in SELECT (except aggregates) must be in GROUP BY!
"""

# QUESTION 3.1: Count scans per gate
# ===================================
# Write a query to count how many scans happened at each gate.
#
# Expected output:
# gate | count
# -----|------
# A    | 6
# B    | 4
# C    | 2
#
# Real-world use: "Which entrance is busiest?" for staff allocation

QUESTION_3_1 = """
SELECT gate, COUNT(*)
FROM scans
GROUP BY gate
ORDER BY gate
;
"""


# QUESTION 3.2: Count entries vs exits
# =====================================
# Write a query to count how many entries vs exits occurred.
#
# Expected output:
# scan_type | count
# ----------|------
# entry     | 8
# exit      | 4
#
# Real-world use: "Entry/exit ratio" to detect if people are still inside

QUESTION_3_2 = """
SELECT scan_type, COUNT (*)
FROM scans
GROUP BY scan_type
"""

# QUESTION 3.3: Scans per ticket
# ===============================
# Write a query to count how many times each ticket was scanned.
#
# Expected output:
# ticket_id | count
# ----------|------
# T001      | 3
# T002      | 2
# T003      | 3
# T004      | 2
# T005      | 1
# T006      | 1
# T007      | 1
#
# Real-world use: "Detect suspicious activity" - tickets scanned too many times

QUESTION_3_3 = """
SELECT ticket_id, COUNT(*)
FROM scans
GROUP BY ticket_id
;
"""

# ===========================================================================
# SECTION 4: INNER JOIN - Combining Tables
# ===========================================================================

"""
📖 LEARNING: INNER JOIN
========================

INNER JOIN combines rows from two tables where there's a match in both.

Syntax:
    SELECT t1.column, t2.column
    FROM table1 t1
    INNER JOIN table2 t2 ON t1.id = t2.id;

Example with our data:
    SELECT s.ticket_id, s.scan_type, t.ticket_type
    FROM scans s
    INNER JOIN tickets t ON s.ticket_id = t.ticket_id;

This joins scans with tickets to show ticket type for each scan.

Aliases (s and t) make queries shorter:
    scans s means "call scans 's' in this query"

Real-world use: "Show scan activity WITH ticket type" - you need data from BOTH tables.

RESULT: Only scans that have matching tickets (orphaned records excluded).
"""

# QUESTION 4.1: Scans with ticket types
# ======================================
# Write a query to show ticket_id, scan_type, and ticket_type for all scans.
#
# Expected output: 12 rows with 3 columns
# ticket_id | scan_type | ticket_type
# ----------|-----------|------------
# T001      | entry     | VIP
# T002      | entry     | General
# ...
#
# Real-world use: "What type of tickets are being scanned?"

QUESTION_4_1 = """
SELECT t.ticket_id, s.scan_type, t.ticket_type
FROM scans s
INNER JOIN tickets t ON s.ticket_id = t.ticket_id;
"""

# QUESTION 4.2: Count scans by ticket type
# =========================================
# Write a query to count how many scans happened for each ticket type (VIP vs General).
#
# Expected output:
# ticket_type | count
# ------------|------
# VIP         | 4
# General     | 8
#
# Real-world use: "VIP vs General usage metrics"

QUESTION_4_2 = """
SELECT t.ticket_type, COUNT(*)
FROM tickets t
INNER JOIN scans s ON t.ticket_id = s.ticket_id
GROUP BY t.ticket_type
"""

# QUESTION 4.3: VIP entry scans only
# ===================================
# Write a query to show all ENTRY scans for VIP tickets.
#
# Expected output: 3 rows (T001 and T005 entries)
# ticket_id | scan_type | ticket_type
# ----------|-----------|------------
# T001      | entry     | VIP
# T005      | entry     | VIP
# T001      | entry     | VIP
#
# Real-world use: "Track VIP arrivals"

QUESTION_4_3 = """
SELECT t.ticket_id, s.scan_type, t.ticket_type
FROM scans s
INNER JOIN tickets t ON t.ticket_id = s.ticket_id
WHERE s.scan_type = 'entry' and t.ticket_type = 'VIP';
"""

# ===========================================================================
# SECTION 5: LEFT JOIN - All from Left Table
# ===========================================================================

"""
📖 LEARNING: LEFT JOIN
=======================

LEFT JOIN returns ALL rows from the left table, with matching rows from right table.
If no match, right table columns are NULL.

Syntax:
    SELECT t.ticket_id, s.scan_type
    FROM tickets t
    LEFT JOIN scans s ON t.ticket_id = s.ticket_id;

Difference from INNER JOIN:
    INNER JOIN: Only tickets that were scanned
    LEFT JOIN:  ALL tickets, show scan data if exists

Example result:
    ticket_id | scan_type
    ----------|-----------
    T001      | entry      ← Has scans
    T001      | exit
    T008      | NULL       ← No scans! (unused ticket)

Real-world use: "Show ALL tickets, even unused ones" to find no-shows.

CHECK FOR NULLS: WHERE s.scan_type IS NULL finds tickets never scanned.
"""

# QUESTION 5.1: All tickets with scans (if any)
# ==============================================
# Write a query using LEFT JOIN to show ALL tickets with their scan data.
#
# Expected output: 13 rows
# - 12 rows for scans that exist (T001-T007)
# - 1 row for T008 (with NULL for scan_type and scan_time)
#
# Real-world use: "Show all tickets, include scan activity if it happened"

QUESTION_5_1 = """
SELECT * FROM tickets t
LEFT JOIN scans s ON t.ticket_id = s.ticket_id;
"""

# QUESTION 5.2: Find unused tickets
# ==================================
# Write a query to find tickets that were NEVER scanned.
#
# Expected output: 1 row
# ticket_id | ticket_type
# ----------|------------
# T008      | General
#
# Real-world use: "Which tickets were no-shows?" for refund processing

QUESTION_5_2 = """
SELECT t.ticket_id, t.ticket_type
FROM tickets t
LEFT JOIN scans s ON t.ticket_id = s.ticket_id
WHERE s.scan_type is NULL
"""

# QUESTION 5.3: Count scans per ticket (including zero)
# ======================================================
# Write a query to show each ticket and how many times it was scanned.
# Include tickets with zero scans.
#
# Expected output:
# ticket_id | ticket_type | scan_count
# ----------|-------------|------------
# T001      | VIP         | 3
# T002      | General     | 2
# T003      | General     | 3
# T004      | General     | 2
# T005      | VIP         | 1
# T006      | General     | 1
# T007      | General     | 1
# T008      | General     | 0  ← This ticket was never scanned!
#
# Use COUNT(s.scan_id) not COUNT(*) - COUNT(*) counts all rows, COUNT(column) counts non-NULLs
# Real-world use: "Ticket usage report"

QUESTION_5_3 = """


"""

# ===========================================================================
# SECTION 6: DISTINCT ON - Latest per Group
# ===========================================================================

"""
📖 LEARNING: DISTINCT ON (PostgreSQL specific)
===============================================

DISTINCT ON gets the first row from each group. Combined with ORDER BY, you can
get "the latest X for each Y".

Syntax:
    SELECT DISTINCT ON(group_column) column1, column2
    FROM table
    ORDER BY group_column, sort_column DESC;

Example - Get each person's most recent scan:
    SELECT DISTINCT ON(ticket_id) ticket_id, scan_type, scan_time
    FROM scans
    ORDER BY ticket_id, scan_time DESC;

How it works:
    1. Groups by ticket_id
    2. Within each group, sorts by scan_time DESC (newest first)
    3. Takes the FIRST row from each group (which is the newest due to DESC)

Real-world use: "Who is currently inside?"
    - Get last scan per person
    - If it's 'entry', they're inside
    - If it's 'exit', they're outside
# HINT: Use query from 6.1, wrap in a WITH clause or subquery, filter WHERE scan_type = 'entry'

This is the SQL equivalent of your Python set tracking!
"""

# QUESTION 6.1: Get each ticket's last scan
# ==========================================
# Write a query to get the most recent scan for each ticket.
#
# Expected output: 7 rows (one per ticket that was scanned)
# ticket_id | scan_type | scan_time
# ----------|-----------|-------------------
# T001      | entry     | 2025-09-30 11:05:00
# T002      | exit      | 2025-09-30 11:10:00
# T003      | exit      | 2025-09-30 12:00:00
# T004      | exit      | 2025-09-30 12:05:00
# T005      | entry     | 2025-09-30 10:05:00
# T006      | entry     | 2025-09-30 11:05:00
# T007      | entry     | 2025-09-30 11:20:00
#
# HINT: DISTINCT ON(ticket_id) ORDER BY ticket_id, scan_time DESC
# Real-world use: "What's each person's current status?"

QUESTION_6_1 = """
SELECT DISTINCT ON(ticket_id) s.ticket_id, s.scan_type, s.scan_time
FROM scans s
ORDER BY s.ticket_id, scan_time DESC
"""

# QUESTION 6.2: Who is currently inside?
# =======================================
# Write a query to find tickets currently inside the venue.
# (Last scan was 'entry')
#
# Expected output: 4 rows
# ticket_id
# ---------
# T001
# T005
# T006
# T007
#
# Real-world use: "Current occupancy list"

QUESTION_6_2 = """
WITH inside AS(SELECT  DISTINCT ON(ticket_id) ticket_id, scan_type
FROM scans 
ORDER BY ticket_id, scan_time DESC)
SELECT ticket_id
FROM inside
WHERE scan_type = 'entry'
"""

# QUESTION 6.3: Count current occupancy
# ======================================
# Write a query to count how many tickets are currently inside.
#
# Expected output: 4
#
# HINT: Use query from 6.2, wrap it and COUNT
# Real-world use: "Current occupancy number" for dashboard

QUESTION_6_3 = """
WITH inside AS(SELECT DISTINCT ON(ticket_id) ticket_id, scan_type
FROM scans 
ORDER BY ticket_id, scan_time DESC)
SELECT COUNT(ticket_id)
FROM inside
WHERE scan_type = 'entry'
"""

# ===========================================================================
# SECTION 7: WITH (CTE) - Multi-Step Queries
# ===========================================================================

"""
📖 LEARNING: WITH (Common Table Expressions)
=============================================

WITH creates a temporary named result you can reference in your main query.
It's like defining a variable in Python before using it.

Syntax:
    WITH temp_name AS (
        SELECT ...
    )
    SELECT * FROM temp_name WHERE ...;

Example - Two-step occupancy calculation:
    WITH last_scans AS (
        SELECT DISTINCT ON(ticket_id) ticket_id, scan_type
        FROM scans
        ORDER BY ticket_id, scan_time DESC
    )
    SELECT COUNT(*)
    FROM last_scans
    WHERE scan_type = 'entry';

Step 1: Get last scan per person (named "last_scans")
Step 2: Count how many are entries

Benefits:
    - Makes complex queries readable
    - Can reuse the CTE multiple times in same query
    - Self-documenting (the name explains what it is)

Real-world use: Any complex calculation broken into logical steps.
"""

# QUESTION 7.1: Current occupancy with CTE
# =========================================
# Rewrite Question 6.3 using a WITH clause for clarity.
#
# Expected output: 4
#
# Structure:
#     WITH last_scans AS (
#         [query to get last scan per ticket]
#     )
#     SELECT COUNT(*) FROM last_scans WHERE scan_type = 'entry';
#
# Real-world use: "This is how you'd write it in production - clear and maintainable"

QUESTION_7_1 = """

"""

# QUESTION 7.2: Current occupancy by ticket type
# ===============================================
# Write a query to count current occupancy split by ticket type (VIP vs General).
#
# Expected output:
# ticket_type | currently_inside
# ------------|------------------
# VIP         | 2  (T001, T005)
# General     | 2  (T006, T007)
#
# HINT: WITH last_scans AS (...), JOIN with tickets, GROUP BY ticket_type
# Real-world use: "How many VIPs vs General are currently inside?"

QUESTION_7_2 = """

"""

# QUESTION 7.3: Occupancy by gate (where they entered)
# =====================================================
# Write a query to count how many people are currently inside, grouped by which gate they last used.
#
# Expected output:
# gate | currently_inside
# -----|------------------
# A    | 2  (T001, T006)
# B    | 1  (T005)
# C    | 1  (T007)
#
# HINT: WITH last_scans (include gate), filter for entry, GROUP BY gate
# Real-world use: "Which gates are people currently using?"

QUESTION_7_3 = """

"""

# ===========================================================================
# SECTION 8: CASE - Conditional Logic
# ===========================================================================

"""
📖 LEARNING: CASE Statements
=============================

CASE adds if/else logic to SQL queries. It transforms values based on conditions.

Syntax:
    CASE
        WHEN condition1 THEN result1
        WHEN condition2 THEN result2
        ELSE default_result
    END

Example - Convert scan type to +1/-1 for math:
    SELECT
        ticket_id,
        CASE
            WHEN scan_type = 'entry' THEN 1
            ELSE -1
        END as occupancy_change
    FROM scans;

Result:
    ticket_id | occupancy_change
    ----------|------------------
    T001      | 1   (entry)
    T001      | -1  (exit)
    T001      | 1   (entry)

Real-world use: Transform data for calculations or create readable labels.
"""

# QUESTION 8.1: Label scan directions
# ====================================
# Write a query to show ticket_id and a readable direction label.
# 'entry' → 'Entering', 'exit' → 'Leaving'
#
# Expected output: 12 rows
# ticket_id | direction
# ----------|-----------
# T001      | Entering
# T002      | Entering
# T001      | Leaving
# ...
#
# HINT: Use CASE WHEN scan_type = 'entry' THEN 'Entering' WHEN scan_type = 'exit' THEN 'Leaving' END
# Real-world use: "API response with friendly labels"

QUESTION_8_1 = """

"""

# QUESTION 8.2: Calculate occupancy changes
# ==========================================
# Write a query to show each scan with an occupancy_change column (+1 for entry, -1 for exit).
#
# Expected output: 12 rows
# ticket_id | scan_type | occupancy_change
# ----------|-----------|------------------
# T001      | entry     | 1
# T002      | entry     | 1
# T001      | exit      | -1
# ...
#
# Real-world use: "Calculate running occupancy total"

QUESTION_8_2 = """

"""

# ===========================================================================
# SECTION 9: Putting It All Together
# ===========================================================================

"""
📖 CHALLENGE: Real-World Analytics Query
=========================================

Now combine everything you've learned to answer a complex question:

"Create a report showing:
- Each ticket
- Ticket type (VIP/General)
- How many times they scanned in
- How many times they scanned out
- Whether they're currently inside (Yes/No)
- Their last scan time"

This uses:
    ✓ JOIN (tickets + scans)
    ✓ LEFT JOIN (include unused tickets)
    ✓ GROUP BY (count per ticket)
    ✓ DISTINCT ON (for last scan)
    ✓ CASE (for Yes/No status)
    ✓ Aggregate functions (COUNT, MAX)

This is the kind of query you might write in the interview!
"""

# QUESTION 9.1: Comprehensive ticket report
# ==========================================
# Write a query for the report described above.
#
# Expected output:
# ticket_id | ticket_type | total_entries | total_exits | currently_inside | last_scan_time
# ----------|-------------|---------------|-------------|------------------|------------------
# T001      | VIP         | 2             | 1           | Yes              | 2025-09-30 11:05:00
# T002      | General     | 1             | 1           | No               | 2025-09-30 11:10:00
# T003      | General     | 2             | 1           | No               | 2025-09-30 12:00:00
# T004      | General     | 1             | 1           | No               | 2025-09-30 12:05:00
# T005      | VIP         | 1             | 0           | Yes              | 2025-09-30 10:05:00
# T006      | General     | 1             | 0           | Yes              | 2025-09-30 11:05:00
# T007      | General     | 1             | 0           | Yes              | 2025-09-30 11:20:00
# T008      | General     | 0             | 0           | No               | NULL
#
# HINT: This is challenging! Break it into steps:
# 1. Start with tickets (to get all tickets)
# 2. LEFT JOIN to count entries/exits
# 3. Use DISTINCT ON in a subquery to get last scan
# 4. Use CASE to determine if inside
#
# Real-world use: "Executive dashboard - complete ticket usage analytics"

QUESTION_9_1 = """

"""

# ===========================================================================
# TEST FUNCTIONS - Use these to check your answers
# ===========================================================================

def test_query(question_num, query, expected_description):
    """
    Test your SQL query.

    Usage:
        test_query("1.1", QUESTION_1_1, "Should return 12 rows with all columns")
    """
    if not query.strip():
        print(f"❌ Question {question_num}: No query written yet!")
        return

    try:
        conn = psycopg2.connect("dbname=occupancy_db_learning2 user=tomfyfe")
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        print(f"\n✅ Question {question_num} executed successfully!")
        print(f"Expected: {expected_description}")
        print(f"Got {len(results)} rows")
        print("\nFirst 5 rows:")
        for row in results[:5]:
            print(row)

        conn.close()
    except Exception as e:
        print(f"\n❌ Question {question_num} failed:")
        print(f"Error: {e}")

def test_all():
    """Run all your queries to check for syntax errors."""
    questions = [
        ("1.1", QUESTION_1_1, "12 rows, all columns"),
        ("1.2", QUESTION_1_2, "12 rows, 3 columns"),
        ("1.3", QUESTION_1_3, "8 rows (entries only)"),
        ("1.4", QUESTION_1_4, "6 rows (Gate A only)"),
        ("2.1", QUESTION_2_1, "Count: 12"),
        ("2.2", QUESTION_2_2, "Count: 8"),
        ("2.3", QUESTION_2_3, "Count: 7"),
        ("2.4", QUESTION_2_4, "Timestamp: 2025-09-30 12:05:00"),
        ("3.1", QUESTION_3_1, "3 rows (A:6, B:4, C:2)"),
        ("3.2", QUESTION_3_2, "2 rows (entry:8, exit:4)"),
        ("3.3", QUESTION_3_3, "7 rows (count per ticket)"),
        ("4.1", QUESTION_4_1, "12 rows with ticket types"),
        ("4.2", QUESTION_4_2, "2 rows (VIP:4, General:8)"),
        ("4.3", QUESTION_4_3, "3 rows (VIP entries)"),
        ("5.1", QUESTION_5_1, "13 rows (includes T008 with NULL scans)"),
        ("5.2", QUESTION_5_2, "1 row (T008)"),
        ("5.3", QUESTION_5_3, "8 rows (including T008 with 0)"),
        ("6.1", QUESTION_6_1, "7 rows (last scan per ticket)"),
        ("6.2", QUESTION_6_2, "4 rows (currently inside)"),
        ("6.3", QUESTION_6_3, "Count: 4"),
        ("7.1", QUESTION_7_1, "Count: 4"),
        ("7.2", QUESTION_7_2, "2 rows (VIP:2, General:2)"),
        ("7.3", QUESTION_7_3, "3 rows (by gate)"),
        ("8.1", QUESTION_8_1, "12 rows with labels"),
        ("8.2", QUESTION_8_2, "12 rows with +1/-1"),
        ("9.1", QUESTION_9_1, "8 rows (complete report)"),
    ]

    for num, query, expected in questions:
        if query.strip():
            test_query(num, query, expected)

# ===========================================================================
# QUICK START
# ===========================================================================

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         SQL BASICS LEARNING MODULE                       ║
    ║         Time estimate: ~1 hour                           ║
    ╚══════════════════════════════════════════════════════════╝

    📚 Instructions:
    1. Open sql_cheat_sheet.md as reference
    2. Fill in the QUESTION variables above with SQL queries
    3. Test with: test_query("1.1", QUESTION_1_1, "description")
    4. Or test all at once with: test_all()

    🎯 Goal: By the end, you'll be able to:
    - Write SELECT queries with WHERE filters
    - Use COUNT, GROUP BY for aggregates
    - Join tables with INNER JOIN and LEFT JOIN
    - Get latest records with DISTINCT ON
    - Build complex queries with WITH (CTEs)
    - Use CASE for conditional logic

    💡 Tip: Start with Section 1, work through sequentially!

    Ready? Open the file and start with QUESTION_1_1!
    """)

    # Uncomment to test a specific question:
    # test_query("1.1", QUESTION_1_1, "Should return all scans")

    # Uncomment to test all questions at once:
    test_all()



