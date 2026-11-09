import math
from .geometry import radian, Point, Convex
from .shaped import AbsShaped

class Unit(AbsShaped) :
    # Initialization / Destruction:
    def __init__(self,
            outline= None, position= Point(), orientation=0.0,
            category=0, owner=0, index=0, name="Unit"):
        super().__init__(category, owner, index, name)
        if outline is None :
            outline= Convex().initSquare(1.0)
        self._outline= outline
        self._position= position.copy()
        self._orientation= radian(orientation)
        
    def copy(self):
        cpy= type(self)(
            self._outline, self._position, self._orientation, 
            self._category, self._owner, self._index, self._name
        )
        return cpy

    # Shape Accessor: 
    def position(self):
        return self._position

    def orientation(self):
        return self._orientation

    def radius(self):
        return self._outline.radius()
    
    def shape(self):
        shape= self._outline.copy()
        shape.rotate( self.orientation() )
        shape.translate( self.position() )
        return shape
    
    # Accessor: 
    def outline(self):
        return self._outline
    
    # Construction:
    def setOutline( self, aConvex):
        self._outline= aConvex
        return self

    def setPosition(self, p):
        self._position= p
        return self

    def setOrientation(self, orientation):
        self._orientation= radian(orientation)
        return self

    def setPose(self, position, angle):
        self.setPosition( position )
        self.setOrientation( angle )
        return self

    #transform:
    def rotate(self, angle):
        self.setOrientation( self._orientation+angle )
        return self
    
    def translate(self, vector):
        self._position+= vector
        return self
