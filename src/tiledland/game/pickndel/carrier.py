"""
Test - MoveIt Robot Class
"""

import tiledland as tild
from tiledland.geometry import Point, Convex, Box

class Carrier(tild.Entity):
    defaultShape= Convex().initArrowTip(0.6)

    def __init__(self, group=0, location= 0, index= 0, name= "Car", mission= 0):
        super(Carrier, self).__init__( 
            group= group,
            location=0, index= 0,
            name= name
        )
        #self._id= identifier
        self._mission= mission
        self._clockMove= 0
    
    def copy(self):
        cpy= type(self)()
        tild.Entity.__init__( cpy,
            self._group,
            self._refShape,
            self._position, self._theta,
            self._brush,
            self._local, self._index,
            self._name
        )
        cpy._mission= self._mission
        cpy._clockMove= self._clockMove
        return cpy
    
    # Accessor:
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
    def str(self): 
        s= super(Carrier, self).str()
        s+= f" |{self._clockMove}, {self._mission}|"
        return s