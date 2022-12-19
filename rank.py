from kivy.uix.relativelayout import RelativeLayout

class RankWidget(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            #When the menu widget opacity = 0, it means the game is going
            #Then the touch down function in rankwidget shouldn't be working
            #Can't click the button
            return False
        #If rank is showing and touch down it should go back
        else:
            self.opacity = 0
            self.parent.rank_state = False
        return super(RelativeLayout, self).on_touch_down(touch)