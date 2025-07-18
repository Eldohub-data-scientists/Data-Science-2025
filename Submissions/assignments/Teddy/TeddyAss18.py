#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Book:
    def __init__(self, title, author, year, copies_available):
        self.title = title
        self.author = author
        self.year = year
        self.copies_available = copies_available

    def borrow(self):
        if self.copies_available > 0:
            self.copies_available -= 1
        else:
            print("Not available.")

    def return_book(self):
        self.copies_available += 1

    def is_same_book(self, other):
        return self.title.lower() == other.title.lower() and self.author.lower() == other.author.lower()

b1 = Book("Python Basics", "Dennis Omboga", 2024, 3)
b2 = Book("Python Basics", "Dennis Omboga", 2024, 2)

b1.borrow() 
print(b1.copies_available)

b1.borrow()         
print(b1.copies_available)

b1.return_book()
print(b1.copies_available)

print(b1.is_same_book(b2))


# In[2]:


class Fraction:
    def __init__(self, num, denom):
        self.num = num
        self.denom = denom

    def simplify(self):
        gcd = self._find_gcd(self.num, self.denom)
        self.num //= gcd
        self.denom //= gcd
        return self

    def _find_gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def __add__(self, other):
        new_num = self.num * other.denom + other.num * self.denom
        new_denom = self.denom * other.denom
        return Fraction(new_num, new_denom).simplify()

    def __eq__(self, other):
        a = Fraction(self.num, self.denom).simplify()
        b = Fraction(other.num, other.denom).simplify()
        return a.num == b.num and a.denom == b.denom

    def __str__(self):
        return f"{self.num}/{self.denom}"

f1 = Fraction(1, 2)
f2 = Fraction(1, 4)
f3 = f1 + f2

print(f3)   
print(f1 == f2)
print(f1 == Fraction(2, 4))


# In[ ]:




