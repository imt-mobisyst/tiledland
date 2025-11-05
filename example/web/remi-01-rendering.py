#!python3
import remi, remi.gui as gui

class MyApp(remi.App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)


    def main(self):
        # Container
        container = gui.VBox( width=400, height=400 )
        self._label = gui.Label( "Salut" )
        self._frame = gui.Svg( width=400, height=300 )
        self._frame.add_child( 'content', '<polygon points="10.0,57.93103448275863 99.65517241379308,57.93103448275863 99.65517241379308,147.58620689655172 10.0,147.58620689655172" style="fill:#ffcd80;stroke:#603800;stroke-width:4" />' )
        container.append(self._frame)
        
        # returning the root widget
        return container

# starts the web server
remi.start(MyApp)
