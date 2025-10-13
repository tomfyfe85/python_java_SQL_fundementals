#!/usr/bin/env python3
"""
Quick test script for your database queries in occupancy_advanced.py
Run this to check if your SQL solutions are correct!
"""

from occupancy_advanced import (
    count_current_occupancy_db,
    get_occupancy_at_time_db,
    track_occupancy_with_details_db,
    detect_scan_anomalies_db,
    manage_capacity_realtime_db,
    count_current_occupancy,
    get_occupancy_at_time,
    track_occupancy_with_details,
    detect_scan_anomalies,
    manage_capacity_realtime,
    mock_scan_stream
)

print("=" * 70)
print("DATABASE QUERY TESTS")
print("=" * 70)

# TEST 1: Current occupancy
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

# TEST 2: Occupancy at specific time
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

# TEST 3: Detailed occupancy breakdown
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

# TEST 4: Anomaly detection
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

# TEST 5: Capacity management
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
print("DONE! Check results above")
print("=" * 70)
