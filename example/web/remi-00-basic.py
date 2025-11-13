#!python3
import remi, remi.gui as gui

class MyApp(remi.App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        # Mesages...
        self._msgs= [ "Salut", "nounou !" ]
        self._i= 0
        
        # Container
        container = gui.VBox(width=400, height=400)
        self._label = gui.Label( self._msgs[self._i] )
        self._button = gui.Button('Press me!')

        # setting the listener for the onclick event of the button
        self._button.onclick.do(self.on_button_pressed)

        # appending a widget to another, the first argument is a string key
        container.append(self._label)
        container.append(self._button)

        # returning the root widget
        return container

    # listener function
    def on_button_pressed(self, widget):
        print( "> button pressed !!!" )
        self._i+= 1
        if self._i == len(self._msgs) :
            self._i= 0
        self._label.set_text( self._msgs[self._i] )

# starts the web server
remi.start(MyApp)
