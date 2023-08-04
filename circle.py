
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color

class CircleWidget(Widget):
    def __init__(self, **kwargs):
        super(CircleWidget, self).__init__(**kwargs)
        self.radius = 100  # Default circle radius
        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 0, 1)  # Set circle color (red)
            Ellipse(pos=self.pos, size=self.size)

    def update_width(self, width):
        self.radius = width
        self.update_circle()