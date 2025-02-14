# Color transform:

def color( red, green, blue ):
    if red > 0xFF :
        red= 0xFF
    if green > 0xFF :
        green= 0xFF
    if blue > 0xFF :
        blue= 0xFF
    return (red<<16) + (green<<8) + (blue)

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

def colorRatio( color, ratio ):
    r,g,b= rgbColor( color )
    r= int( r*ratio )
    g= int( r*ratio )
    b= int( r*ratio )
    return color
 