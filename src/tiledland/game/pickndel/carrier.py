"""
Test - MoveIt Robot Class
"""

import tiledland as tild
from tiledland.geometry import Point, Convex, Box

palette= [
    tild.Brush(0x603800, 0xffcd80, 4), # 10-Background
    tild.Brush(0x991100, 0xff6644, 4), # 11-Red
    tild.Brush(0x20770a, 0x70f050, 4), # 12-Green
    tild.Brush(0x1111aa, 0x6666ff, 4), # 13-Blue
    tild.Brush(0xdd550a, 0xfd9622, 4), # 14-Orange
    tild.Brush(0x8800aa, 0xdd77ff, 4), # 15-Purple
    tild.Brush(0x117799, 0x66ddee, 4), # 16-Cian
    tild.Brush(0xbbbbbb, 0xffffff, 4), # 17-White
    tild.Brush(0x555555, 0x888888, 4), # 18-Grey
    tild.Brush(0x000000, 0x444444, 4)  # 19-Black
]
paletteSize= len(palette)
carrierOutine= Convex().initArrowTip(0.6)

class Carrier(tild.Mobile):
    def __init__(self, owner=0, enclave= 0, index= 0, name= "Car", mission= 0):
        super(Carrier, self).__init__(carrierOutine, enclave= enclave, index= index)
        self._owner= owner
        self.setBrush(palette[owner%paletteSize])
        self.setName(name)
        self._mission= mission
        self._clockMove= 0
    
    def copy(self):
        cpy= type(self)(self._owner)
        super(Carrier, cpy).__init__(self._outline, self._position, self._orientation)
        cpy.setBrush( self.brush() )
        cpy.setSelector( self.enclave(), self.index() )
        cpy.setName( self.name() )
        cpy._mission= self._mission
        cpy._clockMove= self._clockMove
        return cpy
    
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

    # state machine:
    def stateInitialize(self):
        return Action( Action.WAIT )

    # Accessor: 
    def str(self): 
        s= super(Carrier, self).str()
        s+= f" |{self._clockMove}, {self._mission}|"
        return s