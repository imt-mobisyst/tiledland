#!env python3
import tiledland as tll

# Create a new Tiled-Map as a grid:
scene= tll.Scene()
scene.initializeGrid(
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
def newAgent():
    return tll.Agent( shape=tll.Shape().initializeRegular(0.7, 6) )

scene.setAgentConstrutor( newAgent )

bod= scene.popAgentOn(9)
bod.setId(1).setMatter(13)

bod= scene.popAgentOn(14)
bod.setId(2).setMatter(15)

bod= scene.popAgentOn(26)
bod.setId(3).setMatter(13)

# Create an artist to render this scene:
artist= tll.Artist().initializePNG( filePath= "shot-example.png" )
artist.fitBox( scene.box() )
artist.drawScene(scene)
artist.flip() # Uptate the support and return to a blanc page.

print( "You can open now the './shot-example.png' file." )
