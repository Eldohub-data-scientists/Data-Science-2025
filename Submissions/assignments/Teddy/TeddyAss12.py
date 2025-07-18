#!/usr/bin/env python
# coding: utf-8

# In[1]:


def subtract():
    a = int(input("Enter number: "))
    b = int(input("Enter number: "))
    print("Result:", a - b)
print(subtract())


# In[2]:


#Add assert to this code
def check_age(age):
    assert age > 0
    print("Age is okay.")
check_age(16)


# In[3]:


#Use raise to catch invalid input:
def is_even(n):
    try:
     return n % 2 == 0
    except NameError:
      return "Please enter a number"
print(is_even(11))


# In[ ]:




