from .entity import Entity
from .geometry import radian, Point, Convex
from . import artist

_defaultOutline= Convex().initArrowTip(1.0)

class Mobile(Entity) :

    # Initialization/Destruction:
    def __init__(self,
                    outline= _defaultOutline, position=Point(), orientation=0.0,
                    color0x=0x000000, enclave=0, index=0 ):
        self._orientation= 0.0
        self._position= Point()
        super(Mobile, self).__init__(outline, position, orientation, color0x, enclave, index)

    def copy(self):
        cpy= type(self)(
            self._outline,
            self._position, self._orientation,
            self._brush.fill,
            self._enclave, self._index
        )
        cpy.setBrush( self.brush() )
        cpy.setName( self.name() )
        return cpy

    # Accessor: 
    def position(self):
        return self._position

    def orientation(self):
        return self._orientation

    def shape(self):
        shape= self._outline.copy()
        shape.rotate( self.orientation() )
        shape.translate( self.position() )
        return shape

    # Construction:
    def setOutline( self, aConvex):
        self._outline= aConvex
        return self
    
    def setPosition(self, position):
        self._position= position
        return self
     
    def setOrientation(self, angle):
        self._orientation= radian(angle)
        return self
    
    def setPose(self, position, angle):
        self.setPosition(position)
        self.setOrientation(angle)
        return self

    # Transformation : 
    def translate(self, vector2):
        self.setPosition(
            self.position()+vector2
        )
        return self

    def rotate(self, angle):
        self.setOrientation(
            self.orientation()+angle
        )
        return self
