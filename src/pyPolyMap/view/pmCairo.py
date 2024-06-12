
from . import AbsFrame, colorPanel
import math, cairo, pygame

class Frame(AbsFrame) :

    # Draw primitives:
    def initBackground(self, color= colorPanel.background):
        width, height= self._screen.get_width(), self._screen.get_height()
        self._dwidth= width/2
        self._dheight= height/2
        self._surface= cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self._surface)
        ctx.move_to(0, 0)
        ctx.line_to(0, height)
        ctx.line_to(width, height)
        ctx.line_to(width, 0)
        ctx.line_to(0, 0)
        r, g, b= color
        ctx.set_source_rgba(r/255, g/255, b/255, 1.0)
        ctx.fill_preserve()
        ctx.set_line_width(8)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.4)
        ctx.stroke()

    def drawScreenPoint( self, coord, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(10)
        pixx, pixy= coord
        pixRadius= self._epsilon * self._scale
        ctx.arc(pixx, pixy, pixRadius, 0, 2.0*math.pi)
        r, g, b= color
        ctx.set_source_rgb( r/255, g/255, b/255 )
        ctx.stroke()

    def drawScreenLine( self, coordA, coordB, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        xA, yA= coordA
        xB, yB= coordB
        ctx.move_to(xA, yA)
        ctx.line_to(xB, yB)
        r, g, b= color
        ctx.set_source_rgb( r/255, g/255, b/255 )
        ctx.stroke()

    def drawScreenCircle( self, coord, radius, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        pixx, pixy= coord
        ctx.arc(pixx, pixy, radius, 0, 2.0*math.pi)
        r, g, b= color
        ctx.set_source_rgb( r/255, g/255, b/255 )
        ctx.stroke()
    
    def updateScreen(self):
        # Create PyGame surface from Cairo Surface
        width, height= self._surface.get_width(), self._surface.get_height()
        image = pygame.image.frombuffer(
            self._surface.get_data(), # Cairo seems to works on a BGRA suface...
            (width, height), "BGRA"
        )

        # Tranfer to Screen
        self._screen.blit(image, (0, 0))
        pygame.display.flip()