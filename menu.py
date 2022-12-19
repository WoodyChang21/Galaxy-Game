from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty

class MenuWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            #When the menu widget opacity = 0, it means the game is going
            #Then the touch down function in the menuwidget shouldn't be working
            #Can't click the button
            return False
        #menu.opacity != 0 and rank is showing
        elif self.parent.rank_widget.opacity != 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)