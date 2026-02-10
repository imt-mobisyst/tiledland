#!env python3
import tiledland as tll

# Create a new TiledMap as a grid:
scene= tll.Scene()
scene.initializeGrid(
    [[0, 1, 1, -1, 0, 0, 0, 0],              #  -1 : means no cell at this location
    [5, -1, 0, 2, 0, -1, 5, 0],              #  0 - n : give the group identifier of the cell to create.
    [0, 0, 0, -1, 0, 1, 1, 0],               #  
    [0, 4, 0, -1, 0, 2, 1, 6],               #  
    [-1, -1, 0, 0, 0, -1, -1, -1]]           #  
)

# Agent 1
agent= scene.popAgentOn(9)

# Agent 2
agent= scene.popAgentOn(26)
agent.setMatter(13)

# Agent 3
agent= scene.popAgentOn(14)
agent.setMatter(15)

# Create an artist to render this scene:
artist= tll.Artist().initializePNG( "shot-example.png", 600, 800 )
# artist= tll.Artist().initializePNG( filePath= "shot-example.png" )  ## Require cairo (pip install pycairo)
artist.fitBox( scene.box() )
artist.drawScene(scene)
artist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{artist.support().filePath()}' file." )
