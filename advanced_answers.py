    # current_tickets_inside = set()
    
    # for event in stream:
    #     scan_type = event['scan_type']
    #     ticket_id = event['ticket_id']
        
    #     if scan_type == 'entry':
    #         current_tickets_inside.add(ticket_id)
    #     else:
    #         current_tickets_inside.discard(ticket_id)
    # return len(current_tickets_inside)




    # target = datetime.fromisoformat(target_time)
    # tickets_inside = set()

    # for scan in stream:
    #     timestamp = datetime.fromisoformat(scan['timestamp'])
    #     ticket_id = scan['ticket_id']
    #     scan_type = scan['scan_type']

    #     if target >= timestamp:
    #         if scan_type == 'entry':
    #             tickets_inside.add(ticket_id)
    #         else:
    #             tickets_inside.discard(ticket_id)
    #     else:
    #          break
    # return len(tickets_inside)



    # for event in stream:
    #     ticket_id = event['ticket_id']
    #     gate = event['gate']
    #     scan_type = event['scan_type']

    #     if scan_type == 'entry' and ticket_id not in total_occupancy:
    #             total_occupancy.add(ticket_id)
    #             total_entries += 1
    #             by_gate[gate] +=1
    #             by_ticket_type[ticket_type_usage[ticket_id]] += 1

    #     elif scan_type == 'exit':
    #         total_occupancy.discard(ticket_id)
    #         total_exits +=1
    #         by_gate[gate] -=1
    #         by_ticket_type[ticket_type_usage[ticket_id]] -= 1


    # return {
    #         'total_occupancy': len(total_occupancy),
    #         'by_gate': dict(by_gate),
    #         'by_ticket_type': dict(by_ticket_type),
    #         'total_entries': total_entries,
    #         'total_exits': total_exits
    #     }
