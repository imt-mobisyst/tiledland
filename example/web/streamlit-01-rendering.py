"""
# Simple Scene rendering using streamlit.
"""
import streamlit as st
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

# Connect all close enough tiles: 
scene.connectAllDistance( 1.2 )

# Add some objects on the scene:
def newAgent( identifier, group ):
    return tll.Agent( identifier, group, shape=tll.Shape().initializeRegular(0.7, 6) )

scene.setAgentFactory( newAgent )

bod= scene.popAgentOn(9)
bod.setId(1).setMatter(13)

bod= scene.popAgentOn(14)
bod.setId(2).setMatter(15)

bod= scene.popAgentOn(26)
bod.setId(3).setMatter(13)

# Create an artist to render this scene:
artist= tll.Artist().initializeSVG( filePath= "shot-web-rendering.svg" )
artist.fitBox( scene.box() )
artist.drawScene(scene)

# Rendering in a streamlit widget
widget= st.empty()
widget.write( artist.render(), unsafe_allow_html=True )

artist.flip()
