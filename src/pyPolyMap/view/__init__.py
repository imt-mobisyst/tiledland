import math, pygame
from .. import Point2

#class ColorPanel:
class colorPanel:
    background= (230, 204, 102)
    backgroundBis= (204, 178,  80)
    draw=  (204,  26,  26)
    alt1=  ( 26, 204,  26)
    alt2=  ( 26,  26, 204)
    grey=  (102, 102, 102)
    colors= [ backgroundBis, draw, alt1, alt2, grey ]

class AbsFrame :

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
            self.initBackground()
            self._loop= process( self )
            for event in pygame.event.get() :
                eventHandler( self, event )
            self.updateScreen()
    
    def updateScreen(self):
        pygame.display.update()

    # Transformation World <-> Screen
    def toDrawing(self, p):
        dx= (p.x-self._cx)*self._scale
        dy= (p.y-self._cy)*-self._scale
        return (dx+self._dwidth, dy+self._dheight)

    def toWorld(self, pixx, pixy):
        return (0, 0)

    # Draw primitives: 
    def initBackground(self, color= colorPanel.background):
        self._dwidth=  self._screen.get_width() /2
        self._dheight= self._screen.get_height()/2
        self._screen.fill(color)

    def drawScreenPoint( self, coord, color):
        pass

    def drawScreenLine( self, coordA, coordB, color):
        pass

    def drawScreenCircle( self, coord, radius, color):
        pass

    # Drawing :
    def drawPoint( self, point, color= colorPanel.draw ):
        coord= self.toDrawing(point)
        self.drawScreenPoint( coord, color )

    def drawLine( self, pA, pB, color= colorPanel.draw ):
        coordA= self.toDrawing(pA)
        coordB= self.toDrawing(pB)
        self.drawScreenLine( coordA, coordB, color)

    def drawCircle( self, point, radius, color= colorPanel.draw ):
        coord= self.toDrawing(point)
        self.drawScreenCircle( coord, radius*self._scale, color)
    
    # Draw Frame:
    def drawFrameGrid( self, step= 10.0, color= colorPanel.backgroundBis ):
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
            self.drawScreenLine(
                (pixX+(pixStep*i), 10),
                (pixX+(pixStep*i), height-10),
                color
            )

        # Horizontal
        for i in range( (int)(height/pixStep)+1 ) :
            self.drawScreenLine(
                ( 10, pixY+(pixStep*i) ),
                ( width-10, pixY+(pixStep*i) ),
                color
            )
        return self

    def drawFrameAxes( self ):
        zero= Point2()
        self.drawLine(  zero, Point2(1, 0), (204, 102, 102) )
        self.drawLine(  zero, Point2(0, 1), (102, 204, 102) )
        self.drawPoint( zero, (26, 26, 204) )
    
    # Draw PolyMap Elements:
    def drawCell( self, aCell, colors= colorPanel.colors ):
        maxTag= len( colors )-1
        center= aCell.center()
        for segment in aCell.segments() :
            color= colors[ min( segment.tag(), maxTag) ]
            vv1= segment.pointA() - center
            vv2= segment.pointB() - center
            self.drawLine( vv1.scale(0.98)+center, vv2.scale(0.98)+center, color )
        self.drawPoint( aCell.center(), colors[0] )

    def drawBody(self, aBody, aColor= colorPanel.draw):
        pixx, pixy= self.toDrawing( aBody.position )
        pixRadius= aBody.radius * self._scale
        self.drawScreenCircle( (pixx, pixy), pixRadius, aColor )
        self.drawScreenLine( 
            (pixx, pixy),
            (pixx+(math.cos(aBody.orientation))*pixRadius,
              pixy+(-math.sin(aBody.orientation))*pixRadius
            ),
            aColor
        )
