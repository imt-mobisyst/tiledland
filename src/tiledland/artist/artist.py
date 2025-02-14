from .support import SupportVoid, SupportSVG
from .supportCairo import SupportPNG

# Artist:
class Brush():
    def __init__(self, fill= 0xff6644, stroke= 0x991100, width= 4 ):
        self.fill= fill
        self.stroke= stroke
        self.width= width

class Artist():
    def __init__(self):
        #  Initialize support:
        self._support= SupportVoid()

        # Initialize brush :
        self._panel= [
            Brush(0xffbb55, 0xaa6606, 4), # 0-Background
            Brush(0xff6644, 0x991100, 4), # 1-Red
            Brush(0x44ff44, 0x119911, 4), # 2-Green
            Brush(0x6666ff, 0x1111aa, 4), # 3-Blue
            Brush(0xff9922, 0xdd5500, 4), # 4-Orange
            Brush(0xdd77ff, 0x8800aa, 4), # 5-Purple
            Brush(0x66ddee, 0x117799, 4), # 6-Cian
            Brush(0xffffff, 0xdddddd, 4), # 7-White
            Brush(0x888888, 0x555555, 4), # 8-Grey
            Brush(0x444444, 0x000000, 4), # 9-Black

            Brush(0xaa6606, 0xffbb55, 4), # 0-Background
            Brush(0x991100, 0xff6644, 4), # 1-Red
            Brush(0x119911, 0x44ff44, 4), # 2-Green
            Brush(0x1111aa, 0x6666ff, 4), # 3-Blue
            Brush(0xdd5500, 0xff9922, 4), # 4-Orange
            Brush(0x8800aa, 0xdd77ff, 4), # 5-Purple
            Brush(0x117799, 0x66ddee, 4), # 6-Cian
            Brush(0xdddddd, 0xffffff, 4), # 7-White
            Brush(0x555555, 0x888888, 4), # 8-Grey
            Brush(0x000000, 0x444444, 4) # 9-Black
        ]
        self._fontSize= 16

        # Initialize Frame :
        self._x= 0.0
        self._y= 0.0
        self._scale= 100.0
        self.flip()

    # Construction:
    def initializeSVG(self, filePath):
        self._support= SupportSVG( filePath=filePath )
        self.flip()
        return self
    
    def initializePNG(self, filePath):
        self._support= SupportPNG( filePath=filePath )
        self.flip()
        return self

    # Accessor:
    def support(self):
        return self._support

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
    
    def fitBox( self, aBox, marge=10 ):
        marge= marge*2
        minx, miny= aBox[0].tuple()
        maxx, maxy= aBox[1].tuple()
        self.setCamera( (minx+maxx)*0.5, (miny+maxy)*0.5 )
        distx= maxx-minx
        disty= maxy-miny
        ratioX= (self._support.width()-marge)/distx
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
            color= self._panel[0].stroke
        
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
    
    # Drawing map:
    def drawShape( self, envelop, brushId=0, px=0, py=0 ):
        self.drawPolygon(
            [p[0]+px for p in envelop],
            [p[1]+py for p in envelop],
            self._panel[ brushId%len(self._panel) ]
        )
    
    def fillShape( self, envelop, brushId=0, px=0, py=0 ):
        self.fillPolygon(
            [p[0]+px for p in envelop],
            [p[1]+py for p in envelop],
            self._panel[ brushId%len(self._panel) ]
        )
    
    def drawTile( self, aTile ):
        env= aTile.envelope()
        self.drawPolygon(
            [p[0] for p in env],
            [p[1] for p in env],
            self._panel[ aTile.matter() ]
        )
    
    def writeTile( self, aTile ):
        minx, miny= aTile.box()[0].tuple()
        x, y= aTile.center().tuple()
        x= x+(minx-x)*2/3
        y= y+(miny-y)*2/3
        self.write( x, y, str(aTile.number()), self._panel[ aTile.matter() ] )

    def drawPiece( self, position, brushId, shape, name ):
        x, y= position
        self.fillShape(
            shape.envelope(),
            brushId, x, y )
        minx, miny= shape.box()[0].tuple()
        x= x+(minx)*4/5
        y= y+(miny)*1/3
        self.write( x, y, name, self._panel[brushId] )
    
    def drawMapNetwork( self, aMap ):
        for tile in aMap.tiles() :
            cx, cy= tile.center().tuple()
            self.tracePoint( cx, cy, self._panel[ tile.matter() ] )

        for fromId, toId in aMap.edges() :
            fromX, fromY= aMap.tile( fromId ).center().tuple()
            brush= self._panel[ aMap.tile( fromId ).matter() ]
            toX, toY= aMap.tile( toId ).center().tuple()
            self.traceLine( fromX, fromY, toX, toY, brush )
        #    self.tracePoint( aMap.tile(fromId) )

    def drawMapTiles( self, aMap ):
        for tile in aMap.tiles() :
            self.drawTile( tile )

    def drawMapPieces( self, aMap ):
        for tile in aMap.tiles() :
            x, y= tile.center().tuple()
            position= (x+0.1, y+0.1)
            for piece, brushId, shapeId in tile.pieceDescriptions() :
                shape= aMap._shapes[shapeId]
                self.drawPiece( position, brushId, shape, piece.family() )
    
    def writeMapTiles( self, aMap ):
        for tile in aMap.tiles() :
            self.writeTile( tile )

    def drawMap( self, aMap ):
        self.drawMapNetwork(aMap)
        self.drawMapTiles(aMap)
        self.writeMapTiles(aMap)
        self.drawMapPieces(aMap)

    # Control:
    def flip(self):
        h= self._support.height()
        w= self._support.width()
        ref= self._support.flip()
        self._support.fillPolygon(
            [0, 0, w, w],
            [0, h, h, 0],
            self._panel[0].fill
        )
        return ref

