import math

class Float2():
    # Initialization Destruction:
    def __init__( self, x= 0.0, y=0.0 ):
        self._x= x
        self._y= y

    # Accessors
    def x(self):
        return self._x
    
    def y(self):
        return self._y
    
    def tuple(self): 
        return (self._x, self._y)
    
    def list(self): 
        return [self._x, self._y]
    
    # Construction
    def setx(self, value):
        self._x= value
        return self
    
    def sety(self, value):
        self._y= value
        return self

    def set( self, x, y ):
        return self.setx(x).sety(y)
    
    def round(self, precision=0):
        self._x= round( self._x, precision )
        self._y= round( self._y, precision )
        return self
    
    def fromList( self, aList ):
        return self.setx( aList[0] ).sety( aList[1] )
    
    # Operator: 
    def __add__(self, another):
        return Float2( self._x+another._x,  self._y+another._y )

    def __sub__(self, another):
        return Float2( self._x-another._x,  self._y-another._y )

    #Comparison:
    def __eq__(self, another):
        return ( self.x() == another.x()
            and self.y() == another.y()
        )

    def distance(self, another):
        delta= another - self
        dx, dy = delta.tuple()
        return math.sqrt( dx*dx + dy*dy )
    
    # to str
    def str(self): 
        # Myself :
        s= f"({round(self.x(), 2)}, {round(self.y(), 2)})"
        return s
    
    def __str__(self): 
        return self.str()
