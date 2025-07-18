#!/usr/bin/env python
# coding: utf-8

# In[1]:


def recur_factorial(n):
    """
    n: int >= 0

    Returns the factorial of n using recursion.
    Hint: Base case is when n == 0. In the recursive case, return n * factorial(n-1).
    """
    if n == 0:
        return 1
    else:
        return n * recur_factorial(n - 1)

# Examples:
print(recur_factorial(0))
print(recur_factorial(5)) 
print(recur_factorial(7)) 


# In[6]:


def is_palindrome_recur(s):
    """
    s: string

    Returns True if s is a palindrome using recursion, False otherwise.
    Hint: A string is a palindrome if the first and last characters are equal
    and the substring in between is also a palindrome.
    """
    # Base case: if the string has 0 or 1 characters, it's a palindrome
    if len(s) <= 1:
        return True
    # If first and last characters don't match, it's not a palindrome
    if s[0] != s[-1]:
        return False
    # Recursive case: check the substring without the first and last characters
    return is_palindrome_recur(s[1:-1])

# Examples:
print(is_palindrome_recur("racecar"))  
print(is_palindrome_recur("hello")) 
print(is_palindrome_recur("madam")) 


# In[ ]:




