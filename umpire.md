# UMPIRE Framework for Technical Interviews

A structured approach for solving coding problems in technical interviews.

---

## **U - Understand**

- [ ] Clarify the problem statement
- [ ] Identify inputs and outputs
- [ ] Ask about edge cases
- [ ] Confirm assumptions
- [ ] Check constraints (time/space complexity expectations)

### Questions to ask:

- What are the input types and ranges?
- What should I return if input is empty/null?
- Are there any edge cases I should consider?
- What are the performance requirements?
- Can I modify the input?
- What about duplicate values?

---

## **M - Match**

- [ ] Identify the problem pattern (array, string, graph, tree, etc.)
- [ ] Link to similar problems you've solved
- [ ] Choose appropriate data structures
- [ ] Consider relevant algorithms

### Common patterns:

- **Arrays/Strings:** Two pointers, sliding window, prefix sum
- **Hash-based:** Hash maps, hash sets for O(1) lookups
- **Trees/Graphs:** BFS, DFS, recursion
- **Optimization:** Dynamic programming, greedy, backtracking
- **Searching:** Binary search, two pointers
- **Data structures:** Stack, queue, heap, trie

---

## **P - Plan**

- [ ] Write out steps in pseudocode or plain English
- [ ] Identify data structures needed
- [ ] Walk through with an example
- [ ] Verify plan handles edge cases
- [ ] Discuss time/space complexity before coding

### Tips:

- Get interviewer buy-in before coding!
- Use concrete examples to validate your approach
- Start with a brute force solution if needed, then optimize
- Draw diagrams if helpful

---

## **I - Implement**

- [ ] Write clean, readable code
- [ ] Use meaningful variable names
- [ ] Add comments for complex logic
- [ ] Handle edge cases
- [ ] Talk through your code as you write

### Best practices:

- Start with function signature and return statement
- Build incrementally - get something working first
- Use helper functions to keep code modular
- Don't go silent - explain what you're doing

---

## **R - Review**

- [ ] Walk through code with test case
- [ ] Check for bugs (off-by-one, null checks, etc.)
- [ ] Verify edge cases are handled
- [ ] Look for optimization opportunities
- [ ] Clean up any messy code

### Common bugs to check:

- Off-by-one errors
- Null/undefined checks
- Integer overflow
- Empty input handling
- Boundary conditions

---

## **E - Evaluate**

- [ ] Analyze time complexity
- [ ] Analyze space complexity
- [ ] Discuss trade-offs
- [ ] Suggest improvements or alternatives
- [ ] Consider real-world implications

### Discussion points:

- Can we do better than O(n�)?
- What if the input is very large?
- What if we need to handle concurrent requests?
- How would this scale in production?
- Are there memory constraints?

---

## Quick Reference

| Phase | Key Action                         | Time Allocation |
| ----- | ---------------------------------- | --------------- |
| **U** | Ask clarifying questions           | 5-10%           |
| **M** | Identify pattern & data structures | 5-10%           |
| **P** | Plan approach with example         | 15-20%          |
| **I** | Write code                         | 40-50%          |
| **R** | Test & debug                       | 10-15%          |
| **E** | Analyze complexity                 | 5-10%           |

---

## Example Walkthrough

### Problem: "Find two numbers in an array that sum to a target"

**U - Understand:**

- Input: array of integers, target integer
- Output: indices of two numbers or None
- Can I use the same element twice? No
- Is the array sorted? Not guaranteed
- Are there always two numbers? Not guaranteed

**M - Match:**

- Pattern: Array + lookup problem
- Data structure: Hash map for O(1) lookups
- Similar to: Two Sum pattern

**P - Plan:**

```
1. Create empty hash map
2. For each number in array:
   a. Calculate complement (target - number)
   b. If complement exists in hash map, return indices
   c. Otherwise, store current number and index in hash map
3. Return None if no pair found
```

**I - Implement:**

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None
```

**R - Review:**

- Test with [2, 7, 11, 15], target 9 � returns [0, 1] 
- Edge case: empty array � returns None 
- Edge case: no solution � returns None 

**E - Evaluate:**

- Time: O(n) - single pass through array
- Space: O(n) - hash map stores up to n elements
- Trade-off: Used extra space for better time complexity

---

## Tips for Success

1. **Always start with U-M-P** - Don't jump straight to coding
2. **Think out loud** - Interviewers want to hear your thought process
3. **Ask questions** - Better to clarify than make wrong assumptions
4. **Start simple** - Get a working solution, then optimize
5. **Test as you go** - Don't wait until the end to test
6. **Communicate trade-offs** - Show you understand different approaches
7. **Stay calm** - If stuck, go back to UMPIRE framework

---

Good luck! =�

total_occupancy - set same logica as Q1
'total_entries': 8,
'total_exits': 4
id use integer counters here

            'by_gate': {'A': 2, 'B': 2, 'C': 1},

i could import Counter here from the collections library - This will count how many occurences of each gatge would ooccur- 0(n) - and give me a hash like in the example - i couls also use defaultdict(int) here. This a more consie way of implemenitng the counteing pattern using .get(). These are all preferable to the [] pattern as These patterns will account for unknowns IE int has a defalt of 0 if there is no value for the key, so it wont throw an error.

for ticket type, ill need to make a look up from get_mock_tickets() as there are no ticket type infor available from the scan stream.
I'll use a dict comprehension to map ticket ids to ticket types. Then I can
