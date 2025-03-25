"""
Test - MoveIt Robot Class
"""

from ... import Float2, Shape, body

mobileShape= Shape().initializeRegular(0.4, 8)

class Mobile(body.Body):
    def __init__( self, identifier=0, position= Float2(0.0, 0.0), owner=1, mission= 0):
        super().__init__(identifier, position, mobileShape, owner)
        self._mission= mission
        self._clockMove= 0

    # Accessor: 
    def owner(self):
        return self._owner
    
    def mission(self):
        return self._mission
    
    def setMission(self, iMission):
        self._mission= iMission

    def move(self):
        return self._clockMove

    def setMove(self, clockDir):
        self._clockMove= clockDir
