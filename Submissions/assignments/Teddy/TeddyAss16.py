#!/usr/bin/env python
# coding: utf-8

# In[1]:


def count_occurrences_nested(L, target):
    """
    L: a list that may contain other lists (nested)
    target: any value

    Returns the number of times target appears anywhere in L, including nested sublists.
    """
    count = 0
    for item in L:
        if isinstance(item, list):
            count += count_occurrences_nested(item, target)
        else:
            if item == target:
                count += 1
    return count

# Examples:
print(count_occurrences_nested([1, [2, [1, 3], 4], 1], 1))  # prints 3
print(count_occurrences_nested([[1,2],[3,[4,1]]], 4))       # prints 1
print(count_occurrences_nested([[],[],[]], 5))              # prints 0


# In[2]:


def hanoi_moves(n, source, target, spare):
    """
    n: int >= 1
    source, target, spare: string names of rods (e.g. "A", "B", "C")

    Returns a list of strings representing the sequence of moves needed
    to solve the Towers of Hanoi puzzle.
    """
    if n == 1:
        return [f"Move from {source} to {target}"]
    else:
        moves = []
        # Move n-1 disks from source to spare
        moves += hanoi_moves(n - 1, source, spare, target)
        # Move the nth disk from source to target
        moves.append(f"Move from {source} to {target}")
        # Move n-1 disks from spare to target
        moves += hanoi_moves(n - 1, spare, target, source)
        return moves

# Examples:
print(hanoi_moves(2, 'A', 'C', 'B'))
print(hanoi_moves(3, 'A', 'C', 'B'))


# In[ ]:




