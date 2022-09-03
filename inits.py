from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Quad, Triangle

def on_size(self, *args):
        self.perspective_point_x = self.width/2
        self.perspective_point_y = self.height * 0.75

def init_vertical_lines(self):
    with self.canvas:
        Color(1, 1, 1)
        for i in range(0, self.number_vertical_lines):
            self.vertical_lines.append(Line())

def init_horizontal_lines(self):
    with self.canvas:
        Color(1, 1, 1)
        for i in range(0, self.number_horizontal_lines):
            self.horizontal_lines.append(Line())

def init_tiles(self):
    with self.canvas:
        Color(1, 1, 1)
        for i in range(0, self.number_tiles):
            self.tiles.append(Quad())

def init_ship(self):
    with self.canvas:
        Color(0, 0, 0)
        self.ship = Triangle()