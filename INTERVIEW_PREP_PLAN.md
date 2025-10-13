# CrowdComms Junior API Developer - Interview Prep Plan

**Interview Date: Thursday, January 16th (Morning)**

---

## 📋 Overview

**Interview Format:**

- Python pairing session (raw Python, Google allowed)
- Task: Process a stream of check-ins/check-outs at a gate
- Goal: Track how many people are present
- Duration: Not too long (probably 45-60 minutes)

**Your Preparation:**

- 5.5 days of focused prep
- Files: `occupancy_advanced.py` (your practice tool)
- Focus: Python questions first, then database/FastAPI/Django discussion

---

## 📅 5.5-Day Study Plan

### **Day 1 - Saturday (TODAY)**

**Goal: Implement Python Questions 2 & 3**

**Morning (2-3 hours):**

- [ ] Implement Question 2: `get_occupancy_at_time()` (line 688)

  - Parse timestamps with `datetime.fromisoformat()`
  - Only process events before/at target time
  - Expected output: 6 people at 11:30am

- [ ] Test Q2 thoroughly
  - Run: `python occupancy_advanced.py`
  - Verify output matches expected

**Afternoon (2-3 hours):**

- [ ] Implement Question 3: `track_occupancy_with_details()` (line 937)

  - Pre-build ticket lookup dictionary
  - Use `defaultdict(int)` for counting
  - Track by gate and ticket type

- [ ] Test Q3 thoroughly

**Evening (1 hour):**

- [ ] Practice explaining Q1, Q2, Q3 OUT LOUD
  - Why use `set()` vs `list()`?
  - Why parse timestamps?
  - Why use `defaultdict`?

---

### **Day 2 - Sunday**

**Goal: Implement Python Questions 4 & 5**

**Morning (2-3 hours):**

- [ ] Implement Question 4: `detect_scan_anomalies()` (line 1220)

  - Detect duplicate entries
  - Detect exit without entry
  - Detect rapid re-entry (< 5 minutes)
  - Use `timedelta` for time calculations

- [ ] Test Q4 - should find T003 as duplicate

**Afternoon (2-3 hours):**

- [ ] Implement Question 5: `manage_capacity_realtime()` (line 1553)
  - Enforce max capacity
  - Allow VIP overrides
  - Track rejected entries
  - Track theoretical vs actual occupancy

**Evening (1 hour):**

- [ ] Run ALL tests and fix any bugs
- [ ] Practice explaining Q4 and Q5

---

### **Day 3 - Monday**

**Goal: Master explanations and edge cases**

**Morning (2 hours):**

- [ ] Re-implement Question 1 from scratch (no looking!)
- [ ] Re-implement Question 2 from scratch
- [ ] Time yourself - should take < 15 min for Q1, < 20 min for Q2

**Afternoon (2 hours):**

- [ ] Practice explaining EACH question out loud
- [ ] Record yourself or explain to a friend
- [ ] Focus on WHY you made each decision

**Key phrases to practice:**

- "I'm using a set because membership testing is O(1)..."
- "I'll parse timestamps so I can compare them properly..."
- "defaultdict avoids the need to check if keys exist..."
- "I'll use discard() instead of remove() to avoid errors..."

**Evening (1 hour):**

- [ ] Write down edge cases for each question:
  - What if events out of order?
  - What if duplicate entry?
  - What if exit without entry?
  - What if at capacity?

---

### **Day 4 - Tuesday**

**Goal: SQL and Database Concepts**

**Morning (2-3 hours):**

- [ ] Review database schema (lines 79-136)
- [ ] Understand the 3-table design (users, tickets, scans)
- [ ] Study current occupancy query (lines 575-586)

**Key SQL Concepts to Understand:**

1. **JOINs** (lines 326-518)

   - INNER JOIN vs LEFT JOIN
   - When to use each
   - Example: Join scans → tickets → users

2. **Aggregation** (lines 970-1078)

   - COUNT, SUM, AVG
   - GROUP BY and HAVING
   - Example: Count by ticket type

3. **Window Functions** (lines 1250-1378)

   - LAG/LEAD for comparing rows
   - DISTINCT ON (PostgreSQL specific)
   - Example: Find last scan per ticket

4. **Indexes**
   - Why: `CREATE INDEX idx_scans_ticket_time ON scans(ticket_id, scan_time)`
   - Performance improvement

**Afternoon (2 hours):**

- [ ] Practice explaining how you'd persist the stream
- [ ] Be able to explain the occupancy query in plain English

**Discussion Prep - Practice Answering:**

1. "How would you persist this stream to a database?"

   - Answer: INSERT each scan event as it arrives into `scans` table

2. "What indexes would you add?"

   - Answer: `scans(ticket_id, scan_time)` for finding entry/exit pairs
   - Answer: `scans(scan_time)` for time-range queries

3. "How would you get current occupancy from the database?"

   - Answer: Find each ticket's last scan, count where last scan = 'entry'

4. "How would you join with user data?"
   - Answer: scans → tickets (by ticket_id) → users (by user_id)

---

### **Day 5 - Wednesday**

**Goal: FastAPI, Django, and Full Mock Interview**

**Morning (2-3 hours):**

- [ ] Create `api_example.py` with basic FastAPI endpoints
- [ ] Install: `pip install fastapi uvicorn`
- [ ] Run: `uvicorn api_example:app --reload`
- [ ] Test endpoints at http://localhost:8000/docs

**FastAPI Example Endpoints:**

```python
POST   /api/scans              # Record entry/exit
GET    /api/occupancy/current  # Get current count
GET    /api/occupancy/by-gate  # Breakdown by gate
GET    /api/tickets/{id}/scans # Scan history
```

**Key FastAPI Concepts:**

1. **Request validation** with Pydantic models
2. **Path parameters**: `@app.get("/tickets/{ticket_id}")`
3. **Query parameters**: `?gate=A&ticket_type=VIP`
4. **Async/await** (FastAPI is async by default)
5. **Dependency injection** for database connections

**Django Discussion Prep (1 hour):**

- [ ] Review Django vs FastAPI differences
- [ ] Understand Django REST Framework basics
- [ ] Be ready to discuss when you'd use each

**Afternoon (2-3 hours) - FULL MOCK INTERVIEW:**

**Simulate the pairing session:**

1. **Warm-up (5 min)**

   - Open empty Python file
   - Implement Q1 from scratch

2. **Core task (15 min)**

   - "Now show me occupancy at a specific time"
   - Implement Q2
   - Talk through your logic as you code

3. **Edge cases (10 min)**

   - "What if someone scans twice?"
   - Add duplicate detection

4. **Discussion (15 min)**
   - "How would you persist this?"
   - "Design an API endpoint"
   - "What if 1 million events?"

**Practice answering these:**

- [ ] "Why use a set instead of a list?"
- [ ] "How would you handle out-of-order events?"
- [ ] "What if the stream is infinite?" (need database!)
- [ ] "How would you optimize for performance?"

**Evening (1 hour):**

- [ ] Review any weak areas
- [ ] Practice Q1 and Q2 one more time

---

### **Day 6 - Thursday Morning (INTERVIEW DAY)**

**Before the Interview (30 min):**

**Quick Review Checklist:**

- [ ] Can you implement Q1 in 10 minutes? (Practice once)
- [ ] Can you explain why you use `set()`?
- [ ] Can you describe the database schema?
- [ ] Can you sketch a FastAPI endpoint?
- [ ] Can you explain Django vs FastAPI?

**Don't over-study!** You're ready.

**What to Have Open:**

- Empty Python file (for coding)
- Your `occupancy_advanced.py` (for reference if needed)
- Google (they said you can use it!)

**Mindset:**

- Talk through your thinking
- Ask clarifying questions
- It's okay to Google syntax
- Focus on problem-solving, not perfection

---

## 🎯 Key Success Criteria

**By Wednesday night, you should be able to:**

✅ Implement Q1-3 from memory
✅ Explain why you chose each data structure
✅ Describe one SQL query for current occupancy
✅ Sketch a FastAPI endpoint for recording scans
✅ Explain Django vs FastAPI use cases
✅ Handle "what if" edge case questions

---

## 📚 Quick Reference - Data Structures

**Sets** (Q1, Q2, Q3)

- Fast membership testing: `ticket_id in inside` is O(1)
- No duplicates automatically
- Use for tracking who's currently inside

**defaultdict** (Q3, Q5)

```python
from collections import defaultdict
counts = defaultdict(int)  # Auto-creates keys with value 0
counts['A'] += 1  # No need to check if 'A' exists
```

**datetime** (Q2, Q4)

```python
from datetime import datetime, timedelta
dt = datetime.fromisoformat('2025-09-30T10:00:00')
if dt < target_time:  # Compare times
    ...
diff = time2 - time1  # timedelta object
if diff < timedelta(minutes=5):  # Compare durations
    ...
```

**Dictionary Comprehension** (Q3)

```python
# Build lookup from list of dicts
tickets = {t['ticket_id']: t for t in get_mock_tickets()}
ticket_type = tickets['T001']['ticket_type']  # Fast lookup!
```

---

## 🗣️ Interview Discussion Points

### Python Topics

- **Why sets over lists?** O(1) membership testing vs O(n)
- **Why defaultdict?** Cleaner code, avoids KeyError
- **Why parse timestamps?** Proper comparison, calculations
- **Edge cases:** Duplicate entry, exit without entry, out of order

### Database Topics

- **Schema design:** 3 tables (users, tickets, scans) with foreign keys
- **Current occupancy query:** Find last scan per ticket, count entries
- **Indexes:** On (ticket_id, scan_time) for performance
- **JOINs:** Connect scans → tickets → users for rich data

### FastAPI Topics

- **Async/await:** Non-blocking I/O for better performance
- **Pydantic validation:** Automatic request body validation
- **Path parameters:** `/tickets/{ticket_id}`
- **Query parameters:** `?gate=A&type=VIP`
- **Real-time:** WebSockets for live dashboard updates
- **Caching:** Redis for frequently-accessed data (current occupancy)

### Django Topics

**When to use Django vs FastAPI:**

**Use Django when:**

- Building a full web application with admin panel
- Need built-in authentication/authorization
- Want Django ORM for database interactions
- Building traditional multi-page web apps
- Team already knows Django

**Use FastAPI when:**

- Building pure APIs (microservices)
- Need high performance (async)
- Want automatic API documentation (Swagger/OpenAPI)
- Modern async/await patterns
- Type hints and Pydantic validation

**Django REST Framework (DRF) Overview:**

```python
# Django Model
class Scan(models.Model):
    ticket_id = models.CharField(max_length=10)
    scan_type = models.CharField(max_length=5)
    scan_time = models.DateTimeField()

# DRF Serializer
class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = ['ticket_id', 'scan_type', 'scan_time']

# DRF ViewSet
class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
```

**Key Django Concepts:**

- **ORM:** `Scan.objects.filter(scan_type='entry').count()`
- **Migrations:** Automatic database schema management
- **Admin Panel:** Free admin interface for data management
- **Middleware:** Request/response processing
- **Signals:** Event-driven actions (e.g., send email after scan)

**CrowdComms likely uses:**

- Django for main platform (web app with admin)
- FastAPI for high-performance microservices
- Django REST Framework for standard CRUD APIs

**Be ready to say:**
"I'd use Django for the full event management platform with admin panel, but FastAPI for real-time scan processing where we need async performance. Django's ORM and admin would make it easy to manage events, users, and tickets, while FastAPI would handle the high-volume scan stream efficiently."

### System Design Topics

- **Streaming:** Process events one at a time (memory efficient)
- **Database:** Persist events for historical queries
- **Caching:** Redis for current occupancy (reduce DB load)
- **Scaling:** Message queue (Celery) for async processing
- **Monitoring:** Alert at 90% capacity

---

## ❓ Questions to Ask THEM

**Technical:**

1. "How do you handle real-time updates to client dashboards?" (WebSockets? Polling?)
2. "What's your caching strategy for high-traffic events?" (Redis?)
3. "How do you handle time zones for international events?"
4. "Do you use Django for the main platform and FastAPI for microservices?"
5. "How do you monitor for anomalies in production?"

**Team/Culture:**

1. "What does a typical sprint look like?"
2. "How do junior developers get mentored?"
3. "What's the most interesting technical challenge you've solved recently?"
4. "What technologies is the team excited about?"

---

## 🚀 Day-Of Reminders

**During the Pairing Session:**

- ✅ Talk through your thinking process
- ✅ Ask clarifying questions ("Should I handle duplicate entries?")
- ✅ Start simple, then add complexity
- ✅ Test your code as you go
- ✅ It's okay to Google syntax
- ✅ If stuck, say "Let me think through the approach..."

**Don't worry about:**

- ❌ Perfect code style
- ❌ Memorizing every syntax detail
- ❌ Getting it right first time
- ❌ Implementing everything - they want to see your process

---

## 📞 Final Confidence Boost

**You have:**

- ✅ 5.5 days to prepare
- ✅ An excellent practice file with 5 progressive questions
- ✅ Real-world context (event venues)
- ✅ Clear learning materials

**The interviewer wants to see:**

- Your problem-solving process
- How you think through edge cases
- Your communication skills
- Your ability to learn and adapt

**You got this! 💪**

Remember: It's a **pairing session**, not a test. They want to work WITH you, not watch you struggle. Ask questions, think out loud, and show your curiosity.

Good luck! 🚀

Yes! You CAN use Django and FastAPI together
This is actually a common pattern for modern applications. Here's how:
Architecture Pattern: Hybrid Approach
┌─────────────────────────────────────┐
│ Django Application (Port 8000) │
│ │
│ • Event management dashboard │
│ • Admin panel │
│ • User authentication │
│ • Traditional web pages │
│ • Django ORM for database │
└─────────────────────────────────────┘
│
│ Shared PostgreSQL Database
│
┌─────────────────────────────────────┐
│ FastAPI Microservice (Port 8001) │
│ │
│ • Real-time scan processing API │
│ • High-volume ticket validation │
│ • WebSocket for live updates │
│ • Async processing │
└─────────────────────────────────────┘
Real-World Example for CrowdComms:
Django handles:
Event creation/management (admin panel)
User registration and authentication
Ticket sales and payment processing
Reporting dashboards
Slow, heavy operations
FastAPI handles:
Real-time scan validation (thousands per minute)
Live occupancy updates (WebSockets)
Fast read-only queries
Async external API calls
How they communicate:
Option 1: Shared Database

# Django - manages the data

class Scan(models.Model):
ticket_id = models.CharField(max_length=10)
scan_time = models.DateTimeField()

# FastAPI - reads the same data

from sqlalchemy import select
async def get_scans():
result = await db.execute(select(scan_table))
return result.all()
Option 2: REST API calls between them

# FastAPI calls Django endpoint

import httpx

@app.post("/validate-ticket")
async def validate_ticket(ticket_id: str):
async with httpx.AsyncClient() as client:
response = await client.get(
f"http://django-service:8000/api/tickets/{ticket_id}"
)
return response.json()
Option 3: Message Queue (Redis/RabbitMQ/Celery)

# Django publishes event

from django.core.signals import post_save
from redis import Redis

@receiver(post_save, sender=Ticket)
def notify_fastapi(sender, instance, \*\*kwargs):
redis.publish('ticket_created', instance.ticket_id)

# FastAPI subscribes

import redis
r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe('ticket_created')
When CrowdComms Would Use This:

# Scenario: Large conference with 10,000 attendees

# Django Application (django-app.crowdcomms.com)

# - Event organizer creates event

# - Sets capacity limits, VIP lists

# - Manages ticket sales

# - Generates reports

# FastAPI Service (api.crowdcomms.com)

# - Handles scan requests from gates

# - 100+ scans per second during entry rush

# - Real-time occupancy via WebSocket

# - Fast async validation

Example Setup:

# Django settings.py

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'event_venue',
}
}

# FastAPI main.py - same database!

from sqlalchemy import create_engine
engine = create_engine('postgresql://user@localhost/event_venue')
For Your Interview:
Be ready to say:
"I'd use Django for the main platform since it has a great admin panel for event management, and the ORM makes it easy to handle complex business logic. But for the high-volume scan processing, I'd use FastAPI as a microservice because it's async and can handle thousands of requests per second. They'd share the PostgreSQL database, and FastAPI would use WebSockets to push real-time updates to the dashboard."
They'll be impressed you understand:
When to use each framework
Microservices architecture
Shared database patterns
Real-time communication
Want me to help you with anything else in the prep plan, or shall we start implementing Question 2? 🚀
Great question! Yes, absolutely! Using Django and FastAPI together is a common and powerful pattern.
How Django + FastAPI Work Together
Common Architecture Pattern:
┌─────────────────────────────────────┐
│ Django App (Port 8000) │
│ • Admin panel │
│ • User management │
│ • Event CRUD operations │
│ • Django ORM │
│ • Template rendering │
└──────────────┬──────────────────────┘
│
│ Shared PostgreSQL
│
┌──────────────┴──────────────────────┐
│ FastAPI Microservice (Port 8001) │
│ • High-performance APIs │
│ • Real-time scan processing │
│ • WebSocket connections │
│ • Async operations │
└─────────────────────────────────────┘
Real Example for CrowdComms Event Platform:
Django handles:
Event creation/editing (admin interface)
User authentication and profiles
Ticket sales and payment processing
Complex business logic
Reports and analytics dashboards
FastAPI handles:
Real-time ticket scanning (1000s per second)
Live occupancy WebSocket updates
Fast read-only API endpoints
External integrations (async)
Three Ways They Can Work Together:

1. Shared Database (Most Common)
   Both frameworks connect to the same PostgreSQL database:

# Django - manages the schema

# models.py

class Scan(models.Model):
ticket_id = models.CharField(max_length=10)
scan_type = models.CharField(max_length=5)
scan_time = models.DateTimeField()

# FastAPI - reads/writes same tables

# main.py

from sqlalchemy import create_engine, Table
engine = create_engine('postgresql://user@localhost/event_venue')

@app.post("/api/scans")
async def create_scan(scan_data: ScanRequest): # Insert into same 'scans' table Django uses
await db.execute(scans_table.insert().values(...)) 2. HTTP API Calls Between Services

# FastAPI calls Django to validate ticket

import httpx

@app.post("/scan")
async def process_scan(ticket_id: str): # Call Django API to check if ticket is valid
async with httpx.AsyncClient() as client:
response = await client.get(
f"http://django-service:8000/api/tickets/{ticket_id}/validate"
)

    if response.json()['is_valid']:
        # Process the scan
        return {"status": "accepted"}

3. Message Queue (Redis/Celery/RabbitMQ)

# Django publishes events

from redis import Redis
redis_client = Redis()

def create_ticket(ticket_data):
ticket = Ticket.objects.create(\*\*ticket_data) # Notify FastAPI service
redis_client.publish('ticket_created', ticket.id)

# FastAPI subscribes and reacts

import redis
r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe('ticket_created')

for message in pubsub.listen(): # Cache the new ticket for fast lookup
await cache_ticket(message['data'])
Practical CrowdComms Use Case:
Event: Tech Conference with 5,000 attendees

┌─────────────────────────────────────┐
│ Django (event-admin.crowdcomms.com) │
│ │
│ • Event organizer logs in │
│ • Sets event details, capacity │
│ • Manages ticket types (VIP, GA) │
│ • Views analytics reports │
│ • Uses Django Admin panel │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ FastAPI (api.crowdcomms.com) │
│ │
│ • Gate scanners send POST requests │
│ • 50 scans/second during entry rush │
│ • WebSocket pushes live occupancy │
│ • Async validation checks │
│ • Returns result in < 100ms │
└─────────────────────────────────────┘
Why This Works Well:
Django strengths:
✅ Amazing admin panel (free UI for data management)
✅ Mature ORM with migrations
✅ Built-in authentication
✅ Great for traditional web pages
✅ Huge ecosystem
FastAPI strengths:
✅ Async/await for high concurrency
✅ Automatic API docs (Swagger)
✅ Type hints + Pydantic validation
✅ WebSocket support
✅ Fast performance (similar to Node.js/Go)
For Your Interview, Say This:
"I'd use Django for the main event management platform because the admin panel makes it easy to manage events, users, and tickets. But for the real-time scan processing, I'd create a FastAPI microservice because it's async and can handle thousands of scans per second efficiently. Both would connect to the same PostgreSQL database, and I'd use Redis for caching current occupancy. FastAPI would push real-time updates via WebSockets to the Django-rendered dashboard."
Simple Example:

# Django creates the event and tickets

# Admin panel at: localhost:8000/admin

# FastAPI handles scans

# API docs at: localhost:8001/docs

# Both use same database:

# PostgreSQL 'event_venue'

# - users table

# - tickets table

# - scans table

Alternative: Django + DRF vs FastAPI
Some companies choose:
Django + Django REST Framework for everything (simpler, single framework)
Django + FastAPI hybrid when they need async performance
CrowdComms likely uses both because:
Existing Django codebase (main platform)
Adding FastAPI microservices for performance-critical features
This is actually a great interview discussion point! It shows you understand:
When to use each tool
Microservices architecture
Performance considerations
Real-world tradeoffs
Want me to add this to your prep plan file?
Great question! This is about how real-world hardware integrates with your API. Let me explain how gate scanners actually send data:
🚪 Real-World Gate Scanner Architecture
Physical Setup at Event Venue:
┌─────────────────────────────────┐
│ Physical Gate/Turnstile │
│ │
│ ┌──────────────────┐ │
│ │ Ticket Scanner │ │
│ │ (Barcode/QR/NFC)│ │
│ │ │ │
│ │ [Raspberry Pi/ │ │
│ │ IoT Device] │ │
│ │ │ │
│ │ WiFi/4G Module │ │
│ └────────┬─────────┘ │
└───────────┼──────────────────────┘
│
│ HTTP/HTTPS Request
▼
┌───────────────────┐
│ Your API Server │
│ (FastAPI/Django) │
└───────────────────┘
How It Actually Works:
Option 1: Scanner Sends HTTP POST (Most Common)

# What happens at the gate:

# 1. Attendee scans ticket (barcode/QR code)

# 2. Scanner device reads ticket_id: "T001"

# 3. Scanner sends HTTP POST to your API

# The scanner device code (simplified):

import requests
from datetime import datetime

def on_ticket_scanned(ticket_id, scan_type):
"""This runs on the scanner device when ticket is scanned"""

    payload = {
        "ticket_id": ticket_id,
        "gate": "A",  # Hardcoded in scanner config
        "scan_type": scan_type,  # 'entry' or 'exit'
        "timestamp": datetime.utcnow().isoformat(),
        "device_id": "GATE_A_SCANNER_001"  # Device identifier
    }

    # Send to your API
    response = requests.post(
        "https://api.crowdcomms.com/api/scans",
        json=payload,
        headers={"Authorization": "Bearer GATE_TOKEN_XYZ"},
        timeout=5
    )

    if response.status_code == 200:
        # Turn light green, open turnstile
        open_gate()
    else:
        # Turn light red, show error
        reject_entry(response.json()['error'])

Your API receives it:
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class ScanEvent(BaseModel):
ticket_id: str
gate: str
scan_type: str
timestamp: datetime
device_id: str

@app.post("/api/scans")
async def receive_scan(event: ScanEvent):
"""
This endpoint receives scans from physical gate devices.
It's called every time someone scans their ticket.
"""

    # 1. Validate ticket exists and is valid
    ticket = await db.get_ticket(event.ticket_id)
    if not ticket or not ticket.is_valid:
        raise HTTPException(status_code=403, detail="Invalid ticket")

    # 2. Check capacity (for entries)
    if event.scan_type == 'entry':
        current_occupancy = await get_current_occupancy()
        if current_occupancy >= MAX_CAPACITY:
            if ticket.ticket_type != 'VIP':
                raise HTTPException(status_code=403, detail="Venue at capacity")

    # 3. Save to database
    await db.insert_scan(event)

    # 4. Update Redis cache for real-time dashboard
    await redis.set('current_occupancy', current_occupancy + 1)

    # 5. Send WebSocket update to dashboard
    await websocket_manager.broadcast({
        "occupancy": current_occupancy + 1,
        "gate": event.gate
    })

    # 6. Return success to scanner (opens gate)
    return {
        "status": "accepted",
        "message": "Welcome!",
        "current_occupancy": current_occupancy + 1
    }

Option 2: Event Stream / Message Queue (High Volume)
For large venues with many gates:

# Gate scanner publishes to message queue instead of HTTP

import paho.mqtt.client as mqtt

def on_ticket_scanned(ticket_id):
"""Scanner publishes to MQTT topic"""
client = mqtt.Client()
client.connect("mqtt.crowdcomms.com", 1883)

    message = {
        "ticket_id": ticket_id,
        "gate": "A",
        "timestamp": datetime.utcnow().isoformat()
    }

    client.publish("scans/gate_a", json.dumps(message))

# Your backend subscribes and processes

import asyncio
from aiomqtt import Client

async def listen_for_scans():
"""Your server listens to all gate topics"""
async with Client("mqtt.crowdcomms.com") as client:
await client.subscribe("scans/#")
async for message in client.messages:
scan = json.loads(message.payload)
await process_scan(scan)
Option 3: Batch Upload (Offline Mode)
If scanners lose internet connection:

# Scanner stores scans locally

local_queue = []

def on_ticket_scanned(ticket_id):
scan = {
"ticket_id": ticket_id,
"timestamp": datetime.utcnow().isoformat()
}
local_queue.append(scan)

    # Try to sync every 10 scans or 30 seconds
    if len(local_queue) >= 10:
        try:
            sync_to_server()
        except ConnectionError:
            pass  # Will retry later

def sync_to_server():
"""Bulk upload when connection restored"""
requests.post(
"https://api.crowdcomms.com/api/scans/batch",
json={"scans": local_queue}
)
local_queue.clear()
How Your Mock Stream Simulates This:
def mock_scan_stream():
"""
This simulates what would happen if you played back
a day's worth of scans from the database.

    In production:
    - Real scans come via HTTP POST from gate devices
    - Get saved to database immediately
    - This function would read them back for analysis
    """
    events = [
        # Each event represents one ticket scan at a gate
        {'ticket_id': 'T001', 'gate': 'A', 'timestamp': '2025-09-30T10:00:00', 'scan_type': 'entry'},
        # ... more events
    ]
    for event in events:
        yield event  # Yields one at a time (like streaming)

Real-World Flow:
10:00:00 - Alice scans ticket T001 at Gate A
↓
[Scanner Device]
↓
POST /api/scans
↓
[Your FastAPI]
↓
Insert into database
↓
Update Redis cache
↓
Dashboard shows: 1 person inside

10:01:00 - Bob scans ticket T002 at Gate A
↓
(repeat flow)
↓
Dashboard shows: 2 people inside
For Your Interview:
If they ask: "How would the scanner send data?" Answer:
"The gate scanner devices would send HTTP POST requests to our API whenever a ticket is scanned. The scanner would include the ticket ID, gate ID, timestamp, and scan type. For high-volume events, we might use a message queue like MQTT or RabbitMQ so scanners can publish events and our backend processes them asynchronously. We'd also implement offline mode where scanners store scans locally and batch upload when connection is restored."
Mock Stream vs Real Stream:

# MOCK (for testing/interview)

def mock_scan_stream():
events = [...] # Hardcoded list
for event in events:
yield event

# REAL (production)

@app.post("/api/scans")
async def receive_scan_from_gate(scan: ScanEvent): # Validate, process, save
await process_scan(scan)
return {"status": "ok"}

# REAL (reading back from database)

async def get_scans_for_analysis(event_date):
scans = await db.query(
"SELECT \* FROM scans WHERE DATE(scan_time) = %s ORDER BY scan_time",
[event_date]
)
for scan in scans:
yield scan # Stream from database
The mock stream in your practice file is simulating what a replay of the day's scans would look like! 🎯

Excellent point! That's a very real-world consideration. Let me show you:
JSON → Dict Conversion
Scenario 1: Receiving JSON from an API
import json

# Raw JSON string from HTTP request body

json_string = '{"ticket_id": "T001", "gate": "A", "scan_type": "entry"}'

# Parse JSON string to Python dict

event = json.loads(json_string)

print(event)

# Result: {'ticket_id': 'T001', 'gate': 'A', 'scan_type': 'entry'}

# Now you can use it

ticket_id = event['ticket_id'] # 'T001'
Scenario 2: FastAPI automatically parses JSON
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ScanEvent(BaseModel):
ticket_id: str
gate: str
scan_type: str

@app.post("/api/scans")
async def receive_scan(event: ScanEvent):
"""FastAPI automatically converts JSON → Pydantic model"""

    # Convert Pydantic model to dict if needed
    event_dict = event.dict()  # or event.model_dump() in newer versions

    # Now it's a regular Python dict
    process_scan(event_dict)

    return {"status": "ok"}

Scenario 3: Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

@api_view(['POST'])
def receive_scan(request):
"""Django automatically parses JSON to request.data dict"""

    # request.data is already a dict!
    event = request.data
    # {'ticket_id': 'T001', 'gate': 'A', 'scan_type': 'entry'}

    process_scan(event)

    return Response({"status": "ok"})

Your Function Can Handle Both:
def get_occupancy_at_time(stream, target_time: str) -> int:
"""
Works with: - Python dicts (like your mock data) - JSON that's been parsed to dicts - Generator of either
"""
target = datetime.fromisoformat(target_time)
tickets_inside = set()

    for scan in stream:
        # scan is a dict - doesn't matter if it came from JSON or Python
        timestamp = datetime.fromisoformat(scan['timestamp'])
        ticket_id = scan['ticket_id']
        scan_type = scan['scan_type']

        # ... rest of logic

Common JSON Operations:
import json

# 1. Parse JSON string → dict

json_string = '{"ticket_id": "T001"}'
event = json.loads(json_string)

# 2. Convert dict → JSON string

event_dict = {"ticket_id": "T001"}
json_string = json.dumps(event_dict)

# 3. Read JSON from file

with open('events.json', 'r') as f:
events = json.load(f) # Returns list of dicts

# 4. Write dict to JSON file

events = [{"ticket_id": "T001"}, {"ticket_id": "T002"}]
with open('events.json', 'w') as f:
json.dump(events, f, indent=2)
Real-World Stream from API:
import requests

def stream_scans_from_api():
"""Fetch scans from an API and yield them"""
response = requests.get('https://api.crowdcomms.com/scans')

    # API returns JSON array
    events = response.json()  # Parses JSON → list of dicts

    for event in events:
        yield event  # Each event is a dict

# Use it exactly like your mock stream

occupancy = count_current_occupancy(stream_scans_from_api())
Interview Discussion Point:
If they ask: "How would you handle JSON input?" Say:
"In production, the gate scanners would send JSON in the HTTP POST body. FastAPI automatically parses that JSON to a Pydantic model, which I can convert to a dict with .dict(). My function works with dicts, so whether the data comes from a mock generator or parsed JSON doesn't matter - the structure is the same."
Quick Comparison:
Source What You Get How to Use
Your mock Python dict Use directly ✅
JSON string String json.loads() → dict
FastAPI Pydantic model .dict() → dict
Django REST Dict (auto-parsed) Use directly ✅
API response JSON .json() → dict
Key takeaway: Once it's a Python dict, your code doesn't care where it came from! 🎯 Want to tackle Question 3 now? You're doing great! 💪
