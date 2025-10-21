# SQL Cheat Sheet for Interview Prep

Quick reference for PostgreSQL commands needed for event occupancy system

## 🔍 Basic SELECT Queries

### Get all rows from a table

```sql
SELECT * FROM scans;
```

**Real-world:** "Show me all scan activity for debugging"

### Get specific columns

```sql
SELECT ticket_id, scan_type, scan_time FROM scans;
```

**Real-world:** "API response - only send necessary fields to reduce bandwidth"

### Filter with WHERE

```sql
SELECT * FROM scans WHERE scan_type = 'entry';
SELECT * FROM scans WHERE gate = 'A';
SELECT * FROM scans WHERE scan_time > '2025-09-30 11:00:00';
```

**Real-world scenarios:**

- "Show only entry scans for capacity calculation"
- "Which gate is Gate A processing?"
- "Get afternoon activity only"

### Multiple conditions

```sql
-- AND: both must be true
SELECT * FROM scans WHERE gate = 'A' AND scan_type = 'entry';

-- OR: either can be true
SELECT * FROM scans WHERE gate = 'A' OR gate = 'B';

-- NOT: exclude
SELECT * FROM scans WHERE scan_type != 'exit';
```

**Real-world scenarios:**

- **AND:** "VIP entries at Gate A only"
- **OR:** "Activity at main entrances (Gate A or B)"
- **NOT:** "All current entries (exclude exits for occupancy)"

---

## 📊 Counting & Aggregates

### COUNT - How many rows?

```sql
-- Count all rows
SELECT COUNT(*) FROM scans;

-- Count specific column (excludes NULLs)
SELECT COUNT(ticket_id) FROM scans;

-- Count unique values
SELECT COUNT(DISTINCT ticket_id) FROM scans;
```

**Real-world scenarios:**

- `COUNT(*)`: "Total scans today" (dashboard metric)
- `COUNT(ticket_id)`: "Valid scans" (exclude corrupted data with NULL ticket_ids)
- `COUNT(DISTINCT ticket_id)`: "Unique visitors" (not total scans)

### Other aggregates

```sql
-- Sum, average, min, max (work on numbers/dates)
SELECT MAX(scan_time) FROM scans;  -- Latest scan
SELECT MIN(scan_time) FROM scans;  -- Earliest scan
```

**Real-world scenarios:**

- `MAX(scan_time)`: "When was last activity?" (system health check)
- `MIN(scan_time)`: "Event start time"
- `SUM(ticket_price)`: "Total revenue today"
- `AVG(duration)`: "Average visit time"

### GROUP BY - Count per category

```sql
-- How many scans per gate?
SELECT gate, COUNT(*)
FROM scans
GROUP BY gate;

-- How many entries vs exits?
SELECT scan_type, COUNT(*)
FROM scans
GROUP BY scan_type;
```

**Real-world scenarios:**

- "Which gate is busiest?" (staff allocation)
- "Entry/exit ratio" (detect people still inside)
- "VIP vs General ticket usage" (GROUP BY ticket_type)
- "Hourly traffic pattern" (GROUP BY HOUR(scan_time))

---

## 🔗 JOINS - Combining Tables

### INNER JOIN - Only matching rows from both tables

```sql
-- Get scans with their ticket info
SELECT
    s.ticket_id,
    s.scan_type,
    t.ticket_type
FROM scans s
INNER JOIN tickets t ON s.ticket_id = t.ticket_id;
```

**Use when:** You only want data that exists in BOTH tables

**Real-world scenarios:**

- "Show scan activity WITH ticket type" (scans that have valid tickets)
- "Revenue from scanned tickets only" (exclude unused tickets)
- "Active users with purchases" (users table INNER JOIN orders)
- **Interview answer:** "I'd use INNER JOIN when I only care about scans that have matching ticket information, filtering out any orphaned records"

### LEFT JOIN - All from left table, matching from right

```sql
-- Get all tickets, include scan info if exists
SELECT
    t.ticket_id,
    t.ticket_type,
    s.scan_type
FROM tickets t
LEFT JOIN scans s ON t.ticket_id = s.ticket_id;
```

**Use when:** You want ALL records from the left table, even if no match in right
**Result:** Unmatched right table columns will be NULL

**Real-world scenarios:**

- "Show ALL tickets, even unused ones" (find no-shows: WHERE s.scan_type IS NULL)
- "All products, with sales if any" (inventory report)
- "All customers, with recent orders" (even customers who haven't ordered)
- **Interview answer:** "LEFT JOIN is perfect for 'show all X, optionally with Y' - like finding which tickets were never scanned"

### RIGHT JOIN - All from right table, matching from left

```sql
-- Same as LEFT JOIN but reversed
SELECT
    t.ticket_id,
    s.scan_type
FROM tickets t
RIGHT JOIN scans s ON t.ticket_id = s.ticket_id;
```

**Use when:** You want ALL records from the right table (rarely used - just flip tables and use LEFT JOIN instead!)

**Real-world scenarios:**

- Rarely used - just swap tables and use LEFT JOIN
- **Interview answer:** "RIGHT JOIN is uncommon - it's clearer to swap tables and use LEFT JOIN for readability"

### JOIN Summary

| JOIN Type | Returns                                                     | Event System Use Case           |
| --------- | ----------------------------------------------------------- | ------------------------------- |
| INNER     | Only rows that match in BOTH tables                         | "Scans with valid tickets"      |
| LEFT      | ALL rows from left + matching from right (NULL if no match) | "All tickets, show if scanned"  |
| RIGHT     | ALL rows from right + matching from left (NULL if no match) | "Swap tables, use LEFT instead" |

---

## 📝 Sorting & Limiting

### ORDER BY - Sort results

```sql
-- Ascending (A-Z, 0-9, oldest-newest)
SELECT * FROM scans ORDER BY scan_time;
SELECT * FROM scans ORDER BY scan_time ASC;  -- Same as above

-- Descending (Z-A, 9-0, newest-oldest)
SELECT * FROM scans ORDER BY scan_time DESC;

-- Multiple columns
SELECT * FROM scans ORDER BY gate ASC, scan_time DESC;
```

**Real-world scenarios:**

- `ORDER BY scan_time DESC`: "Most recent activity first" (activity feed)
- `ORDER BY scan_time ASC`: "Event timeline from start"
- `ORDER BY gate, scan_time`: "Scan history grouped by gate"
- **Interview tip:** "ORDER BY is crucial with DISTINCT ON - it determines which row you get per group"

### LIMIT - Get first N rows

```sql
-- Get 5 most recent scans
SELECT * FROM scans ORDER BY scan_time DESC LIMIT 5;
```

**Real-world scenarios:**

- "Last 10 scans" (recent activity widget)
- "Top 5 busiest gates" (with ORDER BY COUNT(\*) DESC)
- "First person to arrive" (ORDER BY scan_time ASC LIMIT 1)
- **Performance:** "Use LIMIT for pagination in APIs - don't load all rows"

---

## 🎯 Special PostgreSQL Features

### DISTINCT ON - Get first row per group

```sql
-- Get each person's most recent scan
SELECT DISTINCT ON(ticket_id)
    ticket_id,
    scan_type,
    scan_time
FROM scans
ORDER BY ticket_id, scan_time DESC;
```

**How it works:**

1. Groups by `ticket_id`
2. Within each group, sorts by `scan_time DESC`
3. Takes the first row from each group

**Real-world scenarios:**

- "Who is currently inside?" (last scan per person)
- "Latest price for each product" (last price update per product_id)
- "Most recent order per customer" (last order per customer_id)
- **Interview answer:** "DISTINCT ON is PostgreSQL-specific and perfect for 'give me the latest X for each Y' - like determining current occupancy from scan history"

### WITH (CTE) - Common Table Expression

```sql
-- Create a temporary named result
WITH recent_scans AS (
    SELECT * FROM scans WHERE scan_time > '2025-09-30 11:00:00'
)
SELECT COUNT(*) FROM recent_scans;
```

**Use when:** You want to break complex queries into readable steps

**Real-world scenarios:**

- "Calculate occupancy in multiple steps" (WITH last_scans AS... then filter)
- "Reuse a subquery multiple times" (calculate once, reference twice)
- "Make complex logic readable" (name each logical step)
- **Interview answer:** "CTEs make queries self-documenting - instead of nested subqueries, I can name each step like 'last_scans' or 'current_occupancy' which makes the logic clear"

---

## 🔢 Conditional Logic

### CASE - If/else in SQL

```sql
-- Label scans as "In" or "Out"
SELECT
    ticket_id,
    CASE
        WHEN scan_type = 'entry' THEN 'Coming In'
        WHEN scan_type = 'exit' THEN 'Going Out'
        ELSE 'Unknown'
    END as direction
FROM scans;
```

**Real-world scenarios:**

- "Convert entry/exit to +1/-1 for occupancy math" (CASE WHEN entry THEN 1 ELSE -1)
- "Categorize by time of day" (CASE WHEN hour < 12 THEN 'Morning'...)
- "Priority levels" (CASE WHEN ticket_type = 'VIP' THEN 1 ELSE 2)
- **Interview answer:** "CASE statements let me transform data in the query - like converting scan types to numeric values for calculations, or categorizing scans by time period"

### FILTER - Conditional counting

```sql
-- Count entries and exits in one query
SELECT
    COUNT(*) FILTER (WHERE scan_type = 'entry') as total_entries,
    COUNT(*) FILTER (WHERE scan_type = 'exit') as total_exits
FROM scans;
```

**Real-world scenarios:**

- "Multiple metrics in one query" (count entries AND exits together)
- "Conditional aggregates" (SUM(price) FILTER (WHERE ticket_type = 'VIP'))
- "Performance optimization" (one query instead of multiple)
- **Interview answer:** "FILTER is more readable than CASE for conditional aggregates - lets me count different categories in a single efficient query"

---

## 🗄️ Database Management

### Connect to database

```bash
psql occupancy_db_learning2
```

### List tables

```sql
\dt
```

### Describe table structure

```sql
\d scans
```

### Run SQL file

```bash
psql occupancy_db_learning2 < setup.sql
```

### Quit psql

```
\q
```

---

## 💡 Common Patterns for Event Systems

### Who is currently inside?

```sql
WITH last_scans AS (
    SELECT DISTINCT ON(ticket_id) ticket_id, scan_type
    FROM scans
    ORDER BY ticket_id, scan_time DESC
)
SELECT ticket_id
FROM last_scans
WHERE scan_type = 'entry';
```

### How many people per gate right now?

```sql
WITH last_scans AS (
    SELECT DISTINCT ON(s.ticket_id) s.ticket_id, s.gate, s.scan_type
    FROM scans s
    ORDER BY s.ticket_id, s.scan_time DESC
)
SELECT gate, COUNT(*)
FROM last_scans
WHERE scan_type = 'entry'
GROUP BY gate;
```

### VIP vs General occupancy

```sql
SELECT
    t.ticket_type,
    COUNT(*) as currently_inside
FROM (
    SELECT DISTINCT ON(ticket_id) ticket_id, scan_type
    FROM scans
    ORDER BY ticket_id, scan_time DESC
) last_scans
INNER JOIN tickets t ON last_scans.ticket_id = t.ticket_id
WHERE last_scans.scan_type = 'entry'
GROUP BY t.ticket_type;
```

---

## 🚀 Quick Tips

1. **Always ORDER BY with DISTINCT ON** - It determines which row you get
2. **Use aliases** - `FROM scans s` is cleaner than `FROM scans`
3. **Test JOINs incrementally** - Start with SELECT \*, then add conditions
4. **COUNT(\*) vs COUNT(column)** - COUNT(\*) includes NULLs, COUNT(column) doesn't
5. **LEFT JOIN for "all X, even without Y"** - Most common JOIN type in apps

---

## 📚 Interview Talking Points

**"Why use SQL instead of Python?"**

- SQL is optimized for data filtering and aggregation
- Database does the work (faster than loading into Python)
- Handles large datasets efficiently

**"When would you use a LEFT JOIN?"**

- "Show all tickets, including those never scanned"
- "List all products, with sales data if available"
- Any time you need "ALL from table A, optionally table B"

**"How do you handle duplicates?"**

- `DISTINCT` for unique values
- `DISTINCT ON` for "first row per group"
- `GROUP BY` for aggregations per group

**"What's a CTE (WITH clause)?"**

- Named subquery for readability
- Breaks complex logic into steps
- Can be referenced multiple times in same query
