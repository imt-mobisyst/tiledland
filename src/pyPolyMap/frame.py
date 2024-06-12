import math
import sys

from . import Point2, Segment
import pygame

# global colors.
_backgroundColor= (0.9, 0.8, 0.4)
_bgBisColor= (0.8, 0.7, 0.4)
_drawColor=  (0.8, 0.1, 0.1)
_alt1Color=  (0.1, 0.8, 0.1)
_alt2Color=  (0.1, 0.1, 0.8)
_greyColor=  (0.4, 0.4, 0.4)
_colors= [ _bgBisColor, _drawColor, _alt1Color, _alt2Color, _greyColor ]

class Frame :

    def __init__(self):
        self._epsilon= 0.001
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

    # Drawing Frame:
    def initializeSurface(self, width, height, bgColor= _backgroundColor):
        self._dwidth= width/2
        self._dheight= height/2
        self._surface= cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self._surface)
        ctx.move_to(0, 0)
        ctx.line_to(0, height)
        ctx.line_to(width, height)
        ctx.line_to(width, 0)
        ctx.line_to(0, 0)
        ctx.set_source_rgba(bgColor.r, bgColor.g, bgColor.b, 1.0)
        ctx.fill_preserve()
        ctx.set_line_width(8)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.4)
        ctx.stroke()
        return self._surface

    def drawFrameAxes( self ):
        pixx0, pixy0= self.toDrawing(0, 0)
        pixx1, pixy1= self.toDrawing(1, 1)
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(4)
        ctx.move_to(pixx0, pixy0)
        ctx.line_to(pixx1, pixy0)
        ctx.set_source_rgb(0.8, 0.4, 0.4)
        ctx.stroke()
        ctx.move_to(pixx0, pixy0)
        ctx.line_to(pixx0, pixy1)
        ctx.set_source_rgb(0.4, 0.8, 0.4)
        ctx.stroke()
        ctx.arc(pixx0, pixy0, 5, 0, 2.0 * math.pi)
        ctx.set_source_rgba(0, 0, 1, 1.0)
        ctx.fill()
    
    def drawFrameGrid( self, step= 10.0 ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(1)
        pixX, pixY= self.toDrawing( 0, 0 )
        pixStep= step*self._scale

        ctx.arc(pixX, pixY, 6, 0, 2.0 * math.pi)

        while pixX > pixStep :
            pixX-= pixStep
        
        while pixY > pixStep :
            pixY-= pixStep
        
        width= self._dwidth*2.0
        height= self._dheight*2.0

        # Vertical
        for i in range( (int)(width/pixStep)+1 ) :
            ctx.move_to( pixX+(pixStep*i), 10)
            ctx.line_to( pixX+(pixStep*i), height-10)

        # Horizontal
        for i in range( (int)(height/pixStep)+1 ) :
            ctx.move_to( 10, pixY+(pixStep*i) )
            ctx.line_to( width-10, pixY+(pixStep*i) )

        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.1)
        ctx.stroke()
        return self
    
    # Drawing Primitives:
    def drawPoint(self, aPoint, aColor= _drawColor, width= 6):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(width)
        pixx, pixy= self.toDrawing( aPoint.x, aPoint.y )
        pixRadius= self._epsilon * self._scale
        ctx.arc(pixx, pixy, pixRadius, 0, 2.0*math.pi)
        ctx.set_source_rgb( aColor.r, aColor.g, aColor.b )
        ctx.stroke()

    def drawSegment(self, aSegment, aColor= _drawColor, width= 2):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(width)
        xA, yA= self.toDrawing( aSegment._a.x, aSegment._a.y )
        xB, yB= self.toDrawing( aSegment._b.x, aSegment._b.y )
        ctx.move_to(xA, yA)
        ctx.line_to(xB, yB)
        ctx.set_source_rgb( aColor.r, aColor.g, aColor.b )
        ctx.stroke()

    def drawCircle(self, aCenter, aRadius, aColor= _drawColor, width= 2):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(width)
        pixx, pixy= self.toDrawing( aCenter.x, aCenter.y )
        pixRadius= aRadius * self._scale
        ctx.arc(pixx, pixy, pixRadius, 0, 2.0*math.pi)
        ctx.set_source_rgb( aColor.r, aColor.g, aColor.b )
        ctx.stroke()
    
    # Drawing ConvexMap Object:
    def drawBody(self, aBody, aColor= _drawColor):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(4)
        pixx, pixy= self.toDrawing( aBody.position.x, aBody.position.y )
        pixRadius= aBody.radius * self._scale
        ctx.arc(pixx, pixy, pixRadius, 0, 2.0*math.pi)
        ctx.move_to(pixx, pixy)
        ctx.line_to(
            pixx+(math.cos(aBody.orientation))*pixRadius,
            pixy+(-math.sin(aBody.orientation))*pixRadius
        )
        ctx.set_source_rgb( aColor.r, aColor.g, aColor.b )
        ctx.stroke()

    def drawCell( self, aCell, colors= _colors ):
        maxTag= len( colors )-1
        center= aCell.center()
        for v1, v2, tag in aCell.segments() :
            color= colors[ min(tag, maxTag) ]
            vv1= v1 - center
            vv2= v2 - center
            self.drawSegment(
                Segment(
                    vv1.scale(0.98)+center,
                    vv2.scale(0.98)+center
                ),
                color
            )
        self.drawPoint( aCell.center(), colors[0] )
