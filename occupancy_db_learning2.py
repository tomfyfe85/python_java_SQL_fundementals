# # Event Occupancy Practice Test with Database Learning
# # =====================================================
# # Learn SQL and database concepts while solving occupancy problems

# from datetime import datetime
# from typing import Dict, List, Set, Optional
# import psycopg2

# # MOCK EVENT STREAM (same as original)
# def mock_occupancy_stream():
#     """Generator that yields entry and exit scan events."""
#     events = [
#         {'ticket_id': 'T001', 'user_id': 'U123', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T002', 'user_id': 'U456', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T003', 'user_id': 'U789', 'gate': 'B', 'timestamp': '2025-09-30T10:02:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T004', 'user_id': 'U111', 'gate': 'C', 'timestamp': '2025-09-30T10:03:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T005', 'user_id': 'U222', 'gate': 'B', 'timestamp': '2025-09-30T10:05:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T001', 'user_id': 'U123', 'gate': 'A', 'timestamp': '2025-09-30T11:00:00', 'scan_type': 'exit'},
#         {'ticket_id': 'T006', 'user_id': 'U333', 'gate': 'A', 'timestamp': '2025-09-30T11:05:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T002', 'user_id': 'U456', 'gate': 'A', 'timestamp': '2025-09-30T11:10:00', 'scan_type': 'exit'},
#         {'ticket_id': 'T003', 'user_id': 'U789', 'gate': 'B', 'timestamp': '2025-09-30T11:15:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T007', 'user_id': 'U444', 'gate': 'C', 'timestamp': '2025-09-30T11:20:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T003', 'user_id': 'U789', 'gate': 'B', 'timestamp': '2025-09-30T12:00:00', 'scan_type': 'exit'},
#         {'ticket_id': 'T004', 'user_id': 'U111', 'gate': 'C', 'timestamp': '2025-09-30T12:05:00', 'scan_type': 'exit'},
#     ]
#     for event in events:
#         yield event


# # ===========================================================================
# # DATABASE SETUP - RUN THIS FIRST!
# # ===========================================================================

# def populate_database():
#     """
#     IMPORTANT: Run this function ONCE to fill your database with test data!
#     This takes the mock event stream and puts it into your PostgreSQL database.
#     """
#     conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
#     cursor = conn.cursor()

#     # Clear any existing data (start fresh)
#     cursor.execute("DELETE FROM scans")

#     # Add all events from the mock stream to database
#     for event in mock_occupancy_stream():
#         cursor.execute("""
#             INSERT INTO scans (ticket_id, user_id, gate, scan_type, scan_time)
#             VALUES (%s, %s, %s, %s, %s)
#         """, (
#             event['ticket_id'],
#             event['user_id'],
#             event['gate'],
#             event['scan_type'],
#             event['timestamp']
#         ))

#     # Save all the inserts
#     conn.commit()
#     conn.close()
#     return

# # ===========================================================================
# # QUESTION 1: Basic Occupancy Count
# # ===========================================================================

# def count_current_occupancy(stream):
#     current_occupancy = set()

#     for event in stream:
#         user_id = event['user_id']
#         scan_type = event['scan_type']
#         if scan_type == 'entry':
#             current_occupancy.add(user_id)
#         else:
#             current_occupancy.discard(user_id)
#     return len(current_occupancy)

# """
# 📚 DATABASE LEARNING - QUESTION 1
# ==================================
# Let's create our first database table to store scan events!

# CONCEPT: What is a database table?
# - Think of it like an Excel spreadsheet
# - Each row is a record (one scan event)
# - Each column is a field (ticket_id, user_id, etc.)

# Step 1: Create your database
# -----------------------------
# In your terminal:
# $ createdb event_venue

# Step 2: Connect and create your first table
# --------------------------------------------
# $ psql event_venue

# Run this SQL:

# CREATE TABLE scans (
#     id SERIAL PRIMARY KEY,           -- Auto-incrementing ID
#     ticket_id VARCHAR(10),           -- Text up to 10 characters
#     user_id VARCHAR(10),            
#     gate VARCHAR(1),                
#     scan_type VARCHAR(5),           -- 'entry' or 'exit'
#     scan_time TIMESTAMP             -- Date and time
# );

# What does this mean?
# - SERIAL: Auto-generates unique numbers (1, 2, 3...)
# - PRIMARY KEY: Unique identifier for each row
# - VARCHAR(n): Text with maximum length n
# - TIMESTAMP: Stores date and time

# Step 3: INSERT data (the C in CRUD - Create)
# ---------------------------------------------
# INSERT INTO scans (ticket_id, user_id, gate, scan_type, scan_time)
# VALUES ('T001', 'U123', 'A', 'entry', '2025-09-30 10:00:00');

# Try inserting a few more events from the mock data! 

# Step 4: READ data (the R in CRUD)
# ----------------------------------
# SELECT * FROM scans;                     -- Get all records
# SELECT * FROM scans WHERE user_id = 'U123';  -- Filter specific user
# """

# def count_current_occupancy_db():
#     """
#     DATABASE CHALLENGE 1: Write a SQL query to find who's currently inside.
    
#     ⚠️ PREREQUISITE: Run populate_database() first to add data!
    
#     Hint: For each person, you need to check:
#     - Did they enter? (last scan_type = 'entry')
#     - Did they leave after entering? (compare timestamps)
    
#     Try this query structure:
#     SELECT COUNT(DISTINCT user_id) FROM scans WHERE...
    
#     🤔 Real scenario: What if someone loses their ticket and security lets them in?
#     How would you record this in the database?
#     """

#     conn = psycopg2.connect("dbname=event_venue user=tomfyfe")
#     cursor = conn.cursor()

#     query = """
#     WITH current_occupancy AS (
#         SELECT DISTINCT ON(user_id) user_id, scan_type
#         FROM scans
#         ORDER BY user_id, scan_time DESC
#         )
#     SELECT COUNT(*) 
#     FROM current_occupancy 
#     WHERE scan_type = 'entry';
#     """

#     cursor.execute(query)
#     result = cursor.fetchone()
#     conn.close()

#     return result[0] if result else 0

# # ===========================================================================
# # QUESTION 2: Occupancy Statistics
# # ===========================================================================


# def get_occupancy_statistics(stream):

#     current_users_present = set()
#     total_entry_count = 0
#     total_exit_count = 0
#     max_occupancy_count = 0

#     for event in stream:
#         user_id = event['user_id']
#         scan_type = event['scan_type']

#         if scan_type == 'entry':
#             current_users_present.add(user_id)
#             total_entry_count += 1
#         else:
#             current_users_present.discard(user_id)
#             total_exit_count += 1

#         max_occupancy_count = max(max_occupancy_count, len(current_users_present))

#     return {
#         'current_occupancy': len(current_users_present),
#         'total_entries': total_entry_count,
#         'total_exits': total_exit_count,
#         'max_occupancy': max_occupancy_count
#     }

# """
# 📚 DATABASE LEARNING - QUESTION 2
# ==================================
# Now let's learn about aggregate functions and tracking statistics!

# CONCEPT: Aggregate Functions
# - COUNT(): Counts rows
# - MAX(): Finds maximum value
# - MIN(): Finds minimum value
# - SUM(): Adds up values
# - AVG(): Calculates average

# Example queries:
# ----------------
# -- Count total entries
# SELECT COUNT(*) FROM scans WHERE scan_type = 'entry';

# -- Count by type
# SELECT scan_type, COUNT(*) 
# FROM scans 
# GROUP BY scan_type;

# IMPORTANT: Running totals (for max occupancy)
# ----------------------------------------------
# This is tricky! We need to track occupancy over time.

# -- This shows occupancy changes over time
# SELECT 
#     scan_time,
#     CASE 
#         WHEN scan_type = 'entry' THEN 1 
#         ELSE -1 
#     END as change
# FROM scans
# ORDER BY scan_time;

# 🚨 REAL SCENARIO: Duplicate ticket scans
# -----------------------------------------
# What happens if someone scans the same ticket twice?
# Should we allow it? Let's add a constraint!

# ALTER TABLE scans 
# ADD CONSTRAINT unique_scan 
# UNIQUE (ticket_id, scan_time);

# This prevents the exact same ticket from scanning at the exact same time.
# But what about scanning twice at different times?
# """

# def get_occupancy_statistics_db():
#     """
#     DATABASE CHALLENGE 2: Calculate statistics using SQL
    
#     Create these queries:
#     1. Count total entries
#     2. Count total exits  
#     3. Find current occupancy
#     4. Calculate max occupancy (hardest!)
    
#     For max occupancy, you'll need a "running total".
#     Research: PostgreSQL window functions - SUM() OVER (ORDER BY...)
    
#     🤔 Real scenario: What if someone tailgates (follows someone in without scanning)?
#     How would this affect your statistics? How could you detect it?
#     """
    
#     conn = psycopg2.connect("dbname=event_venue user=your_username")
#     cursor = conn.cursor()
    
#     stats = {}
    
#     # TODO: Query for total entries
#     cursor.execute("SELECT COUNT(*) FROM scans WHERE scan_type = ?")
#     stats['total_entries'] = cursor.fetchone()[0]
    
#     # TODO: Add queries for other statistics
    
#     conn.close()
#     return stats


# # ===========================================================================
# # QUESTION 3: Occupancy by Gate
# # ===========================================================================

# def count_occupancy_by_gate(stream):
#     """
#     Track current occupancy at each gate separately.
#     Note: People are tracked by the LAST gate they u    
#     Args:
#         stream: Iterator/generator yielding event dictiona  
#     Returns:
#         dict: Gate ID -> number of people currently at that     
#     Expected output: {'A': 1, 'B': 1, 'C'   
#     Reasoning (tracking last gate used):
#     - U222: last used gate B for entry (at gate B)
#     - U333: last used gate A for entry (at gate A)
#     - U444: last used gate C for entry (at gate C)
#     """
#     current_occupancy_per_gate = {}
#     current_occupancy = set()

#     for event in stream:
#         user_id = event['user_id']
#         scan_type = event['scan_type']
#         gate = event['gate']
        
#         if scan_type == 'entry' and user_id not in current_occupancy:
#             current_occupancy.add(user_id)
#             current_occupancy_per_gate[gate] = current_occupancy_per_gate.get(gate, 0) + 1
#         elif scan_type == 'entry' and user_id in current_occupancy:
#             continue
#         else:
#             current_occupancy.discard(user_id)
#             current_occupancy_per_gate[gate] = current_occupancy_per_gate.get(gate, 0) - 1
#     return current_occupancy_per_gate



# """
# 📚 DATABASE LEARNING - QUESTION 3
# ==================================
# Let's explore JOINs and relationships between tables!

# CONCEPT: Normalized Database Design
# ------------------------------------
# Instead of one big table, let's create related tables:

# CREATE TABLE gates (
#     gate_id VARCHAR(1) PRIMARY KEY,
#     gate_name VARCHAR(50),
#     security_level VARCHAR(20)
# );

# CREATE TABLE tickets (
#     ticket_id VARCHAR(10) PRIMARY KEY,
#     user_id VARCHAR(10),
#     ticket_type VARCHAR(20),  -- 'VIP', 'General', 'Staff'
#     is_valid BOOLEAN DEFAULT true
# );

# Now update our scans table to reference these:

# ALTER TABLE scans 
# ADD FOREIGN KEY (gate) REFERENCES gates(gate_id);

# ALTER TABLE scans 
# ADD FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id);

# CONCEPT: JOINs
# --------------
# Connect data from multiple tables:

# SELECT s.*, t.ticket_type, g.gate_name
# FROM scans s
# JOIN tickets t ON s.ticket_id = t.ticket_id
# JOIN gates g ON s.gate = g.gate_id;

# 🚨 REAL SCENARIO: Counterfeit tickets!
# ---------------------------------------
# Someone tries to enter with ticket 'T999' that doesn't exist in our tickets table.
# The FOREIGN KEY constraint would reject this scan!

# This is database-level fraud prevention.
# """

# def count_occupancy_by_gate_db():
#     """
#     DATABASE CHALLENGE 3: Complex query with GROUP BY
    
#     Write a query that:
#     1. Finds people currently inside
#     2. Groups them by their last-used gate
#     3. Counts per gate
    
#     Hint: You'll need a subquery or CTE (Common Table Expression)
    
#     WITH last_gate_used AS (
#         -- Find each person's most recent gate
#     )
#     SELECT gate, COUNT(*) FROM last_gate_used GROUP BY gate;
    
#     🤔 Real scenario: VIP gates vs General gates
#     What if certain tickets can only use certain gates?
#     How would you enforce this in the database?
#     """
    
#     # TODO: Implement database query
#     pass


# # ===========================================================================
# # QUESTION 4: Find People Still Inside
# # ===========================================================================

# def find_people_still_inside(stream):
#     """
#     Return the IDs of people who are still inside the venue.
    
#     Args:
#         stream: Iterator/generator yielding event dictionaries
    
#     Returns:
#         set: User IDs of people currently inside
#     """
#     current_occupancy = set()

#     for event in stream:
#         user_id = event['user_id']
#         scan_type = event['scan_type']
#         if scan_type == 'entry':
#             current_occupancy.add(user_id)
#         else:
#             current_occupancy.discard(user_id)
#     return current_occupancy


# """
# 📚 DATABASE LEARNING - QUESTION 4
# ==================================
# Let's learn about UPDATE and DELETE operations!

# CONCEPT: UPDATE (the U in CRUD)
# --------------------------------
# Change existing records:

# -- Mark a ticket as invalid (lost/stolen)
# UPDATE tickets 
# SET is_valid = false 
# WHERE ticket_id = 'T001';

# -- Update timestamp (correction)
# UPDATE scans 
# SET scan_time = '2025-09-30 10:05:00'
# WHERE id = 1;

# CONCEPT: DELETE (the D in CRUD)
# --------------------------------
# Remove records (use carefully!):

# DELETE FROM scans WHERE id = 1;

# Better approach - Soft Delete:
# ------------------------------
# Add a column to track "deleted" records without removing them:

# ALTER TABLE scans ADD COLUMN is_deleted BOOLEAN DEFAULT false;

# -- Instead of DELETE:
# UPDATE scans SET is_deleted = true WHERE id = 1;

# -- Queries now need to filter:
# SELECT * FROM scans WHERE is_deleted = false;

# 🚨 REAL SCENARIO: Lost ticket replacement
# ------------------------------------------
# Customer loses ticket T001. You issue replacement T001-R.
# How do you handle this?

# -- Invalidate old ticket
# UPDATE tickets SET is_valid = false WHERE ticket_id = 'T001';

# -- Create replacement
# INSERT INTO tickets (ticket_id, user_id, ticket_type, is_valid)
# VALUES ('T001-R', 'U123', 'General', true);
# """

# def find_people_still_inside_db():
#     """
#     DATABASE CHALLENGE 4: Handling edge cases
    
#     Modify your database to handle:
#     1. Lost tickets (replacements)
#     2. Suspicious activity flags
#     3. Manual overrides (security lets someone in)
    
#     Add these columns:
#     ALTER TABLE scans ADD COLUMN override_reason TEXT;
#     ALTER TABLE scans ADD COLUMN flagged_suspicious BOOLEAN DEFAULT false;
    
#     Now write a query that finds people inside, but also:
#     - Flags anyone who entered with an invalid ticket
#     - Shows if they had manual override
    
#     🤔 Real scenario: Fire alarm evacuation
#     Everyone leaves quickly without scanning out.
#     How would you handle this in the database?
#     """
    
#     # TODO: Implement enhanced query
#     pass


# # ===========================================================================
# # QUESTION 5: Detect Anomalies
# # ===========================================================================

# def detect_anomalies(stream):
#     """
#     Detect suspicious scanning patterns:
#     - People who exited without entering
#     - People who tried to enter while already in    
#     Args:
#         stream: Iterator/generator yielding event dictiona  
#     Returns:
#         dict with keys:
#             - exit_without_entry: set of user IDs who exited without entering
#             - duplicate_entries: set of user IDs who tried to enter while already in    
#     Expected output: {
#         'exit_without_entry': set(),
#         'duplicate_entries': {'U789'}

#     U789 entered at 10:02, then tried to enter again at 11:15 (duplicate entry attempt)
#     """
#     # people who have exited with out entering-
#     # - check for ticket_id that have 
#     pass


# """
# 📚 DATABASE LEARNING - QUESTION 5
# ==================================
# Advanced concepts: Triggers, Stored Procedures, and Audit Logs!

# CONCEPT: Triggers
# -----------------
# Automatically execute code when something happens:

# CREATE OR REPLACE FUNCTION check_duplicate_entry()
# RETURNS TRIGGER AS $$
# BEGIN
#     -- Check if person is already inside
#     IF EXISTS (
#         SELECT 1 FROM scans 
#         WHERE user_id = NEW.user_id 
#         AND scan_type = 'entry'
#         AND scan_time > (
#             SELECT MAX(scan_time) FROM scans 
#             WHERE user_id = NEW.user_id 
#             AND scan_type = 'exit'
#         )
#     ) THEN
#         -- Flag as suspicious but still insert
#         NEW.flagged_suspicious := true;
#     END IF;
#     RETURN NEW;
# END;
# $$ LANGUAGE plpgsql;

# CREATE TRIGGER check_entry 
# BEFORE INSERT ON scans
# FOR EACH ROW 
# WHEN (NEW.scan_type = 'entry')
# EXECUTE FUNCTION check_duplicate_entry();

# CONCEPT: Audit Logging
# -----------------------
# Track all changes for security:

# CREATE TABLE scan_audit (
#     audit_id SERIAL PRIMARY KEY,
#     scan_id INTEGER,
#     action VARCHAR(10),  -- INSERT, UPDATE, DELETE
#     changed_by VARCHAR(50),
#     changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     old_values JSONB,
#     new_values JSONB
# );

# 🚨 REAL SCENARIOS to detect:
# -----------------------------
# 1. Ticket sharing (same ticket, different times)
# 2. Passback fraud (enter, pass ticket back, someone else enters)
# 3. Tailgating (multiple people on one scan)
# 4. Extended stays (someone inside for suspiciously long)
# 5. Impossible travel (exit Gate A, immediately enter Gate C far away)
# """

# def detect_anomalies_db():
#     """
#     DATABASE CHALLENGE 5: Complex anomaly detection
    
#     Create queries to detect:
#     1. Duplicate entries (someone entering twice)
#     2. Exit without entry
#     3. Suspiciously quick re-entry (passback fraud)
#     4. People inside too long (> 8 hours)
    
#     Advanced: Create a stored procedure that runs all checks:
    
#     CREATE OR REPLACE FUNCTION run_anomaly_detection()
#     RETURNS TABLE(
#         anomaly_type VARCHAR,
#         user_id VARCHAR,
#         details TEXT
#     ) AS $$
#     BEGIN
#         -- Your detection logic here
#     END;
#     $$ LANGUAGE plpgsql;
    
#     🤔 Ultimate challenge: Real-time alerting
#     How would you alert security in real-time when anomalies are detected?
#     Research: PostgreSQL NOTIFY/LISTEN
#     """
    
#     # TODO: Implement comprehensive anomaly detection
#     pass


# # ===========================================================================
# # BONUS: Real-World Database Schema
# # ===========================================================================

# """
# 📚 COMPLETE VENUE MANAGEMENT SCHEMA
# ====================================
# Here's what a production system might look like:

# -- Core tables
# CREATE TABLE venues (
#     venue_id SERIAL PRIMARY KEY,
#     venue_name VARCHAR(100),
#     max_capacity INTEGER,
#     address TEXT
# );

# CREATE TABLE events (
#     event_id SERIAL PRIMARY KEY,
#     venue_id INTEGER REFERENCES venues(venue_id),
#     event_name VARCHAR(200),
#     event_date DATE,
#     doors_open TIME,
#     doors_close TIME
# );

# CREATE TABLE users (
#     user_id VARCHAR(10) PRIMARY KEY,
#     email VARCHAR(100) UNIQUE,
#     phone VARCHAR(20),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# CREATE TABLE tickets (
#     ticket_id VARCHAR(10) PRIMARY KEY,
#     event_id INTEGER REFERENCES events(event_id),
#     user_id VARCHAR(10) REFERENCES users(user_id),
#     ticket_type VARCHAR(20),
#     price DECIMAL(10,2),
#     purchase_date TIMESTAMP,
#     is_valid BOOLEAN DEFAULT true,
#     replacement_for VARCHAR(10) REFERENCES tickets(ticket_id)
# );

# -- Tracking tables
# CREATE TABLE scans (
#     scan_id SERIAL PRIMARY KEY,
#     ticket_id VARCHAR(10) REFERENCES tickets(ticket_id),
#     gate VARCHAR(1),
#     scan_type VARCHAR(5),
#     scan_time TIMESTAMP,
#     flagged_suspicious BOOLEAN DEFAULT false,
#     override_reason TEXT,
#     scanner_device_id VARCHAR(50)
# );

# -- Security tables  
# CREATE TABLE security_incidents (
#     incident_id SERIAL PRIMARY KEY,
#     scan_id INTEGER REFERENCES scans(scan_id),
#     incident_type VARCHAR(50),
#     description TEXT,
#     resolved BOOLEAN DEFAULT false,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Analytics views
# CREATE VIEW current_venue_status AS
# SELECT 
#     v.venue_id,
#     v.venue_name,
#     COUNT(DISTINCT s.user_id) as people_inside,
#     v.max_capacity,
#     (COUNT(DISTINCT s.user_id)::FLOAT / v.max_capacity) * 100 as occupancy_percent
# FROM venues v
# -- ... complex join logic
# GROUP BY v.venue_id, v.venue_name, v.max_capacity;

# Test your understanding:
# 1. How would you find all people at a specific event?
# 2. How would you check if venue is at capacity?
# 3. How would you track entry/exit patterns over time?
# 4. How would you implement a "one ticket, one entry per day" rule?
# 5. How would you handle group tickets (one ticket, multiple people)?
# """

# # ===========================================================================
# # TEST YOUR SOLUTIONS
# # ===========================================================================

# if __name__ == "__main__":
#     print("=" * 60)
#     print("EVENT OCCUPANCY TEST WITH DATABASE LEARNING")
#     print("=" * 60)
#     populate_database()
#     print('count_current_occupancy_db() result: ', count_current_occupancy_db())
#     print('get_occupancy_statistics() result: ', get_occupancy_statistics(mock_occupancy_stream()))
#     print('count_occupancy_by_gate() result: ', count_occupancy_by_gate(mock_occupancy_stream()))
#     print('find_people_still_inside() result: ', find_people_still_inside(mock_occupancy_stream()))
