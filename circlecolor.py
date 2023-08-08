#this code draws a circle on a kivy window
#then it adjusts the color of the circle using RGB keys. The values run up and down between 0 and 1
#when you reach 1 it goes down again and when you reach 0 it goes up
#also, the circle moves using arrow keys

# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color
from kivy.clock import Clock


class CircleWidget(Widget):
    def __init__(self, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (400, 400)
        # circle_red = 1
        # circle_green = 1
        # circle_blue = 1

        with self.canvas:  # Draw a blue circle
            self.circle_color = Color(1, 1, 1)  # Initialize color
            self.circle = Ellipse(pos=(150, 150), size=(100, 100))

        self.keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self.keyboard.bind(on_key_down=self._on_key_down)

        # Schedule the update function to be called every frame
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        # Store the circle's position deltas
        self.delta_x = 0
        self.delta_y = 0


    def _keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_key_down)
        self.keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        key = keycode[1]
        #print(key)
        if key == 'left':
            self.delta_x = -10
        elif key == 'right':
            self.delta_x = 10
        elif key == 'up':
            self.delta_y = 10
        elif key == 'down':
            self.delta_y = -10
        elif key == 'r':
            self.adjust_color('r', 0.05)
        elif key == 'g':
            self.adjust_color('g', 0.05)
        elif key == 'b':
            self.adjust_color('b', 0.05)

    def update(self, dt):
        # Update the circle's position based on deltas
        self.circle.pos = (self.circle.pos[0] + self.delta_x, self.circle.pos[1] + self.delta_y)

        # Reset deltas
        self.delta_x = 0
        self.delta_y = 0

    #true is up, false is down
    triggers = {
        'r' : False,
        'g' : False,
        'b' : False
    }

    def adjust_color(self, channel, dt):
        channel_value = getattr(self.circle_color, channel)
        print(channel)
        print(channel_value)
        #innitialize new value
        new_value = channel_value
        if channel_value > 1:
            self.triggers[channel] = False
        elif channel_value < 0:
            self.triggers[channel] = True

        #UP
        if self.triggers[channel]:
            new_value += dt
        #DOWN
        else:
            new_value -= dt

        new_value = round(new_value, 2)
        setattr(self.circle_color, channel, new_value)

        # Call the update function to trigger the rendering of the new color
        self.update(0)
class CircleApp(App):
    def build(self):
        circle_widget = CircleWidget()
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Use arrow keys to control the circle's position."))
        layout.add_widget(circle_widget)
        return layout


if __name__ == '__main__':
    CircleApp().run()
