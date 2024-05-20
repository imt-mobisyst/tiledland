import math

from .point import Point2

class Body2:

    # Initialization Destruction:
    def __init__( self, position_x= 0.0, position_y= 0.0, orientation= 0.0, radius= 1.0 ):
        self.position= Point2(position_x, position_y)
        self.radius= radius
        self.orientation= orientation
    
    # Accessor:
    def tuple(self) :
        return ( 
            self.position.x,
            self.position.y,
            self.orientation,
            self.radius
        )

    # Construction:
    def set( self, position_x= 0.0, position_y= 0.0, orientation_z= 0.0 ):
        self.px= position_x
        self.py= position_y
        self.oz= orientation_z
        return self

    def setPosition( self, position_x= 0.0, position_y= 0.0 ):
        self.position= Point2(position_x, position_y)
        return self

    def setOrientation( self, orientation_z= 0.0 ):
        self.orientation= orientation_z
        return self

    # Transformation:
    def move(self, translation, rotation, dtime=1.0 ):
        c= math.cos( self.orientation )
        s= math.sin( self.orientation )
        self.position.translate( Point2 (
            c*translation.x*dtime + s*translation.y*dtime,
            s*translation.x*dtime + -c*translation.y*dtime
        ))
        self.orientation+= rotation*dtime
        return self
        
    # Distance:
    def distance( self, aBody ):
        return self.position.distance( aBody.position )
    
    # Print:
    def __str__(self):
        return f"({self.px}, {self.py} | {self.oz})"
