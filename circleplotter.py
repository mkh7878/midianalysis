# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.graphics import Color, Ellipse
#
# class CircleWidget(Widget):
#     def __init__(self, **kwargs):
#         super(CircleWidget, self).__init__(**kwargs)
#         self.circle_pos = (0, 0)
#
#     def set_circle_position(self, x, y):
#         self.circle_pos = (x, y)
#         self.canvas.clear()
#         with self.canvas:
#             Color(1, 0, 0)
#             Ellipse(pos=(x - 50, y - 50), size=(100, 100))
#
#
# class CircleApp(App):
#     def __init__(self, x, y, **kwargs):
#         self.x = x
#         self.y = y
#         super(CircleApp, self).__init__(**kwargs)
#
#     def build(self):
#         circle_widget = CircleWidget()
#         circle_widget.set_circle_position(self.x, self.y)
#         return circle_widget
#

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty

class MidiEvent(EventDispatcher):
    x_coordinate = NumericProperty(0)
    y_coordinate = NumericProperty(0)

class CircleWidget(Widget):
    def __init__(self, midi_event, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)
        self.midi_event = midi_event
        self.bind(x_coordinate=self.update_circle_x, y_coordinate=self.update_circle_y)

        with self.canvas:
            Color(1, 0, 0)
            self.circle = Ellipse(pos=(self.midi_event.x_coordinate - 50, self.midi_event.y_coordinate - 50), size=(100, 100))

    def update_circle_x(self, instance, value):
        self.circle.pos = (value - 50, self.midi_event.y_coordinate - 50)

    def update_circle_y(self, instance, value):
        self.circle.pos = (self.midi_event.x_coordinate - 50, value - 50)

    def on_key_down(self, window, key, *args):
        step = 10
        if key == 273:  # Up Arrow
            self.midi_event.y_coordinate += step
        elif key == 274:  # Down Arrow
            self.midi_event.y_coordinate -= step
        elif key == 276:  # Left Arrow
            self.midi_event.x_coordinate -= step
        elif key == 275:  # Right Arrow
            self.midi_event.x_coordinate += step

class CircleApp(App):
    def __init__(self, **kwargs):
        super(CircleApp, self).__init__(**kwargs)
        self.midi_event = None

    def build(self):
        Window.bind(on_key_down=self.on_key_down)  # Bind keyboard events to the app
        if self.midi_event:
            circle_widget = CircleWidget(self.midi_event)
            return circle_widget

    def on_key_down(self, window, key, *args):
        # Pass the keyboard events to the CircleWidget
        if self.root:
            self.root.on_key_down(window, key, *args)

def update_coordinates(midi_event, x, y):
    midi_event.x_coordinate = x
    midi_event.y_coordinate = y

# ... (Your existing code for finding MIDI device and other functions)

if __name__ == '__main__':
    # Create the MidiEvent instance
    midi_event = MidiEvent()

    # Start the music function in a separate thread and pass the MidiEvent instance
    music_thread = threading.Thread(target=musicmusic, args=(midi_event,))
    music_thread.start()

    # Run the Kivy app with the MidiEvent instance
    CircleApp(midi_event=midi_event).run()
