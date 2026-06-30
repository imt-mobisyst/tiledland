#!env python3
import tiledland as tll

# Load a gridmap in ROS format:
mapYaml= "map-room3006.yaml"
print( f"Load ./{mapYaml}" )

grid= tll.interface.ros.loadGridMap( ".", mapYaml )
print( f"grid ({grid.dimention()}) at {grid.resolution()} resolution loaded" )


## Load free space (0) with 1.5m radius cells: 
radius= 1.5/grid.resolution()
convexes= grid.makeConvexes(0, radius)

## Instanciate the map with this layer
map= tll.Map(convexes)
tll.draw( map, "shot-demo.png" )

## Add obstables (1), but with a finest definition:
radius= 0.5/grid.resolution()
convexes= grid.makeConvexes(1, radius)
map.createSeveralTiles( convexes, 1 )
tll.draw( map, "shot-demo.png" )

## Finnally connect close cells together :
map.connectAllClose( grid.resolution()*1.001 )
tll.draw( map, "shot-demo.png" )