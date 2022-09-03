from kivy.uix.relativelayout import RelativeLayout
from kivy import platform

def is_desktop(self):
    if platform in ('linux', 'win', 'macosx'):
        return True
    else:
        return False

def keyboard_closed(self):
    self.keyboard.unbind(on_key_down = self.on_keyboard_down)
    self.keyboard.unbind(on_key_up = self.on_keyboard_up)
    self.keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x += self.vertical_lines_sp * self.width

        if keycode[1] == 'right':
            self.current_speed_x += -self.vertical_lines_sp * self.width

        return True

def on_keyboard_up(self, keyboard, keycode):
    return True

def on_touch_down(self, touch):
    if not self.state_game_over and self.state_game_started:
        if touch.x < self.width/2:
            self.current_speed_x += self.vertical_lines_sp * self.width
        else:
            self.current_speed_x += -self.vertical_lines_sp * self.width

    return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    return True