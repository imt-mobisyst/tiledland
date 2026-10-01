from .entity import SimpleEnt
from .geometry import radian, Point, Convex
from . import artist

_defaultOutline= Convex().initArrowTip(1.0)

class Mobile(SimpleEnt) :

    # Initialization / Destruction:
    def __init__(self,
                outline= _defaultOutline.copy(),
                color=0x000000, enclave=0, index=0):
        super(Mobile, self).__init__(outline, color, enclave, index)
        self._position= Point(0.0, 0.0)
        self._orientation= 0.0

    def copy(self):
        cpy= type(self)(
            self._group,
            self._refShape,
            self._position, self._theta,
            self._brush,
            self._local, self._index,
            self._name
        )
        cpy.setPose( self.position(), self.orientation() )

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
