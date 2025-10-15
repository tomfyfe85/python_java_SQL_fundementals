# # Event Occupancy Practice - Tech Test Simulation
# # =================================================

# # MOCK EVENT STREAM (simulates entry/exit scanning at an event)
# def mock_occupancy_stream():
#     """
#     Generator that yields entry and exit scan events.
#     Each event is a dictionary with:
#     - ticket_id: unique ticket identifier
#     - user_id: unique user identifier
#     - gate: gate where scan occurred (A, B, or C)
#     - timestamp: ISO format timestamp
#     - scan_type: 'entry' or 'exit'
#     """
#     events = [
#         {'ticket_id': 'T001', 'user_id': 'U123', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T002', 'user_id': 'U456', 'gate': 'A', 'timestamp': '2025-09-30T10:01:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T003', 'user_id': 'U789', 'gate': 'B', 'timestamp': '2025-09-30T10:02:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T004', 'user_id': 'U111', 'gate': 'C', 'timestamp': '2025-09-30T10:03:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T005', 'user_id': 'U222', 'gate': 'B', 'timestamp': '2025-09-30T10:05:00', 'scan_type': 'entry'},
#         # Now some people start leaving
#         {'ticket_id': 'T001', 'user_id': 'U123', 'gate': 'A', 'timestamp': '2025-09-30T11:00:00', 'scan_type': 'exit'},
#         {'ticket_id': 'T006', 'user_id': 'U333', 'gate': 'A', 'timestamp': '2025-09-30T11:05:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T002', 'user_id': 'U456', 'gate': 'A', 'timestamp': '2025-09-30T11:10:00', 'scan_type': 'exit'},
#         # Person tries to enter twice (already inside)
#         {'ticket_id': 'T003', 'user_id': 'U789', 'gate': 'B', 'timestamp': '2025-09-30T11:15:00', 'scan_type': 'entry'},
#         {'ticket_id': 'T007', 'user_id': 'U444', 'gate': 'C', 'timestamp': '2025-09-30T11:20:00', 'scan_type': 'entry'},
#         # More exits
#         {'ticket_id': 'T003', 'user_id': 'U789', 'gate': 'B', 'timestamp': '2025-09-30T12:00:00', 'scan_type': 'exit'},
#         {'ticket_id': 'T004', 'user_id': 'U111', 'gate': 'C', 'timestamp': '2025-09-30T12:05:00', 'scan_type': 'exit'},
#     ]
    
#     for event in events:
#         yield event


# # YOUR TASK: Implement these functions
# # =====================================

# # def count_current_occupancy(stream):
# #     """
# #    Count how many people are currently inside the venue.
    
# #     Args:
# #         stream: Iterator/generator yielding event dictionaries
    
# #     Returns:
# #         int: Number of people currently inside
    
# #     Expected output: 4 people still inside (U222, U333, U444, and U789 if counted only once)
# #     Note: U789 entered twice but should only count as 1 person inside
    
# #     After all events:
# #     - U123: entered then exited (NOT inside)
# #     - U456: entered then exited (NOT inside)  
# #     - U789: entered, tried to enter again, then exited (NOT inside)
# #     - U111: entered then exited (NOT inside)
# #     - U222: entered (INSIDE)
# #     - U333: entered (INSIDE)
# #     - U444: entered (INSIDE)
# #     Total inside: 3 people 
# #     """
# #     occupancy_tracker = {}

# #     for event in stream:
# #         scan_type = event['scan_type']
        
# #         occupancy_tracker[scan_type] = occupancy_tracker.get(scan_type, 0) + 1
# #     return sum(1 for status in occupancy_tracker.items() if status == 'entry' )


# # def get_occupancy_statistics(stream):
# #     """
# #     Get comprehensive occupancy statistics.
    
# #     Args:
# #         stream: Iterator/generator yielding event dictionaries
    
# #     Returns:
# #         dict with keys:
# #             - current_occupancy: number of people currently inside
# #             - total_entries: total entry scans processed
# #             - total_exits: total exit scans processed
# #             - max_occupancy: maximum number of people inside at any point
    
# #     Expected output: {
# #         'current_occupancy': 3,
# #         'total_entries': 8,
# #         'total_exits': 4,
# #         'max_occupancy': 5
# #     }
    
# #     Max occupancy timeline:
# #     - After event 1-5: 5 people inside (U123, U456, U789, U111, U222)
# #     - After U123 exits: 4 people inside
# #     - After U333 enters: 5 people inside again
# #     - Etc.
# #     Max reached: 5 people
# #     """
# #     # TODO: Implement this
# #     pass


# # def count_occupancy_by_gate(stream):
# #     """
# #     Track current occupancy at each gate separately.
# #     Note: People are tracked by the LAST gate they used.
    
# #     Args:
# #         stream: Iterator/generator yielding event dictionaries
    
# #     Returns:
# #         dict: Gate ID -> number of people currently at that gate
    
# #     Expected output: {'A': 1, 'B': 1, 'C': 1}
    
# #     Reasoning (tracking last gate used):
# #     - U222: last used gate B for entry (at gate B)
# #     - U333: last used gate A for entry (at gate A)
# #     - U444: last used gate C for entry (at gate C)
# #     """
# #     # TODO: Implement this
# #     pass


# # def find_people_still_inside(stream):
# #     """
# #     Return the IDs of people who are still inside the venue.
    
# #     Args:
# #         stream: Iterator/generator yielding event dictionaries
    
# #     Returns:
# #         set: User IDs of people currently inside
    
# #     Expected output: {'U222', 'U333', 'U444'}
# #     """
# #     # TODO: Implement this
# #     pass


# # def detect_anomalies(stream):
# #     """
# #     Detect suspicious scanning patterns:
# #     - People who exited without entering
# #     - People who tried to enter while already inside
    
# #     Args:
# #         stream: Iterator/generator yielding event dictionaries
    
# #     Returns:
# #         dict with keys:
# #             - exit_without_entry: set of user IDs who exited without entering
# #             - duplicate_entries: set of user IDs who tried to enter while already inside
    
# #     Expected output: {
# #         'exit_without_entry': set(),
# #         'duplicate_entries': {'U789'}
# #     }
    
# #     U789 entered at 10:02, then tried to enter again at 11:15 (duplicate entry attempt)
# #     """
# #     # TODO: Implement this
# #     pass

# print(count_current_occupancy(mock_occupancy_stream()))
# # TEST YOUR SOLUTIONS
# # ===================

# if __name__ == "__main__":
#     print("=" * 60)
#     print("Testing count_current_occupancy:")
#     print("=" * 60)
#     result1 = count_current_occupancy(mock_occupancy_stream())
#     print(f"Result: {result1}")
#     print(f"Expected: 3")
#     print()
    
# #     print("=" * 60)
# #     print("Testing get_occupancy_statistics:")
# #     print("=" * 60)
# #     result2 = get_occupancy_statistics(mock_occupancy_stream())
# #     print(f"Result: {result2}")
# #     print(f"Expected: {{'current_occupancy': 3, 'total_entries': 8, 'total_exits': 4, 'max_occupancy': 5}}")
# #     print()
    
# #     print("=" * 60)
# #     print("Testing count_occupancy_by_gate:")
# #     print("=" * 60)
# #     result3 = count_occupancy_by_gate(mock_occupancy_stream())
# #     print(f"Result: {result3}")
# #     print(f"Expected: {{'A': 1, 'B': 1, 'C': 1}}")
# #     print()
    
# #     print("=" * 60)
# #     print("Testing find_people_still_inside:")
# #     print("=" * 60)
# #     result4 = find_people_still_inside(mock_occupancy_stream())
# #     print(f"Result: {result4}")
# #     print(f"Expected: {{'U222', 'U333', 'U444'}}")
# #     print()
    
# #     print("=" * 60)
# #     print("Testing detect_anomalies:")
# #     print("=" * 60)
# #     result5 = detect_anomalies(mock_occupancy_stream())
# #     print(f"Result: {result5}")
# #     print(f"Expected: {{'exit_without_entry': set(), 'duplicate_entries': {{'U789'}}}}")
# #     print()


# # """
# # Design a system to track occupancy by gate. Choose between:

# # A) Track which gate each person entered from, decrement from entry gate on exit
# # B) Track entries/exits independently at each gate

# # Given events:
# # - U222 enters gate A
# # - U222 exits gate C

# # What should the result be and why?

# # Discuss: Data structures needed, time complexity, edge cases
# # """