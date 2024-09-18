import math, cairo, pygame
from .geometry import Coord2, Segment

class Rgb:
    def __init__(self, r=0.0, g=0.0, b=0.0):
        self.r= r
        self.g= g
        self.b= b

class Pencil:
    def __init__(self, width=1200, height=800, title='Tiled-Land'):
        # Initialize pyGame:
        pygame.init()
        self._screen= pygame.display.set_mode( (width, height), pygame.RESIZABLE )
        pygame.display.set_caption(title)

    # Drawing primitives (level screen):
    def initBackground(self, color ):
        width, height= self._screen.get_width(), self._screen.get_height()
        self._surface= cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        ctx = cairo.Context(self._surface)
        ctx.move_to(0, 0)
        ctx.line_to(0, height)
        ctx.line_to(width, height)
        ctx.line_to(width, 0)
        ctx.close_path()
        #ctx.line_to(0, 0)
        ctx.set_source_rgba(color.r, color.g, color.b, 1.0)
        ctx.fill_preserve()
        ctx.set_line_width(8)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.4)
        ctx.stroke()
        return width, height
    
    # Drawing primitives (level screen):
    def tracePoint( self, pixx, pixy, color ):
        ctx = cairo.Context(self._surface)
        #ctx.set_line_width(10)
        pixRadius= 2 #self._epsilon * self._scale
        ctx.arc(pixx, pixy, pixRadius, 0, 2.0*math.pi)
        ctx.set_source_rgb( color.r, color.g, color.b )
        ctx.fill()

    def traceLine( self, pixxA, pixyA, pixxB, pixyB, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        ctx.move_to(pixxA, pixyA)
        ctx.line_to(pixxB, pixyB)
        ctx.set_source_rgb( color.r, color.g, color.b )
        ctx.stroke()

    def traceCircle( self, pixx, pixy, radius, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        ctx.arc(pixx, pixy, radius, 0, 2.0*math.pi)
        ctx.set_source_rgb( color.r, color.g, color.b )
        ctx.stroke()

    def fillCircle( self, pixx, pixy, radius, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        ctx.arc(pixx, pixy, radius, 0, 2.0*math.pi)
        ctx.set_source_rgb( color.r, color.g, color.b )
        ctx.fill()
    
    def drawCircle( self, pixx, pixy, radius, colorFill, colorTrace ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        ctx.arc(pixx, pixy, radius, 0, 2.0*math.pi)
        ctx.set_source_rgb( colorFill.r, colorFill.g, colorFill.b )
        ctx.fill_preserve()
        ctx.set_source_rgb( colorTrace.r, colorTrace.g, colorTrace.b )
        ctx.stroke()
    
    def tracePolygon( self, pixxs, pixys, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        ctx.move_to( pixxs[0], pixys[0] )
        for pixx, pixy in zip( pixxs[1:], pixys[1:] ) :
            ctx.line_to(pixx, pixy)
        ctx.close_path()
        ctx.set_source_rgb( color.r, color.g, color.b )
        ctx.stroke()
    
    def fillPolygon( self, pixxs, pixys, color ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        ctx.move_to( pixxs[0], pixys[0] )
        for pixx, pixy in zip( pixxs[1:], pixys[1:] ) :
            ctx.line_to(pixx, pixy)
        ctx.close_path()
        ctx.set_source_rgb( color.r, color.g, color.b )
        ctx.fill()
    
    def drawPolygon( self, pixxs, pixys, colorFill, colorTrace ):
        ctx = cairo.Context(self._surface)
        ctx.set_line_width(2)
        ctx.move_to( pixxs[0], pixys[0] )
        for pixx, pixy in zip( pixxs[1:], pixys[1:] ) :
            ctx.line_to(pixx, pixy)
        ctx.close_path()
        ctx.set_source_rgb( colorFill.r, colorFill.g, colorFill.b )
        ctx.fill_preserve()
        ctx.set_source_rgb( colorTrace.r, colorTrace.g, colorTrace.b )
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
        return width, height
    
class Interface:

    #Constructor:
    def __init__(self,
                 width=1200, height=800,
                 traceColors= [ Rgb( 0.8,  0.1,  0.1), Rgb( 0.1,  0.8,  0.1), Rgb( 0.1,  0.1,  0.8), Rgb(0.40, 0.40, 0.40), Rgb( 0.8, 0.70, 0.30) ],
                 fillColors= [ Rgb( 0.9,  0.7,  0.5), Rgb( 0.8,  0.9,  0.5), Rgb( 0.8,  0.7,  0.9), Rgb(0.80, 0.80, 0.80), Rgb( 0.90, 0.8, 0.40) ] ):

        #  Initialize Pencil:
        self._pencil= Pencil()
        # Initialize Color panels:
        self._traceColors= traceColors
        self._fillColors= fillColors
        # Initialize Frame :
        self._dwidth= width/2
        self._dheight= height/2
        self.initializeBasis(
            Coord2( 10.0, 5.0),
            40.0
        )
        # Initialize engine:
        self._loop= False

    def initializeBasis(self, center, scale):
        self._center= Coord2( 10.0, 5.0) # the center of the screen look at (10.0, 5.0)
        self._scale= 40.0 # 1 meter = 40 pixel
        return self
    
    def initializeColorPanels( self, traceColors, fillColors ):
        self._traceColors= traceColors
        self._fillColors= fillColors
        return self
    

    # Transformation World <-> Screen
    def toDrawing(self, x, y ):
        dx= (x-self._center._x)*self._scale
        dy= (y-self._center._y)*-self._scale
        return dx+self._dwidth, dy+self._dheight

    def xToDrawing(self, x ):
        return (x-self._center._x)*self._scale + self._dwidth

    def yToDrawing(self, y ):
        return (y-self._center._y)*-self._scale + self._dheight

    def toWorld(self, pixx, pixy):
        return 0, 0

    # Drawing primitives (level basis):
    def drawFrameGrid( self, step= 10.0 ):
        pixX, pixY= self.toDrawing( 0, 0 )
        pixStep= step*self._scale

        while pixX > pixStep :
            pixX-= pixStep
        
        while pixY > pixStep :
            pixY-= pixStep
        
        width= self._dwidth*2.0
        height= self._dheight*2.0

        # Vertical
        for i in range( (int)(width/pixStep)+1 ) :
            self._pencil.traceLine( pixX+(pixStep*i), 10, pixX+(pixStep*i), height-10, self._traceColors[-1] )
        # Horizontal
        for i in range( (int)(height/pixStep)+1 ) :
            self._pencil.traceLine( 10, pixY+(pixStep*i), width-10, pixY+(pixStep*i), self._traceColors[-1] )
        return self

    def drawFrameAxes( self ):
        zero= Coord2(0, 0)
        self.traceLine(  zero, Coord2(1, 0), Rgb(0.8, 0.4, 0.4 ) )
        self.traceLine(  zero, Coord2(0, 1), Rgb(0.4, 0.8, 0.4 ) )
        self.tracePoint( zero, Rgb(0.1, 0.1, 0.8) )

    # Drawing primitives (level geometry):
    def tracePoint( self, point, color= Rgb(0.2,0.2,0.2) ):
        pixx, pixy= self.toDrawing( point.x(), point.y() )
        self._pencil.tracePoint( pixx, pixy, color )

    def traceLine( self, pA, pB, color= Rgb(0.2,0.2,0.2) ):
        pixxA, pixyA= self.toDrawing( pA.x(), pA.y() )
        pixxB, pixyB= self.toDrawing( pB.x(), pB.y() )
        self._pencil.traceLine( pixxA, pixyA, pixxB, pixyB, color)

    def traceCircle( self, point, radius, color= Rgb(0.2,0.2,0.2) ):
        pixx, pixy= self.toDrawing(point.x(), point.y())
        self._pencil.traceCircle( pixx, pixy, radius*self._scale, color)

    def fillCircle( self, point, radius, color= Rgb(0.8,0.8,0.8) ):
        pixx, pixy= self.toDrawing(point.x(), point.y())
        self._pencil.fillCircle( pixx, pixy, radius*self._scale, color)

    def drawCircle( self, point, radius, colorFill= Rgb(0.8,0.8,0.8), colorTrace=Rgb(0.2,0.2,0.2) ):
        pixx, pixy= self.toDrawing(point.x(), point.y())
        self._pencil.drawCircle( pixx, pixy, radius*self._scale, colorFill, colorTrace)

    def tracePolygon( self, coords, color= Rgb(0.2,0.2,0.2) ):
        self._pencil.tracePolygon(
            [ self.xToDrawing( c.x() ) for c in coords ],
            [ self.yToDrawing( c.y() ) for c in coords ],
            color
        )

    def fillPolygon( self, coords, color= Rgb(0.8,0.8,0.8) ):
        self._pencil.fillPolygon(
            [ self.xToDrawing( c.x() ) for c in coords ],
            [ self.yToDrawing( c.y() ) for c in coords ],
            color
        )

    def drawPolygon( self, coords, colorFill= Rgb(0.8,0.8,0.8), colorTrace= Rgb(0.2,0.2,0.2) ):
        self._pencil.drawPolygon(
            [ self.xToDrawing( c.x() ) for c in coords ],
            [ self.yToDrawing( c.y() ) for c in coords ],
            colorFill, colorTrace
        )

    # Drawing primitives (level tiled-land):
    def drawTile( self, aTile ):
        # Local parameters:
        maxTag= min( len( self._traceColors ), len( self._fillColors ) )-1
        center= aTile.center()
        segments= aTile.segments()
        # fill shape:
        if len(segments) > 0 :
            self.fillPolygon(
                [ seg.a() for seg in segments ],
                self._fillColors[ aTile.tag()%(maxTag+1) ]
            )
        # trace shape:
        for seg, tag in zip( segments, aTile.segmentTags() ) :
            segmentColor= self._traceColors[ min( tag, maxTag) ]
            self.traceLine( seg.a(), seg.b(), segmentColor )
        # central point:
        self.tracePoint( center, self._traceColors[ aTile.tag()%(maxTag+1) ] )

    def drawJoint( self, aJoint ):
        gateA, gateB= aJoint.gates()
        self.traceLine( gateA.middle(), gateB.middle(), self._traceColors[-1] )

    def drawJointShape( self, aJoint ):
        for seg in aJoint.shapeSegments() :
            self.traceLine( seg.a(), seg.b(), self._traceColors[-1] )
        front= aJoint.frontiere()
        self.traceLine( front.a(), front.b(), self._traceColors[-1] )

    def drawMap( self, aMap ):
        for tile in aMap.tiles() :
            self.drawTile( tile )
        for joint in aMap.allJoints() :
            self.drawJoint( joint )
        
    def drawBody( self, aBody, aColor= Rgb(0.2,0.2,0.2) ):
        pixx, pixy= self.toDrawing( aBody.position.x(), aBody.position.y() )
        pixRadius= aBody.radius * self._scale
        self._pencil.traceCircle( pixx, pixy, pixRadius, aColor )
        self._pencil.traceLine( 
            pixx, pixy,
            pixx+(math.cos(aBody.orientation))*pixRadius,
            pixy+(-math.sin(aBody.orientation))*pixRadius,
            aColor
        )

    # Engine:
    def process_void(frame):
        return True

    def eventHandler_basic(self, event):
        if event.type == pygame.QUIT:
            self._loop= False

    def infiniteLoop(self, process= process_void, eventHandler= eventHandler_basic ):
        self._loop= True
        while self._loop :
            self._pencil.initBackground( self._fillColors[-1] )
            self._loop= process( self )
            for event in pygame.event.get() :
                eventHandler( self, event )
            self._pencil.updateScreen()

    def signalHandler_stop(self, sig, frame):
        self._loop= False


