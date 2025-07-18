#!/usr/bin/env python
# coding: utf-8

# In[1]:


def sort_names():
    # Enter a list of names separated by commas
    names = input("Enter a list of names : ")

    # Split the input into a list
    name_list = [name.strip() for name in names.split(",")]

    # Remove duplicates
    unique_names = set(name_list)

    # Sort the names
    sorted_names = sorted(unique_names)

    # Display the result
    print("Sorted names:", sorted_names)

# Run the function
sort_names()


# In[2]:


L1 = ['sun'] 
L2 = L1
L1 = ['moon']
# L2 points to the same memory allocation of L1 which contains the string "sun"
# When the value of L1 changes to "moon", L2 still points to the memory allocation of the "sun"
print(L2) 


# In[3]:


# Create the list of 10 names with duplicates
random_names = ["Beatrice", "Gladys","Collins", "Loice", "Janet", "Collins", "Eunice", "Joyce", "Loice", "Gladys"]

# Remove the duplicates
unique_names = set(random_names)

# Sort the names
sorted_names = sorted(unique_names)

# Print the results
print("Sorted names:", sorted_names)


# In[ ]:




