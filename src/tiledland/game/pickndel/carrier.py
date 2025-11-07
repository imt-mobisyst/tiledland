"""
Test - MoveIt Robot Class
"""
from ... import Point, Shaped, Agent

mobileShape= Shaped().initializeRegular(0.4, 8)

class Carrier(Agent):
    def __init__( self, identifier=0, owner=1, position=  Point(0.0, 0.0), mission= 0):
        super().__init__(identifier, owner, position, mobileShape)
        self._mission= mission
        self._clockMove= 0

    # Accessor:     
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