from ...geometry import Point, Convex
from ...agent import Agent

mobileConvex= Convex().initRegular(0.4, 8)

class Bot(Agent):
    def __init__( self, identifier=0, owner=1, position= Point(0.0, 0.0), mission= 0):
        super().__init__(identifier, owner, mobileConvex, position)
        self._mission= mission
        self._clockMove= 0

