#!env python3
import tiledland as tild

# Load a gridmap in ROS format:
mapYaml= "map-room3006.yaml"
print( f"Load ./{mapYaml}" )

grid= tild.interface.ros.loadGridMap( ".", mapYaml )
print( f"grid ({grid.dimention()}) at {grid.resolution()} resolution loaded" )


## Load free space (0) with 1.5m radius cells: 
radius= 1.5/grid.resolution()
convexes= grid.makeConvexes(0, radius)

## Instanciate the tabletop with this layer
tabletop= tild.Tabletop(convexes)
tild.draw( tabletop, "shot-demo.png" )

## Add obstables (1), but with a finest definition:
radius= 0.5/grid.resolution()
convexes= grid.makeConvexes(1, radius)
tabletop.createSeveralTiles( convexes, 1 )
tild.draw( tabletop, "shot-demo.png" )

## Finnally connect close cells together :
tabletop.connectAllClose( grid.resolution()*1.001 )
tild.draw( tabletop, "shot-demo.png" )