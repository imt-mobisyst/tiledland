import math
from .geometry import radian, Point, Convex
from . import artist

#_defaultOutline= Convex().initRegular(1.0, 3)
_defaultOutline= Convex().initSquare(1.0)

class Entity :
    # Initialization / Destruction:
    def __init__(self,
                    outline= _defaultOutline, position=Point(), orientation=0.0,
                    color0x=0x000000, enclave=0, index=0 ):
        assert type(outline) == Convex
        self.setOutline(outline)
        self.rotate(orientation)
        self.translate(position)
        self.setColor(color0x)
        self.setSelector(enclave, index)
        self.setName( type(self).__name__ )

    def copy(self):
        cpy= type(self)(self._outline)
        cpy.setBrush( self.brush() )
        cpy.setSelector( self.enclave(), self.index() )
        cpy.setName( self.name() )
        return cpy
    
    # Accessor: 
    def name(self):
        return self._name
    
    def outline(self):
        return self._outline

    def shape(self):
        return self._outline
    
    def position(self):
        return self.shape().center()

    def orientation(self):
        return 0.0

    def enclave(self):
        return self._enclave

    def index(self):
        return self._index
    
    def selector(self):
        return (self._enclave, self._index)

    def color(self):
        return self._brush.fill

    # Convex accessor : 
    def box(self):
        return self.shape().box()
    
    def radius(self):
        return self.outline().radius()
    
    # Construction: 
    def setName(self, aName):
        self._name= aName
        return self
    
    def setOutline( self, aConvex):
        self._outline= aConvex.copy()
        return self
    
    def setShape(self, aConvex, position, orientation=0.0 ):
        self.setOutline(aConvex)
        self.setPose(position, orientation)

    def setPosition(self, position):
        self._outline.setCenter(position)
        return self
     
    def setCoordinates(self, x, y):
        return self.setPosition( Point(x, y) )

    def setOrientation(self, angle):
        return self.setPose( self.position(), angle )
    
    def setPose(self, position, angle):
        angle= radian(angle)
        toZero= self.position().negative()
        self._outline.translate( toZero )
        if angle != 0.0 :
            self._outline.rotate( angle )
        self.setPosition( position )
        return self
    
    def setEnclave(self, e):
        self._enclave= e
        return self
    
    def setIndex(self, i):
        self._index= i
        return self

    def setSelector(self, enclave, index):
        self.setEnclave(enclave)
        self.setIndex(index)
        return self

    #transform:
    def rotate(self, angle):
        self._outline.rotate( angle )
        return self
    
    def translate(self, v2):
        self._outline.translate(v2)
        return self

    # Comparison :
    def centerDistance(self, another):
        return self.position().distance( another.position() )

    def shapeDistance(self, another):
        return self.shape().distance( another.shape() )

    # Artist:
    def brush(self):
        return self._brush

    def setBrush(self, aBrush):
        self._brush= aBrush
        return self
        
    def setColors( self, fillColor, strokeColor, width= 4 ):
        self.setBrush( artist.Brush(fillColor, strokeColor, width) )
        return self

    def setColor( self, fillColor, width= 4 ):
        self._brush= artist.Brush( fillColor, artist.color.lightest(fillColor, 0.5), width)
        return self
    
    def renderOn( self, artist ):
        artist.fillConvex( self.shape(), self.brush() )
        return self

    def writeOn( self, artist, text ):
        minx, miny= self.box().leftFloor().asTuple()
        cx, cy= self.position().asTuple()
        x= minx + 0.1 * (cx - minx)
        artist.write( x, cy, text, self.brush() )
        return self
    
    # str:
    def str(self): 
        return self.strIdentity() + f" {self.box()}"
    
    def strIdentity(self):
        return f"{self._name} {self.enclave()}-{self.index()}"

    def __str__(self):
        return self.str()
