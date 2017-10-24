#!/usr/bin/env python
__TODDLER_VERSION__="1.0.0"

import time
from pathFinder import pathFinder



# Hardware test code
class Toddler:
    def __init__(self,IO):
        print "Hey, I'm alive!"
        self.IO=IO
        

    # This is a callback that will be called repeatedly.
    # It has its dedicated thread so you can keep block it.
    def Control(self, OK):
        mission = pathFinder(self.IO, OK)
        mission.explore()
        #mission.pointAntenna(1.4,1.92,45)
        while OK():
        	continue



    def Vision(self, OK):
        while OK():
        	continue
