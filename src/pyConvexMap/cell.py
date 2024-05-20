import math
from .point import Point2

class Cell:

    # Initialization Destruction:
    def __init__( self, points= []):
        self.borders= []
        self.links= []