#import math, shapely

class Map:
    # Initialization Destruction:
    def __init__(self):
        self._tiles= []
        self._adjacences= []

    def setTags( self, tags ):
        self._tags= tags
    
    # Accessors:
    def size(self):
        return len(self._tiles)
    

