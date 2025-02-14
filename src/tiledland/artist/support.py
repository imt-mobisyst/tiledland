from .color import webColor

class SupportVoid():

    # Accessor:
    def width(self):
        return 1200
    
    def height(self):
        return 800
    
    # Control:
    def clear(self):
        pass
    
    def render( self ):
        return None
    
    def flip( self ):
        rendering= self.render()
        self.clear()
        return rendering
    
    # Drawing primitives:
    def traceLine( self, pixxA, pixyA, pixxB, pixyB, strokeColor, strokeWidth ):
        pass

    def traceCircle( self, pixx, pixy, radius, strokeColor, strokeWidth ):
        pass

    def fillCircle( self, pixx, pixy, radius, fillColor ):
        pass

    def drawCircle( self, pixx, pixy, radius, fillColor, strokeColor, strokeWidth):
        pass

    def tracePolygon( self, pixXs, pixYs, strokeColor, strokeWidth ):
        pass

    def fillPolygon( self, pixXs, pixYs, fillColor ):
        pass

    def drawPolygon( self, pixXs, pixYs, fillColor, strokeColor, strokeWidth ):
        pass

    # Writting primitives:
    def write( self, pixXs, pixYs, text, color, fontSize ):
        pass

class SupportSVG( SupportVoid ):
    def __init__(self, width= 800, height= 600, filePath= "shot-hacka.svg" ):
        self._width= width
        self._height= height
        self._canvas= []
        self._filePath= filePath
        self.save( self._filePath )
    
    # Accessor: 
    def width(self):
        return self._width
    
    def height(self):
        return self._height
    
    def canvas(self):
        return self._canvas
    
    def filePath(self):
        return self._filePath

    # Control:
    def clear(self):
        self._canvas= []
    
    def render(self):
        return f'<svg width="{self.width()}" height="{self.height()}">\n' + '\n'.join( self._canvas + ['</svg>'] ) 

    def flip(self):
        if self._filePath :
            arts= self.save( self._filePath )
        else :
            arts= self.render()
        self.clear()
        return arts

    def save( self, filePath ):
        file = open( filePath, "w")
        file.write( '<?xml version="1.0" encoding="UTF-8"?>\n' )
        arts= self.render()
        file.write( arts )
        file.close()
        return arts

    # Drawing primitives:
    def traceLine( self, pixxA, pixyA, pixxB, pixyB, strokeColor, strokeWidth ):
        self._canvas.append( f'<line x1="{pixxA}" y1="{pixyA}" x2="{pixxB}" y2="{pixyB}" style="stroke:{webColor(strokeColor)};stroke-width:{strokeWidth}"/>' )
        return self

    def traceCircle( self, pixx, pixy, radius, strokeColor, strokeWidth ):
        self._canvas.append( f'<circle r="{radius}" cx="{pixx}" cy="{pixy}" fill="none" stroke="{webColor(strokeColor)}" stroke-width="{strokeWidth}" />' )
        return self

    def fillCircle( self, pixx, pixy, radius, fillColor ):
        self._canvas.append( f'<circle r="{radius}" cx="{pixx}" cy="{pixy}" fill="{webColor(fillColor)}" />' )
        return self

    def drawCircle( self, pixx, pixy, radius, fillColor, strokeColor, strokeWidth):
        self._canvas.append( f'<circle r="{radius}" cx="{pixx}" cy="{pixy}" fill="{webColor(fillColor)}" stroke="{webColor(strokeColor)}" stroke-width="{strokeWidth}" />' )
        return self
    
    def tracePolygon( self, pixXs, pixYs, strokeColor, strokeWidth ):
        points= " ".join( [ f'{x},{y}' for x, y in zip(pixXs, pixYs) ] )
        self._canvas.append( f'<polygon points="{points}" style="fill:none;stroke:{webColor(strokeColor)};stroke-width:{strokeWidth}" />' )
        return self

    def fillPolygon( self, pixXs, pixYs, fillColor ):
        points= " ".join( [ f'{x},{y}' for x, y in zip(pixXs, pixYs) ] )
        self._canvas.append( f'<polygon points="{points}" fill="{webColor(fillColor)}" />' )
        return self

    def drawPolygon( self, pixXs, pixYs, fillColor, strokeColor, strokeWidth ):
        points= " ".join( [ f'{x},{y}' for x, y in zip(pixXs, pixYs) ] )
        self._canvas.append( f'<polygon points="{points}" style="fill:{webColor(fillColor)};stroke:{webColor(strokeColor)};stroke-width:{strokeWidth}" />' )
        return self
    
    # Writting primitives:
    def write( self, pixXs, pixYs, text, color, fontSize ):
        self._canvas.append( f'<text x="{pixXs}" y="{pixYs}" fill="{webColor(color)}" font-family="Verdana" font-size="{fontSize}">{text}</text>" />' )
        return self
    