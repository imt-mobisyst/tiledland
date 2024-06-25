import math, shapely

class Joint:
    # Initialization Destruction:
    def __init__( self, tileA= None, tileB= None, segementA= 0, segementB= 0 ):
        self._tileA= tileA
        self._segementA= segementA
        self._tileB= tileB
        self._segementB= segementB
        self._tag= 0
