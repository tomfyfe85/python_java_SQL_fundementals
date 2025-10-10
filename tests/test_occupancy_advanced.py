"""
Pytest tests for Advanced Event Occupancy System
=================================================
Run with: pytest test_occupancy_advanced.py -v
"""

import pytest
from occupancy_advanced import (
    count_current_occupancy,
    get_occupancy_at_time,
    track_occupancy_with_details,
    detect_scan_anomalies,
    manage_capacity_realtime,
    mock_scan_stream,
    get_mock_tickets,
    get_mock_users,
)


# ===========================================================================
# TEST QUESTION 1: Basic Occupancy
# ===========================================================================

def test_count_current_occupancy_basic():
    """Test basic occupancy counting."""
    result = count_current_occupancy(mock_scan_stream())
    assert result == 5, f"Expected 5 tickets inside, got {result}"


def test_count_current_occupancy_empty_stream():
    """Test with no events."""
    result = count_current_occupancy(iter([]))
    assert result == 0, "Empty stream should have 0 occupancy"


def test_count_current_occupancy_only_entries():
    """Test with only entry scans."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
        {'ticket_id': 'T003', 'gate': 'B', 'timestamp': '2025-09-30T10:02:00', 'scan_type': 'entry'},
    ]
    result = count_current_occupancy(iter(events))
    assert result == 3, "All 3 tickets should be inside"


def test_count_current_occupancy_entry_then_exit():
    """Test that exits are properly tracked."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T11:00:00', 'scan_type': 'exit'},
    ]
    result = count_current_occupancy(iter(events))
    assert result == 0, "Ticket that entered and exited should not be inside"


def test_count_current_occupancy_multiple_tickets_same_user():
    """Test that same user with 2 tickets counts as 2."""
    # U123 has T001 and T008
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T008', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
    ]
    result = count_current_occupancy(iter(events))
    assert result == 2, "Same user with 2 tickets should count as 2"


# ===========================================================================
# TEST QUESTION 2: Time-based Occupancy
# ===========================================================================

def test_occupancy_at_time_before_any_scans():
    """Test occupancy before any events."""
    result = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T09:00:00')
    assert result == 0, "No one inside before first scan"


def test_occupancy_at_time_after_first_entry():
    """Test occupancy right after first entry."""
    result = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T10:00:01')
    assert result == 1, "Should be 1 ticket inside"


def test_occupancy_at_time_mid_event():
    """Test occupancy at 11:30am."""
    result = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T11:30:00')
    assert result == 6, "Should be 6 tickets inside at 11:30am"


def test_occupancy_at_time_after_all_events():
    """Test occupancy after all events."""
    result = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T23:59:59')
    assert result == 5, "Should be 5 tickets inside at end of day"


def test_occupancy_at_time_exact_scan_time():
    """Test occupancy at exact time of a scan."""
    # T001 enters at exactly 10:00:00
    result = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T10:00:00')
    assert result == 1, "Should include scan at exact timestamp"


def test_occupancy_at_time_between_entry_and_exit():
    """Test occupancy between entry and exit of same ticket."""
    # T001 enters at 10:00, exits at 11:00
    result = get_occupancy_at_time(mock_scan_stream(), '2025-09-30T10:30:00')
    assert result >= 1, "T001 should still be inside at 10:30"


# ===========================================================================
# TEST QUESTION 3: Detailed Tracking
# ===========================================================================

def test_track_occupancy_total():
    """Test total occupancy calculation."""
    result = track_occupancy_with_details(mock_scan_stream())
    assert 'total_occupancy' in result, "Should include total_occupancy"
    assert result['total_occupancy'] == 5, f"Expected 5, got {result.get('total_occupancy')}"


def test_track_occupancy_by_gate():
    """Test occupancy breakdown by gate."""
    result = track_occupancy_with_details(mock_scan_stream())
    assert 'by_gate' in result, "Should include by_gate breakdown"

    by_gate = result['by_gate']
    assert isinstance(by_gate, dict), "by_gate should be a dictionary"

    # Check that all gates have counts
    total_by_gate = sum(by_gate.values())
    assert total_by_gate == result['total_occupancy'], "Gate totals should equal total occupancy"


def test_track_occupancy_by_ticket_type():
    """Test occupancy breakdown by ticket type."""
    result = track_occupancy_with_details(mock_scan_stream())
    assert 'by_ticket_type' in result, "Should include by_ticket_type breakdown"

    by_type = result['by_ticket_type']
    assert 'VIP' in by_type or 'General' in by_type, "Should have ticket types"

    total_by_type = sum(by_type.values())
    assert total_by_type == result['total_occupancy'], "Type totals should equal total occupancy"


def test_track_occupancy_entry_exit_counts():
    """Test total entry and exit counts."""
    result = track_occupancy_with_details(mock_scan_stream())
    assert 'total_entries' in result, "Should include total_entries"
    assert 'total_exits' in result, "Should include total_exits"

    # Count scans manually
    entries = sum(1 for e in mock_scan_stream() if e['scan_type'] == 'entry')
    exits = sum(1 for e in mock_scan_stream() if e['scan_type'] == 'exit')

    assert result['total_entries'] == entries, f"Expected {entries} entries"
    assert result['total_exits'] == exits, f"Expected {exits} exits"


def test_track_occupancy_validates_ticket_types():
    """Test that ticket types match expected values."""
    result = track_occupancy_with_details(mock_scan_stream())
    by_type = result.get('by_ticket_type', {})

    for ticket_type in by_type.keys():
        assert ticket_type in ['VIP', 'General'], f"Unexpected ticket type: {ticket_type}"


# ===========================================================================
# TEST QUESTION 4: Anomaly Detection
# ===========================================================================

def test_detect_anomalies_duplicate_entry():
    """Test detection of duplicate entries."""
    result = detect_scan_anomalies(mock_scan_stream())

    assert 'duplicate_entries' in result, "Should detect duplicate entries"
    assert 'T003' in result['duplicate_entries'], "T003 has duplicate entry at 11:15"


def test_detect_anomalies_exit_without_entry():
    """Test detection of exits without entry."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'exit'},
    ]
    result = detect_scan_anomalies(iter(events))

    assert 'exit_without_entry' in result, "Should detect exit without entry"
    assert 'T001' in result['exit_without_entry'], "T001 exits without entering"


def test_detect_anomalies_rapid_reentry():
    """Test detection of rapid re-entry (within 5 minutes)."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:10:00', 'scan_type': 'exit'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:12:00', 'scan_type': 'entry'},  # 2 min later
    ]
    result = detect_scan_anomalies(iter(events))

    assert 'rapid_reentry' in result, "Should detect rapid re-entry"
    assert 'T001' in result['rapid_reentry'], "T001 re-enters within 2 minutes"


def test_detect_anomalies_normal_reentry():
    """Test that normal re-entry (>5 minutes) is not flagged."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:10:00', 'scan_type': 'exit'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:20:00', 'scan_type': 'entry'},  # 10 min later
    ]
    result = detect_scan_anomalies(iter(events))

    assert 'T001' not in result.get('rapid_reentry', set()), "Normal re-entry should not be flagged"


def test_detect_anomalies_no_anomalies():
    """Test clean data with no anomalies."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T11:00:00', 'scan_type': 'exit'},
    ]
    result = detect_scan_anomalies(iter(events))

    assert len(result['duplicate_entries']) == 0, "Should have no duplicate entries"
    assert len(result['exit_without_entry']) == 0, "Should have no exits without entry"


def test_detect_anomalies_multiple_types():
    """Test detection of multiple anomaly types in same stream."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},  # Duplicate
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T10:02:00', 'scan_type': 'exit'},   # No entry
    ]
    result = detect_scan_anomalies(iter(events))

    assert 'T001' in result['duplicate_entries'], "Should detect T001 duplicate"
    assert 'T002' in result['exit_without_entry'], "Should detect T002 exit without entry"


# ===========================================================================
# TEST QUESTION 5: Capacity Management
# ===========================================================================

def test_capacity_management_basic():
    """Test basic capacity tracking."""
    result = manage_capacity_realtime(mock_scan_stream(), max_capacity=6)

    assert 'final_occupancy' in result, "Should include final_occupancy"
    assert 'times_at_capacity' in result, "Should track times at capacity"
    assert 'rejected_entries' in result, "Should track rejected entries"


def test_capacity_management_never_at_capacity():
    """Test when capacity is never reached."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
    ]
    result = manage_capacity_realtime(iter(events), max_capacity=10)

    assert result['times_at_capacity'] == 0, "Should never hit capacity"
    assert len(result['rejected_entries']) == 0, "No entries should be rejected"


def test_capacity_management_at_capacity():
    """Test rejection when at capacity."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
        {'ticket_id': 'T003', 'gate': 'B', 'timestamp': '2025-09-30T10:02:00', 'scan_type': 'entry'},  # Should be rejected
    ]
    result = manage_capacity_realtime(iter(events), max_capacity=2)

    assert result['times_at_capacity'] >= 1, "Should hit capacity"
    assert len(result['rejected_entries']) >= 1, "Should reject some entries"


def test_capacity_management_vip_override():
    """Test that VIP tickets can enter even at capacity."""
    # This is complex - VIP tickets should bypass capacity
    result = manage_capacity_realtime(mock_scan_stream(), max_capacity=4)

    # T001 and T005 are VIP tickets
    # Should have VIP override count if VIPs entered at capacity
    assert 'vip_override_count' in result, "Should track VIP overrides"


def test_capacity_management_would_be_occupancy():
    """Test would-be occupancy without limits."""
    result = manage_capacity_realtime(mock_scan_stream(), max_capacity=3)

    assert 'would_be_occupancy' in result, "Should track theoretical occupancy"
    # would_be is what occupancy would be if no limits
    assert result['would_be_occupancy'] >= result['final_occupancy'], \
        "Would-be occupancy should be >= actual occupancy"


def test_capacity_management_exit_frees_space():
    """Test that exits free up capacity."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T002', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:02:00', 'scan_type': 'exit'},
        {'ticket_id': 'T003', 'gate': 'B', 'timestamp': '2025-09-30T10:03:00', 'scan_type': 'entry'},  # Should succeed
    ]
    result = manage_capacity_realtime(iter(events), max_capacity=2)

    # T003 should NOT be rejected because T001 exited
    assert 'T003' not in result['rejected_entries'], "T003 should enter after T001 exits"


# ===========================================================================
# EDGE CASE TESTS
# ===========================================================================

def test_same_ticket_multiple_entries_exits():
    """Test ticket that enters and exits multiple times."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T11:00:00', 'scan_type': 'exit'},
        {'ticket_id': 'T001', 'gate': 'B', 'timestamp': '2025-09-30T12:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'B', 'timestamp': '2025-09-30T13:00:00', 'scan_type': 'exit'},
    ]
    result = count_current_occupancy(iter(events))
    assert result == 0, "Ticket should be outside after final exit"


def test_different_gates_same_ticket():
    """Test that gate changes are tracked correctly."""
    events = [
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        {'ticket_id': 'T001', 'gate': 'B', 'timestamp': '2025-09-30T11:00:00', 'scan_type': 'exit'},
    ]
    result = count_current_occupancy(iter(events))
    assert result == 0, "Exit from different gate should still work"


def test_mock_data_integrity():
    """Test that mock data is properly structured."""
    users = get_mock_users()
    tickets = get_mock_tickets()
    scans = list(mock_scan_stream())

    # Check users have required fields
    for user in users:
        assert 'user_id' in user
        assert 'email' in user

    # Check tickets have required fields
    for ticket in tickets:
        assert 'ticket_id' in ticket
        assert 'user_id' in ticket
        assert 'ticket_type' in ticket

    # Check scans have required fields
    for scan in scans:
        assert 'ticket_id' in scan
        assert 'gate' in scan
        assert 'timestamp' in scan
        assert 'scan_type' in scan


def test_user_with_multiple_tickets():
    """Test that U123 has multiple tickets in mock data."""
    tickets = get_mock_tickets()
    u123_tickets = [t for t in tickets if t['user_id'] == 'U123']

    assert len(u123_tickets) >= 2, "U123 should have at least 2 tickets (T001 and T008)"
    assert 'T001' in [t['ticket_id'] for t in u123_tickets]
    assert 'T008' in [t['ticket_id'] for t in u123_tickets]


# ===========================================================================
# PERFORMANCE TESTS (Discussion points for interview)
# ===========================================================================

def test_large_stream_performance():
    """
    Test with larger stream (not truly large, but demonstrates concept).

    Interview discussion: How would you handle millions of events?
    - Use generators (memory efficient)
    - Batch database writes
    - Use Redis for caching
    - Use database indexes
    """
    # Create 1000 entry/exit events
    large_events = []
    for i in range(500):
        large_events.append({
            'ticket_id': f'T{i:03d}',
            'gate': 'A',
            'timestamp': f'2025-09-30T10:{i % 60:02d}:00',
            'scan_type': 'entry'
        })
        large_events.append({
            'ticket_id': f'T{i:03d}',
            'gate': 'A',
            'timestamp': f'2025-09-30T11:{i % 60:02d}:00',
            'scan_type': 'exit'
        })

    result = count_current_occupancy(iter(large_events))
    # All should have exited
    assert result == 0, "All tickets should have exited"


# ===========================================================================
# RUN ALL TESTS
# ===========================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
