import math
from .point import Point2

class Cell:

    # Initialization Destruction:
    def __init__( self, vertices= [Point2()]):
        self._vertices= vertices
        self._tags= [0 for i in range( len(vertices) )]
        self.updateCenter()

    # Construction:
    def makeConvex(self):
        return self._vertices
    
    def updateCenter(self):
        self._center= Point2(0.0, 0.0)

    # Accessors:
    def center(self):
        return self._center
    
    def vertices(self):
        return self._vertices