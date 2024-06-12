import math
import sys

from . import Point2, Segment
import pygame

# global colors.
_backgroundColor= (230, 204, 102)
_bgBisColor= (204, 178,  80)
_drawColor=  (204,  26,  26)
_alt1Color=  ( 26, 204,  26)
_alt2Color=  ( 26,  26, 204)
_greyColor=  (102, 102, 102)
_colors= [ _bgBisColor, _drawColor, _alt1Color, _alt2Color, _greyColor ]


class Frame :

    def __init__(self, width=1200, height=800):
        # Initialize pyGame:
        pygame.init()
        self._screen= pygame.display.set_mode( (width, height), pygame.RESIZABLE )
        pygame.display.set_caption('Poly-Map')
        self._dwidth= width/2
        self._dheight= height/2
        self._loop= False

        # Initialize cartesian basis:
        self._epsilon= 0.001
        self._cx= 10.0
        self._cy= 5.0
        self._scale= 40.0
    
    # Void process executor:
    def process_void(frame):
        return True

    # basic event handler:
    def eventHandler_basic(self, event):
        if event.type == pygame.QUIT:
            self._loop= False
        #else:
        #    print(event)

    # Infinite loop:
    def infiniteLoop(self, process= process_void, eventHandler= eventHandler_basic ):
        self._loop= True
        while self._loop :
            self._loop= process( self )
            for event in pygame.event.get() :
                eventHandler( self, event )
            pygame.display.update()

    # Transformation World <-> Screen
    def toDrawing(self, p):
        dx= (p.x-self._cx)*self._scale
        dy= (p.y-self._cy)*-self._scale
        return (dx+self._dwidth, dy+self._dheight)

    def toWorld(self, pixx, pixy):
        return (0, 0)

    # Draw primitives: 
    def initBackground(self, color= _backgroundColor):
        self._dwidth=  self._screen.get_width() /2
        self._dheight= self._screen.get_height()/2
        self._screen.fill(color)

    def drawPoint( self, point, color= _drawColor ):
        coord= self.toDrawing(point)
        pygame.draw.circle( self._screen, color, coord, 5 )

    def drawLine( self, pA, pB, color= _drawColor ):
        coord1= self.toDrawing(pA)
        coord2= self.toDrawing(pB)
        pygame.draw.line( self._screen, color, coord1, coord2, 2 )

    def drawCircle( self, point, radius, color= _drawColor ):
        coord= self.toDrawing(point)
        pygame.draw.circle( self._screen, color, coord, radius*self._scale, 2 )

    # Draw Frame:
    def drawFrameAxes( self ):
        pixx0, pixy0= self.toDrawing( Point2(0, 0) )
        pixx1, pixy1= self.toDrawing( Point2(1, 1) )

        pygame.draw.line(
            self._screen, (204, 102, 102),
            (pixx0, pixy0), (pixx1, pixy0), 4
        )
        pygame.draw.line(
            self._screen, (102, 204, 102),
            (pixx0, pixy0), (pixx0, pixy1), 4
        )
        pygame.draw.circle( self._screen, (26, 26, 204), (pixx0, pixy0), 5 )

    def drawFrameGrid( self, step= 10.0, color= _bgBisColor ):
        pixX, pixY= self.toDrawing( Point2(0, 0) )
        pixStep= step*self._scale

        while pixX > pixStep :
            pixX-= pixStep
        
        while pixY > pixStep :
            pixY-= pixStep
        
        width= self._dwidth*2.0
        height= self._dheight*2.0

        # Vertical
        for i in range( (int)(width/pixStep)+1 ) :
            pygame.draw.line(
                self._screen, color,
                (pixX+(pixStep*i), 10),
                (pixX+(pixStep*i), height-10), 4
            )

        # Horizontal
        for i in range( (int)(height/pixStep)+1 ) :
            pygame.draw.line(
                self._screen, color,
                ( 10, pixY+(pixStep*i) ),
                ( width-10, pixY+(pixStep*i) ), 4
            )
        return self
    
    # Draw PolyMap Elements:
    def drawCell( self, aCell, colors= _colors ):
        maxTag= len( colors )-1
        center= aCell.center()
        for segment in aCell.segments() :
            color= colors[ min( segment.tag(), maxTag) ]
            vv1= segment.pointA() - center
            vv2= segment.pointB() - center
            self.drawLine( vv1.scale(0.98)+center, vv2.scale(0.98)+center, color )
        self.drawPoint( aCell.center(), colors[0] )

    def drawBody(self, aBody, aColor= _drawColor):
        pixx, pixy= self.toDrawing( aBody.position )
        pixRadius= aBody.radius * self._scale
        pygame.draw.circle( self._screen, aColor, (pixx, pixy), pixRadius, 2 )
        pygame.draw.line( self._screen, aColor, (pixx, pixy),
            (pixx+(math.cos(aBody.orientation))*pixRadius,
              pixy+(-math.sin(aBody.orientation))*pixRadius
            )
        )