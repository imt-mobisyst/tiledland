from .color import percentColor
from .support import SupportVoid

import math, cairo
#from .geometry import Coord2, Segment

class SupportPNG( SupportVoid ):
    def __init__(self, width= 800, height= 600, filePath= "shot-hacka.png" ):
        self._canvas= cairo.ImageSurface( cairo.Format.RGB24, width, height )
        self._width= width
        self._height= height
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
        self._canvas= cairo.ImageSurface( cairo.Format.RGB24, self._width, self._height )
    
    def render(self):
        return self._canvas
    
    def flip(self):
        if self._filePath :
            arts= self.save( self._filePath )
        else :
            arts= self.render()
        self.clear()
        return arts

    def save( self, filePath ):
        self._canvas.write_to_png( filePath )
        return

    # Drawing primitives:
    def traceLine( self, pixxA, pixyA, pixxB, pixyB, strokeColor, strokeWidth ):
        ctx = cairo.Context( self._canvas )
        r, g, b= percentColor(strokeColor)
        ctx.set_line_width(strokeWidth)
        ctx.move_to(pixxA, pixyA)
        ctx.line_to(pixxB, pixyB)
        ctx.set_source_rgb( r, g, b )
        ctx.stroke()
        return self
    
    def traceCircle( self, pixx, pixy, radius, strokeColor, strokeWidth ):
        ctx = cairo.Context( self._canvas )
        r, g, b= percentColor( strokeColor )
        ctx.set_line_width( strokeWidth )
        ctx.arc(pixx, pixy, radius, 0, 2.0*math.pi)
        ctx.set_source_rgb( r, g, b )
        ctx.stroke()
        return self

    def fillCircle( self, pixx, pixy, radius, fillColor ):
        ctx = cairo.Context( self._canvas )
        r, g, b= percentColor( fillColor )
        ctx.arc(pixx, pixy, radius, 0, 2.0*math.pi)
        ctx.set_source_rgb( r, g, b )
        ctx.fill()
        return self

    def drawCircle( self, pixx, pixy, radius, fillColor, strokeColor, strokeWidth):
        ctx = cairo.Context( self._canvas )
        sr, sg, sb= percentColor(strokeColor)
        fr, fg, fb= percentColor( fillColor )
        ctx.set_line_width(strokeWidth)
        ctx.arc(pixx, pixy, radius, 0, 2.0*math.pi)
        ctx.set_source_rgb( fr, fg, fb )
        ctx.fill_preserve()
        ctx.set_source_rgb( sr, sg, sb )
        ctx.stroke()
        return self
    
    def tracePolygon( self, pixXs, pixYs, strokeColor, strokeWidth ):
        ctx = cairo.Context( self._canvas )
        r, g, b= percentColor(strokeColor)
        ctx.set_line_width(strokeWidth)
        ctx.move_to( pixXs[0], pixYs[0] )
        for pixx, pixy in zip( pixXs[1:], pixYs[1:] ) :
            ctx.line_to(pixx, pixy)
        ctx.close_path()
        ctx.set_source_rgb( r, g, b )
        ctx.stroke()
        return self

    def fillPolygon( self, pixXs, pixYs, fillColor ):
        ctx = cairo.Context( self._canvas )
        r, g, b= percentColor( fillColor )
        ctx.move_to( pixXs[0], pixYs[0] )
        for pixx, pixy in zip( pixXs[1:], pixYs[1:] ) :
            ctx.line_to( pixx, pixy )
        ctx.close_path()
        ctx.set_source_rgb( r, g, b )
        ctx.fill()
        return self

    def drawPolygon( self, pixXs, pixYs, fillColor, strokeColor, strokeWidth ):
        ctx = cairo.Context( self._canvas )
        sr, sg, sb= percentColor(strokeColor)
        fr, fg, fb= percentColor(fillColor)
        ctx.set_line_width(strokeWidth)
        ctx.move_to( pixXs[0], pixYs[0] )
        for pixx, pixy in zip( pixXs[1:], pixYs[1:] ) :
            ctx.line_to(pixx, pixy)
        ctx.close_path()
        ctx.set_source_rgb( fr, fg, fb )
        ctx.fill_preserve()
        ctx.set_source_rgb( sr, sg, sb )
        ctx.stroke()
        return self

    
    # Writting primitives:
    def write( self, pixX, pixY, text, color, fontSize ):
        ctx = cairo.Context( self._canvas )
        r, g, b= percentColor(color)
        ctx.set_font_size(fontSize)
        ctx.set_source_rgb( r, g, b )
        ctx.move_to( pixX, pixY )
        ctx.show_text(text)
        ctx.stroke()
        return self
