from .color import color, colorRatio, colorRatio, rgbColor, percentColor, webColor, colorFromWeb
from .support import AbsSupport, Support, SupportSVG

def draw(anEntity, filePath="shot-tiledland.png", width= 1600, height= 1200):
    pablo= Artist()
    fileExtend= filePath.split(".")[-1]
    if fileExtend in ["png", "PNG"]:
        from .supportCairo import SupportPNG
        pablo.init( filePath, width, height, SupportPNG )
    elif fileExtend in ["svg", "SVG"]:
        pablo.init( filePath, width, height, SupportSVG )    
    
    pablo.fit(anEntity)
    anEntity.renderOn(pablo)
    pablo.flip()
    return pablo

def createArtistSVG(filePath, width, height):
    return Artist().init(filePath, width, height, SupportSVG)

def createArtistPNG(filePath, width, height):
    from .supportCairo import SupportPNG
    return Artist().init(filePath, width, height, SupportPNG)

# Artist:
class Brush():
    def __init__(self, fill= 0xff6644, stroke= 0x991100, width= 4 ):
        self.fill= fill
        self.stroke= stroke
        self.width= width

class palette :
    background= [
        Brush(0xffcd80, 0x603800, 4), # 0-Free
        Brush(0xff6644, 0x991100, 4), # 1-Red
        Brush(0x70f050, 0x20770a, 4), # 2-Green
        Brush(0x6666ff, 0x1111aa, 4), # 3-Blue
        Brush(0xfd9622, 0xdd550a, 4), # 4-Orange
        Brush(0xdd77ff, 0x8800aa, 4), # 5-Purple
        Brush(0x66ddee, 0x117799, 4), # 6-Cian
        Brush(0xffffff, 0xbbbbbb, 4), # 7-White
        Brush(0x888888, 0x555555, 4), # 8-Grey
        Brush(0x444444, 0x000000, 4)  # 9-Black
    ]
    foreground= [
        Brush(0x603800, 0xffcd80, 4), # 10-Background
        Brush(0x991100, 0xff6644, 4), # 11-Red
        Brush(0x20770a, 0x70f050, 4), # 12-Green
        Brush(0x1111aa, 0x6666ff, 4), # 13-Blue
        Brush(0xdd550a, 0xfd9622, 4), # 14-Orange
        Brush(0x8800aa, 0xdd77ff, 4), # 15-Purple
        Brush(0x117799, 0x66ddee, 4), # 16-Cian
        Brush(0xbbbbbb, 0xffffff, 4), # 17-White
        Brush(0x555555, 0x888888, 4), # 18-Grey
        Brush(0x000000, 0x444444, 4)  # 19-Black
    ]

class Artist():
    def __init__(self):
        #  Initialize support:
        self._support= Support()

        # Initialize brush :
        self._background= 0xb86e00
        self._fontSize= 16

        # Initialize Frame :
        self._x= 0.0
        self._y= 0.0
        self._scale= 100.0
        self.flip()

    # Construction:
    def init(self, filePath, width, height, SupportClass= SupportSVG):
        self._support= SupportClass( width, height, filePath )
        self.flip()
        return self

    # Accessor:
    def support(self):
        return self._support

    def content(self):
        return self._support.content()

    def clear(self):
        h= self._support.height()
        w= self._support.width()
        self._support.clear()
        self._support.fillPolygon(
            [0, 0, w, w],
            [0, h, h, 0],
            self._background
        )
        return self
    
    def render( self ):
        return self._support.render()

    def camera( self ):
        return (self._x, self._y)
        
    def scale( self ):
        return (self._scale)

    # Setters:
    def setCamera( self, x, y ):
        self._x, self._y= x, y
        return self
        
    def setScale( self, scale ):
        self._scale= scale
        return self
    
    def fit(self, anObj):
        return self.fitBox( anObj.box() )

    def fitBox( self, aBox, marge=10 ):
        marge= marge*2
        minx, miny= aBox.leftFloor().asTuple()
        maxx, maxy= aBox.rightCeiling().asTuple()
        self.setCamera( (minx+maxx)*0.5, (miny+maxy)*0.5 )
        distx= maxx-minx
        disty= maxy-miny
        ratioX, ratioY= 1.0, 1.0
        if distx != 0.0 :
           ratioX= (self._support.width()-marge)/distx
        if disty != 0.0 :
            ratioY= (self._support.height()-marge)/disty
        self.setScale( min(ratioX, ratioY) )
        return self

    # Panel managments:

    # Transformation World <-> Frame
    def toFrame(self, x, y ):
        dwidth= self._support.width()*0.5
        dheight= self._support.height()*0.5
        dx= (x-self._x)*self._scale
        dy= (y-self._y)*-self._scale
        return dx+dwidth, dy+dheight

    def xToFrame(self, x ):
        dwidth= self._support.width()*0.5
        return (x-self._x)*self._scale + dwidth

    def yToFrame(self, y ):
        dheight= self._support.height()*0.5
        return (y-self._y)*-self._scale + dheight

    def toWorld(self, pixx, pixy):
        return 0, 0

    # Drawing primitives:
    def tracePoint( self, x, y, brush= Brush() ):
        pixx, pixy= self.toFrame( x, y )
        self._support.fillCircle( pixx, pixy, brush.width, brush.stroke )
        return self

    def traceLine( self, ax, ay, bx, by, brush= Brush() ):
        pixxA, pixyA= self.toFrame( ax, ay )
        pixxB, pixyB= self.toFrame( bx, by )
        self._support.traceLine( pixxA, pixyA, pixxB, pixyB, brush.stroke, brush.width)
        return self

    def traceCircle( self, x, y, radius, brush= Brush()):
        pixx, pixy= self.toFrame(x, y)
        self._support.traceCircle( pixx, pixy, radius*self._scale, brush.stroke, brush.width)
        return self

    def fillCircle( self, x, y, radius, brush= Brush()):
        pixx, pixy= self.toFrame(x, y)
        self._support.fillCircle( pixx, pixy, radius*self._scale, brush.fill )
        return self

    def drawCircle( self, x, y, radius, brush= Brush() ):
        pixx, pixy= self.toFrame( x, y )
        self._support.drawCircle( pixx, pixy, radius*self._scale, brush.fill, brush.stroke, brush.width )
        return self

    def tracePolygon( self, coordXs, coordYs, brush= Brush() ):
        self._support.tracePolygon(
            [ self.xToFrame( x ) for x in coordXs ],
            [ self.yToFrame( y ) for y in coordYs ],
            brush.stroke, brush.width
        )
        return self

    def fillPolygon( self, coordXs, coordYs, brush= Brush() ):
        self._support.fillPolygon(
            [ self.xToFrame( x ) for x in coordXs ],
            [ self.yToFrame( y ) for y in coordYs ],
            brush.fill
        )
        return self

    def drawPolygon( self, coordXs, coordYs, brush= Brush() ):
        self._support.drawPolygon(
            [ self.xToFrame( x ) for x in coordXs ],
            [ self.yToFrame( y ) for y in coordYs ],
            brush.fill, brush.stroke, brush.width
        )
        return self

    # tiledland geometry:
    def drawConvex( self, shape, brush, px=0.0, py=0.0 ):
        listxs, listys= shape.asLists(px, py)
        self.drawPolygon( listxs, listys, brush )
        return self
    
    def fillConvex( self, shape, brush, px=0.0, py=0.0 ):
        listxs, listys= shape.asLists(px, py)
        self.fillPolygon( listxs, listys, brush )
        return self

    # Writting primitives:
    def write( self, x, y, text, brush= Brush() ):
        self._support.write(
            self.xToFrame(x), self.yToFrame(y),
            text, brush.stroke, self._fontSize
        )
        return self

    # Drawing frame:
    def drawFrameGrid( self, step= 1.0, color=None ):
        
        pixX, pixY= self.toFrame( 0, 0 )
        pixStep= step*self._scale

        while pixX > pixStep :
            pixX-= pixStep
        
        while pixY > pixStep :
            pixY-= pixStep
        
        width= self._support.width()
        height= self._support.height()

        if not color :
            color= palette.background[0].stroke
        
        # Vertical
        for i in range( (int)(width/pixStep)+1 ) :
            self._support.traceLine( pixX+(pixStep*i), 10, pixX+(pixStep*i), height-10, color, 2 )
        # Horizontal
        for i in range( (int)(height/pixStep)+1 ) :
            self._support.traceLine( 10, pixY+(pixStep*i), width-10, pixY+(pixStep*i), color, 2 )
        return self

    def drawFrameAxes( self ):
        brush= Brush( 0xE26060,  0xE26060, 6 )
        self.traceLine(  0, 0, 1, 0, brush )
        brush.stroke= 0x60E260
        self.traceLine(  0, 0, 0, 1, brush )
        brush.stroke= 0x0606E2
        self.tracePoint( 0, 0, brush )
        return self

    # Control:
    def flip(self):
        ref= self._support.flip()
        self.clear()
        return ref
