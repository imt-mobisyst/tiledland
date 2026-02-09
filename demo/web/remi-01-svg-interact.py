#!python3
import remi, remi.gui as gui

class MyApp(remi.App):
    def __init__(self, *args):
        self._height=300
        self._width=400
        self._clicks= []
        self._selects= []
        super(MyApp, self).__init__(*args)

    def main(self):
        # Container
        container = gui.VBox( width=400, height=400 )
        self._label = gui.Label("Salut")
        self._frame = gui.Svg( width=400, height=300 )
        self._frame.onmousedown.do( self.svg_pressed )
        self._frame.onmouseup.do( self.svg_rel )
        container.append(self._frame)

        # Drawing
        self.draw()

        # returning the root widget
        return container

    def draw(self):
        svg= f'<polygon points="0,0 {self._width},0 {self._width},{self._height} 0,{self._height}" style="fill:#ffcd80;stroke:#603800;stroke-width:4" />'
        for x, y in self._clicks : 
            svg+= f'<circle r="4" cx="{x}" cy="{y}" fill="#a01010" />'
        for x1, y1, x2, y2 in self._selects : 
            svg+= f'<polygon points="{x1},{y1} {x1},{y2} {x2},{y2} {x2},{y1}" style="fill:none;stroke:#a01010;stroke-width:2" />'

        self._frame.add_child( 'content', svg )
    
    # listener function
    def svg_pressed(self, obj, x, y):
        self._coord= (x, y)

    def svg_rel(self, obj, x, y):
        if self._coord == (x, y) :
            self._clicks.append( self._coord )
        else :
            x1, y1= self._coord
            self._selects.append( (x1, y1, x, y) )
    
    
    def idle(self):
        self.draw()

# starts the web server
remi.start(MyApp, address='0.0.0.0', port=20014, update_interval=0.1)
