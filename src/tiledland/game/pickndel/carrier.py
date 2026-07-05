"""
Test - MoveIt Robot Class
"""
from ...geometry import Point, Convex
from ...agent import Entity

mobileConvex= Convex().initRegular(0.4, 8)

class Carrier(Entity):
    def __init__( self, identifier=0, owner=1, position= Point(0.0, 0.0), mission= 0):
        super(Carrier, self).__init__( owner, mobileConvex, position )
        self._id= identifier
        self._mission= mission
        self._clockMove= 0
        self._tile= 0

    # Accessor:
    def tile(self):
        return self._tile
    
    def mission(self):
        return self._mission
    
    def setMission(self, iMission):
        self._mission= iMission

    def move(self):
        return self._clockMove

    def setMove(self, clockDir):
        self._clockMove= clockDir

    # Accessor: 
    def str(self, typeName= "Carrier"): 
        s= super(Carrier, self).str(typeName)
        s+= f" |{self._clockMove}, {self._mission}|"
        return s