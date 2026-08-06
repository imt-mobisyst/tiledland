#!env python3
import tiledland as tll

# Create a new TiledTabletop as a grid:
tabletop= tll.Tabletop()
tabletop.initHexa(
    [[0, 0, 0, -1, 0, 0, 0, 0],              #   -1   : means no cell at this selector
       [0, -1, 0, 0, 0, -1, 0, 0],           #  0 - n : give the group identifier of the cell to create.
     [0, 0, 0, -1, 0, 0, 0, 0],              #  
       [0, 0, 0, -1, 0, 0, 0, 0],            #  
    [-1, -1, 0, 0, 0, -1, -1, -1]]           #  
)

# Add some objects on the tabletop:
def newAgent( identifier, group ):
    ag= tll.Agent( identifier, group, shape=tll.Convex().initRegular(0.7, 6) )
    ag.setMatter(12)
    return ag

tabletop.setAgentFactory( newAgent )

bod= tabletop.popAgentOn(9)

bod= tabletop.popAgentOn(26)
bod.setMatter(13)

bod= tabletop.popAgentOn(14)
bod.setMatter(15)


# Create an artist to render this tabletop:
anArtist= tll.createArtistPNG( "shot-demo.png", 800, 600 )
anArtist.fitBox( tabletop.box() )
tabletop.renderOn(anArtist)
anArtist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{anArtist.support().filePath()}' file." )
