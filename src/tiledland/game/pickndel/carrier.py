"""
Test - MoveIt Robot Class
"""

import tiledland as tll
from tiledland.geometry import Point, Convex, Box

class Carrier(tll.Agent):

    def __init__(self, aBody= None, tabletop= None, mission= 0):
        super(Carrier, self).__init__( aBody, tabletop, Carrier.stateInitialize )
        #self._id= identifier
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

    # state machine:
    def stateInitialize(self):
        return Action( Action.WAIT )

    # Accessor: 
    def str(self, typeName= "Carrier"): 
        s= super(Carrier, self).str(typeName)
        s+= f" |{self._clockMove}, {self._mission}|"
        return s