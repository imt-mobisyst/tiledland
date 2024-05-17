import math

class Pose2:

    # Initialization Destruction:
    def __init__( self, position_x= 0.0, position_y= 0.0, orientation_z= 0.0 ):
        self.px= position_x
        self.py= position_y
        self.oz= orientation_z
    
    # Accessor:
    def tuple(self) :
        return ( self.px, self.py, self.oz )
    
    def position(self) :
        return ( self.px, self.py )
    
    def orientation(self) :
        return ( self.oz )

    def lenghtSquare(self) : 
        return self.px*self.px + self.py*self.py
    
    def lenght(self) : 
        return math.sqrt( self.px*self.px + self.py*self.py )

    # Construction:
    def set( self, position_x= 0.0, position_y= 0.0, orientation_z= 0.0 ):
        self.px= position_x
        self.py= position_y
        self.oz= orientation_z
        return self

    def setPosition( self, position_x= 0.0, position_y= 0.0 ):
        self.px= position_x
        self.py= position_y
        return self

    def setOrientation( self, orientation_z= 0.0 ):
        self.oz= orientation_z
        return self

    # Transformation:
    def move(self, transform, dtime=1.0 ):
        c= math.cos( self.oz )
        s= math.sin( self.oz )
        self.oz+= transform.oz*dtime
        self.px= self.px + c*transform.px*dtime + s*transform.py*dtime
        self.py= self.py + s*transform.px*dtime + -c*transform.py*dtime
        return self
        
    # Distance:
    def distance( self, aPose ):
        sa= Pose2( aPose.px-self.px, aPose.py-self.py )
        return sa.lenght()
    
    def distanceSquare( self, aPose ):
        return Pose2( aPose.px-self.px, aPose.py-self.py ).lenghtSquare()
    
    # Print:
    def __str__(self):
        return f"({self.px}, {self.py} | {self.oz})"
