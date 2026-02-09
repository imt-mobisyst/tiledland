#!env python3
import tiledland as tll

# Create a new TiledMap as a grid:
scene= tll.Scene()
scene.initializeHexa(
    [[0, 0, 0, -1, 0, 0, 0, 0],              #  -1 : means no cell at this location
       [0, -1, 0, 0, 0, -1, 0, 0],              #  0 - n : give the group identifier of the cell to create.
     [0, 0, 0, -1, 0, 0, 0, 0],               #  
       [0, 0, 0, -1, 0, 0, 0, 0],               #  
    [-1, -1, 0, 0, 0, -1, -1, -1]]           #  
)

# Add some objects on the scene:
def newAgent( identifier, group ):
    ag= tll.Agent( identifier, group, shape=tll.Convex().initializeRegular(0.7, 6) )
    ag.setMatter(12)
    return ag

scene.setAgentFactory( newAgent )

bod= scene.popAgentOn(9)

bod= scene.popAgentOn(26)
bod.setMatter(13)

bod= scene.popAgentOn(14)
bod.setMatter(15)


# Create an artist to render this scene:
artist= tll.Artist().initializePNG( filePath= "shot-example.png" )
# artist= tll.Artist().initializePNG( filePath= "shot-example.png" )  ## Require cairo (pip install pycairo)
artist.fitBox( scene.box() )
artist.drawScene(scene)
artist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{artist.support().filePath()}' file." )
