#!env python3
import tiledland as tll

# Create a new Tiled-Map as a grid:
scene= tll.Scene()
scene.initializeSquares(
    [[0, 1, 1, -1, 0, 0, 0, 0],
    [5, -1, 0, 2, 0, -1, 5, 0],
    [0, 0, 0, -1, 0, 1, 1, 0],
    [0, 4, 0, -1, 0, 2, 1, 6],
    [-1, -1, 0, 0, 0, -1, -1, -1]]
)

# Connect all close enough tiles: 
scene.connectAllCondition(
    lambda tileFrom, tileTo : tileFrom.centerDistance( tileTo ) < 1.2
)

# Add some objects on the scene:

# Create an artist to render this scene:
artist= tll.Artist().initializePNG( filePath= "shot-example.png" )
artist.fitBox( scene.box() )
artist.drawScene(scene)
artist.flip() # Uptate the support and return to a blanc page.

print( "You can open now the './shot-example.png' file." )
