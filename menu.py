from kivy.uix.relativelayout import RelativeLayout

class MenuLayout(RelativeLayout):

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return True
        return super(RelativeLayout, self).on_touch_down(touch)