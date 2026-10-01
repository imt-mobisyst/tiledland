# Color transform:

def decompose(color):
    return (color>>16)&0xFF, (color>>8)&0xFF, (color)&0xFF

def recompose(r, g, b):
    return (r&0xFF)<<16 | (g&0xFF)<<8 | b&0xFF

def lightest(color, ratio):
    r, g, b= decompose(color)
    r= r + int( (0x100-r)*ratio )
    g= g + int( (0x100-g)*ratio )
    b= b + int( (0x100-b)*ratio )
    return recompose(r, g, b)

def darckest(color, ratio):
    r, g, b= decompose(color)
    r= int( r*ratio )
    g= int( g*ratio )
    b= int( b*ratio )
    return recompose(r, g, b)

def colorFromWeb( webColor ):
    return int( webColor[1:], base=16)

def rgbColor( color ):
    b= (color & 0xFF)
    var= color >> 8
    g= (var & 0xFF)
    var= var >> 8
    r= (var & 0xFF)
    return (r, g, b)

def percentColor( color ):
    r, g, b= rgbColor(color)
    ratio= 1.0/0xff
    return round(r*ratio, 4), round(g*ratio, 4), round(b*ratio, 4)

def webColor( color ):
    string= '#'
    for c in rgbColor( color ) :
        string+= hex( (c>>4)&0xF )[2]
        string+= hex( c&0xF )[2]
    return string

def oldColorRatio( color, ratio ):
    r,g,b= rgbColor( color )
    r= int( r*ratio )
    g= int( r*ratio )
    b= int( r*ratio )
    return color
 