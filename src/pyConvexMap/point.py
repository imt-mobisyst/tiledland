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
    
    # Print:
    def __str__(self):
        return f"({self.x}, {self.y})"
