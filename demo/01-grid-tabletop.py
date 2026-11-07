#!env python3
import tiledland as tild

# Create a new TiledTabletop as a grid:
tabletop= tild.Tabletop()
tabletop.initGrid(
    [[0, 1, 1, -1, 0, 0, 0, 0],              #  -1 : means no cell at this selector
    [5, -1, 0, 2, 0, -1, 5, 0],              #  0 - n : give the group identifier of the cell to create.
    [0, 0, 0, -1, 0, 1, 1, 0],               #  
    [0, 4, 0, -1, 0, 2, 1, 6],               #  
    [-1, -1, 0, 0, 0, -1, -1, -1]]           #  
)


tabletop.tileAppendEntity(2, tild.Unit(color0x=0x004455))
tabletop.tileAppendEntity(12, tild.Unit(color0x=0x000000))
tabletop.tileAppendEntity(24, tild.Unit(color0x=0x770022))

# Create an artist to render this tabletop:
anArtist= tild.artist.openPNG( "shot-demo.png", 800, 600 )
anArtist.fitBox( tabletop.box() )
tabletop.renderOn(anArtist)
anArtist.flip() # Uptate the support and return to a blanc page.

print( f"You can open now the './{anArtist.support().filePath()}' file." )
