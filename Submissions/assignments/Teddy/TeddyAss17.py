#!/usr/bin/env python
# coding: utf-8

# In[4]:


class Box:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def get_volume(self):
        return self.length * self.width * self.height

    def is_cube(self):
        return self.length == self.width == self.height

    def bigger(self, other):
        if self.get_volume() >= other.get_volume():
            return self
        else:
            return other

box1 = Box(2, 4, 8)
box2 = Box(4, 4, 4)

print("Box 1 volume:", box1.get_volume())
print("Box 2 volume:", box2.get_volume())
print("Box 2 is cube:", box2.is_cube())

bigger_box = box1.bigger(box2)
print("Bigger box volume:", bigger_box.get_volume())


# In[9]:


class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration

    def is_long(self):
        return self.duration > 300

    def same_artist(self, other):
        return self.artist == other.artist

    def longer_song(self, other):
        if self.duration >= other.duration:
            return self
        else:
            return other

song1 = Song("Mask Off", "Future", 316)
song2 = Song("Distance", "Lost Frequencies", 248)
song3 = Song("Home", "Lost Frequencies", 107)

print(song1.is_long())
print(song2.same_artist(song3))
print(song3.same_artist(song1))

longer = song1.longer_song(song2)
print(f"The longer song is: {longer.title} by {longer.artist}")


# In[ ]:




