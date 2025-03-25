"""
Test - MoveIt Robot Class
"""

from ... import Float2, Shape, agent

mobileShape= Shape().initializeRegular(0.4, 8)

class Robot(agent.Agent):
    def __init__( self, identifier=0, owner=1, position= Float2(0.0, 0.0), mission= 0):
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
    def str(self, typeName= "Robot"): 
        return super(Robot, self).str(typeName)