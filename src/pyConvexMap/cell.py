import math
from .pose import Pose2

class Cell:

    # Initialization Destruction:
    def __init__( self, points= []):
        self.borders= []
        self.links= []