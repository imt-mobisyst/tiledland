from . import tile

# Tiled Map Components:
Tile= tile.Tile
#Map= map.Map
#Body2= body.Body2

# Point2 toolbox:

def roundPoint( aPoint, precision=1 ):
    x, y= aPoint
    return (
        round( x, precision ),
        round( y, precision )
    )