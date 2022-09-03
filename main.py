from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy import platform
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.graphics.vertex_instructions import Line, Quad
from kivy.properties import Clock
from kivy.core.window import Window
    
from kivy.lang.builder import Builder

from random import randint

Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import is_desktop, keyboard_closed,on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up
    from inits import on_size, init_horizontal_lines, init_tiles, init_vertical_lines, init_ship
    from get import get_line_x_from_index, get_line_y_from_index, get_tiles_coodinates

    menu_widget = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    number_vertical_lines = 10
    vertical_lines_sp = .3
    vertical_lines = []

    number_horizontal_lines = 15
    horizontal_lines_sp = .1
    horizontal_lines = []

    current_y_loop = 0
    current_offset_y = 0
    SPEED = .01

    SPEED_x = 4
    current_speed_x = 0
    current_offset_x = 0

    number_tiles = 10
    tiles = []
    tiles_coordinates = []

    SHIP_WIDTH = .1
    SHIP_HEIGHT = 0.035
    SHIP_BASE = 0.04
    ship = None
    ship_coordinates = [(0,0), (0,0), (0,0)]

    state_game_over = False
    state_game_started = False

    menu_title = StringProperty("G   A   L   A   X   Y")
    button_title = StringProperty("START")

    points = StringProperty("0")

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down = self.on_keyboard_down)
            self.keyboard.bind(on_key_up = self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1/60)

    def generate_tiles_coordinates(self):
        start_index = -int(self.number_vertical_lines/2) + 1
        end_index = start_index + self.number_vertical_lines - 1
        last_y = 0
        last_x = 0

        for c in range(len(self.tiles_coordinates)-1, -1, -1):
            if self.tiles_coordinates[c][1] < self.current_y_loop:
                del self.tiles_coordinates[c]

        if len(self.tiles_coordinates) > 0:
            last_coordinate = self.tiles_coordinates[-1]
            last_y = last_coordinate[1] + 1
            last_x = last_coordinate[0]

        for i in range(len(self.tiles_coordinates), self.number_tiles):
            r = randint(0, 2)
            self.tiles_coordinates.append((last_x, last_y))
            if last_y >= 10:
                if last_x <= start_index:
                    r = 1
                elif last_x >= end_index - 1:
                    r = 2

                if r == 1:
                    last_x += 1
                    self.tiles_coordinates.append((last_x, last_y))
                    last_y +=1
                    self.tiles_coordinates.append((last_x, last_y))

                elif r == 2:
                    last_x -= 1
                    self.tiles_coordinates.append((last_x, last_y))
                    last_y += 1
                    self.tiles_coordinates.append((last_x, last_y))

            last_y += 1
                
    def update_horizontal_lines(self):
        start_index = -int(self.number_vertical_lines/2) + 1
        end_index = start_index + self.number_vertical_lines - 1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)

        for i in range(0, self.number_horizontal_lines):
            line_y = self.get_line_y_from_index(i)

            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)

            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update_vertical_lines(self):
        start_index = -int(self.number_vertical_lines/2) + 1
        for i in range(start_index, start_index + self.number_vertical_lines):
            line_x = self.get_line_x_from_index(i)

            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def update_tiles(self):
        for i in range(0, self.number_tiles):
            tile = self.tiles[i]
            coordinates = self.tiles_coordinates[i]
            xmin, ymin = self.get_tiles_coodinates(coordinates[0], coordinates[1])
            xmax, ymax = self.get_tiles_coodinates(coordinates[0] + 1, coordinates[1] + 1)

            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_ship(self):
        center_x = self.width/2
        base_y = self.SHIP_BASE * self.height
        ship_width = self.SHIP_WIDTH * self.width
        ship_height = self.SHIP_HEIGHT * self.height

        self.ship_coordinates[0] = (center_x - ship_width/2, base_y)
        self.ship_coordinates[1] = (center_x, base_y + ship_height)
        self.ship_coordinates[2] = (center_x + ship_width/2, base_y)

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self, tile_x, tile_y):
        xmin, ymin = self.get_tiles_coodinates(tile_x, tile_y)
        xmax, ymax = self.get_tiles_coodinates(tile_x + 1, tile_y + 1)

        for i in range(0, 3):
            px, py = self.ship_coordinates[i]
            if px > xmax or px < xmin and py > ymax or py < ymin:
                return False
            
        return True

    def check_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            tile_x, tile_y = self.tiles_coordinates[i]

            if tile_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision(tile_x, tile_y):
                return True
        
        return False

    def start_game(self):
        self.state_game_started = True
        self.state_game_over = False
        self.menu_widget.opacity = 0
        self.points = str(0)

        self.reset_game()

    def reset_game(self):
        self.current_y_loop = 0
        self.current_offset_y = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.SPEED = .005

        self.tiles_coordinates = []
        self.generate_tiles_coordinates()

        self.state_game_over = False

    def update(self, dt):
        time_factor = dt*60
        speed_y = self.SPEED * self.height

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_started:
            self.current_offset_y += speed_y * time_factor
            
            spacing_y = self.horizontal_lines_sp * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.points = str(self.current_y_loop)
                self.generate_tiles_coordinates()
                
                if self.SPEED <= .1:
                    self.SPEED += .0002
                elif self.SPEED <= .2:
                    self.SPEED += .00003
                elif self.SPEED <= .3:
                    self.SPEED += .00002
                else:
                    self.SPEED += .000002

            self.current_offset_x = self.current_speed_x

        if not self.check_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_widget.opacity = 1
            self.button_title = "RESTART"
            self.menu_title = "G  A  M  E    O  V  E  R"


class GalaxyApp(App):
    pass

GalaxyApp().run()
