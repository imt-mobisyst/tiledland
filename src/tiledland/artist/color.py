# Color transform:

def decompose(color):
    return (color>>16)&0xFF, (color>>8)&0xFF, (color)&0xFF

def compose(r, g, b):
    r= min( max(0, r), 0xFF)
    g= min( max(0, g), 0xFF)
    b= min( max(0, b), 0xFF)
    return (r&0xFF)<<16 | (g&0xFF)<<8 | b&0xFF

def lightest(color, ratio):
    r, g, b= decompose(color)
    r= r + int( (0x100-r)*ratio )
    g= g + int( (0x100-g)*ratio )
    b= b + int( (0x100-b)*ratio )
    return compose(r, g, b)

def darckest(color, ratio):
    r, g, b= decompose(color)
    r= int( r*ratio )
    g= int( g*ratio )
    b= int( b*ratio )
    return compose(r, g, b)

def fromWeb( aWebColor ):
    return int( aWebColor[1:], base=16)

def percent( color ):
    r, g, b= decompose(color)
    ratio= 1.0/0xff
    return round(r*ratio, 4), round(g*ratio, 4), round(b*ratio, 4)

def web( color ):
    string= '#'
    for c in decompose( color ) :
        string+= hex( (c>>4)&0xF )[2]
        string+= hex( c&0xF )[2]
    return string

def ratio( color, ratio ):
    r,g,b= decompose( color )
    r= int( r*ratio )
    g= int( g*ratio )
    b= int( b*ratio )
    return compose(r, g, b)
 