#! /usr/bin/python3
import tiledland as tll
import remi, remi.gui as gui

# Remi :: App
class MyApp(remi.App):
    def __init__(self, *args):
        # Create a new TiledMap as a grid:
        map= tll.Map()
        map.initializeHexa(
            [[0, 0, 0, -1, 0, 0, 0, 0],              #  -1 : means no cell at this location
            [0, -1, 0, 0, 0, -1, 0, 0],              #  0 - n : give the group identifier of the cell to create.
            [0, 0, 0, -1, 0, 0, 0, 0],               #  
            [0, 0, 0, -1, 0, 0, 0, 0],               #  
            [-1, -1, 0, 0, 0, -1, -1, -1]]           #  
        )

        # Add some objects on the map:
        def newAgent( identifier, group ):
            ag= tll.Agent( identifier, group, shape=tll.Convex().initializeRegular(0.7, 6) )
            ag.setMatter(12)
            return ag

        map.setAgentFactory( newAgent )

        bod= map.popAgentOn(9)

        bod= map.popAgentOn(26)
        bod.setMatter(13)

        bod= map.popAgentOn(14)
        bod.setMatter(15)
        #
        self._map= map
        self._artist= tll.Artist()
        self._artist.fitBox( map.box() )
        self._width=800
        self._height=600
        self._clicks= []
        self._selects= []
        super(MyApp, self).__init__(*args)

    def main(self):
        # Container
        container = gui.VBox( width=self._width, height=self._height+100 )
        self._label = gui.Label("Salut")
        self._frame = gui.Svg( width=self._width, height=self._height )
        self._frame.onmousedown.do( self.svg_pressed )
        self._frame.onmouseup.do( self.svg_rel )
        container.append(self._frame)

        # Drawing
        self.draw()

        # returning the root widget
        return container

    def draw(self):
        self._map.draw( self._artist )
        svg= self._artist.content()
        self._frame.add_child( 'content', svg )
        self._artist.clear()
    
    # listener function
    def svg_pressed(self, obj, x, y):
        self._coord= (x, y)

    def svg_rel(self, obj, x, y):
        self.draw()

# starts the web server
remi.start(MyApp, address='0.0.0.0', port=20014)
