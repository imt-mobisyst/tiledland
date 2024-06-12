from . import AbsFrame
import pygame

class Frame(AbsFrame) :

    # Draw primitives:
    def drawScreenPoint( self, coord, color ):
        pygame.draw.circle( self._screen, color, coord, 5 )

    def drawScreenLine( self, coordA, coordB, color ):
        pygame.draw.line( self._screen, color, coordA, coordB, 2 )

    def drawScreenCircle( self, coord, radius, color ):
        pygame.draw.circle( self._screen, color, coord, radius, 2 )
