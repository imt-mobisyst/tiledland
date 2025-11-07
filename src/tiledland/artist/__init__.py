from . import color as smColor, support, supportCairo

# Color function:
colorRatio= smColor.colorRatio
rgbColor= smColor.rgbColor
percentColor= smColor.percentColor
webColor= smColor.webColor
colorFromWeb= smColor.colorFromWeb
color= smColor.color

# Support:
SupportVoid= support.SupportVoid
SupportSVG= support.SupportSVG
SupportPNG= supportCairo.SupportPNG

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
        self._background= 0xb86e00
        self._panel= [
            Brush(0xffcd80, 0x603800, 4), # 0-Free
            Brush(0xff6644, 0x991100, 4), # 1-Red
            Brush(0x70f050, 0x20770a, 4), # 2-Green
            Brush(0x6666ff, 0x1111aa, 4), # 3-Blue
            Brush(0xfd9622, 0xdd550a, 4), # 4-Orange
            Brush(0xdd77ff, 0x8800aa, 4), # 5-Purple
            Brush(0x66ddee, 0x117799, 4), # 6-Cian
            Brush(0xffffff, 0xbbbbbb, 4), # 7-White
            Brush(0x888888, 0x555555, 4), # 8-Grey
            Brush(0x444444, 0x000000, 4), # 9-Black

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
        pmin= aBox.leftFloor()
        pmax= aBox.rightCeiling()
        self.setCamera( (pmin.x+pmax.x)*0.5, (pmin.y+pmax.y)*0.5 )
        distx= pmax.x-pmin.x
        disty= pmax.y-pmin.y
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
        pmin= aTile.box().leftFloor()
        c= aTile.position()
        x= c.x+(pmin.x-c.x)*2/3
        y= c.y+(pmin.y-c.y)*2/3
        self.write( x, y, str(aTile.id()), self._panel[ aTile.matter() ] )

    def drawAgent( self, agent, brushId ):
        self.fillShape(
            agent.envelope(),
            brushId )
        c= agent.position()
        self.write( c.x, c.y, str(agent.id()), self._panel[brushId] )
    
    def drawSceneNetwork( self, aScene ):
        for tile in aScene.tiles() :
            c= tile.position()
            self.tracePoint( c.x, c.y, self._panel[ tile.matter() ] )

        for fromId, toId in aScene.edges() :
            pfrom= aScene.tile( fromId ).position()
            brush= self._panel[ aScene.tile( fromId ).matter() ]
            pto= aScene.tile( toId ).position()
            self.traceLine( pfrom.x, pfrom.y, pto.x, pto.y, brush )
        #    self.tracePoint( aScene.tile(fromId) )

    def drawSceneTiles( self, aScene ):
        for tile in aScene.tiles() :
            self.drawTile( tile )

    def drawSceneAgents( self, aScene ):
        for tile in aScene.tiles() :
            for agent in tile.agents() :
                self.drawAgent( agent, agent.matter() )
    
    def writeSceneTiles( self, aScene ):
        for tile in aScene.tiles() :
            self.writeTile( tile )

    def drawScene( self, aScene ):
        self.drawSceneNetwork(aScene)
        self.drawSceneTiles(aScene)
        self.writeSceneTiles(aScene)
        self.drawSceneAgents(aScene)

    # Control:
    def flip(self):
        h= self._support.height()
        w= self._support.width()
        ref= self._support.flip()
        self._support.fillPolygon(
            [0, 0, w, w],
            [0, h, h, 0],
            self._background
        )
        return ref
