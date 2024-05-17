import math
import sys

import cairo

class Frame :

    def __init__(self):
        self._cx= 10.0
        self._cy= 5.0
        self._scale= 40.0
    
    # Transfomation:
    def toDrawing(self, x, y):
        dx= (x-self._cx)*self._scale
        dy= (y-self._cy)*-self._scale
        return (dx+self._dwidth, dy+self._dheight)

    def toWorld(self, pixx, pixy):
        return (0, 0)

    # Drawing:
    def initializeSurface(self, width, height):
        self._dwidth= width/2
        self._dheight= height/2
        self._surface= cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self._surface)
        ctx.move_to(0, 0)
        ctx.line_to(0, height)
        ctx.line_to(width, height)
        ctx.line_to(width, 0)
        ctx.line_to(0, 0)
        ctx.set_source_rgba(0.9, 0.8, 0.4, 1.0)
        ctx.fill_preserve()
        ctx.set_line_width(8)
        ctx.set_source_rgba(0.76, 0.67, 0.33, 1.0)
        ctx.stroke()
        return self._surface

    def drawFrame( self ):
        pixx0, pixy0= self.toDrawing(0, 0)
        pixx1, pixy1= self.toDrawing(1, 1)
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(4)
        ctx.move_to(pixx0, pixy0)
        ctx.line_to(pixx1, pixy0)
        ctx.set_source_rgba(1, 0, 0, 0.4)
        ctx.stroke()
        ctx.move_to(pixx0, pixy0)
        ctx.line_to(pixx0, pixy1)
        ctx.set_source_rgba(0, 1, 0, 0.4)
        ctx.stroke()
        ctx.arc(pixx0, pixy0, 5, 0, 2.0 * math.pi)
        ctx.set_source_rgba(0, 0, 4, 1.0)
        ctx.fill()
    
    def drawPose(self, aPose):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(4)
        pixx, pixy= self.toDrawing( aPose.px, aPose.py )
        pixRadius= 0.1 * self._scale
        ctx.arc(pixx, pixy, pixRadius, 0, 2.0*math.pi)
        ctx.move_to(pixx, pixy)
        ctx.line_to(pixx+(math.cos(aPose.oz))*pixRadius, pixy+(-math.sin(aPose.oz))*pixRadius)
        ctx.set_source_rgb( 0.8, 0.1, 0.1 )
        ctx.stroke()

