import math

class Point2:

    # Initialization Destruction:
    def __init__( self, x= 0.0, y= 0.0 ):
        self.x= x
        self.y= y
    
    # Accessor:
    def tuple(self) :
        return ( self.x, self.y )

    def lenghtSquare(self) : 
        return self.x*self.x + self.y*self.y
    
    def lenght(self) : 
        return math.sqrt( self.x*self.x + self.y*self.y )

    # Construction:
    def set( self, x= 0.0, y= 0.0 ):
        self.x= x
        self.y= y
        return self
    
    # Operators: 
    def __add__( self, another ):
        return Point2( self.x+another.x, self.y+another.y )

    # Scalaire: 
    def scale( self, aFloat ):
        self.x*= aFloat
        self.y*= aFloat
        return self
    
    def round( self, nb= 1 ):
        self.x= round( self.x, nb )
        self.y= round( self.y, nb )
        return self

    # Distance:
    def distance( self, aPose ):
        sa= Point2( aPose.x-self.x, aPose.y-self.y )
        return sa.lenght()
    
    def distanceSquare( self, aPose ):
        return Point2( aPose.x-self.x, aPose.y-self.y ).lenghtSquare()
    
    # Transform: 
    def translate( self, vector):
        self.x= self.x + vector.x
        self.y= self.y + vector.y
        return self
    
    # Comparison:
    def __eq__(self, another):
        return ( self.x == another.x and self.y == another.y )

    # Print:
    def __str__(self):
        return f"({self.x}, {self.y})"
