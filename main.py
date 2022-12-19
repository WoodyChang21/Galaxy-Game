from kivy.core.window import Window
#This set up the window size
Window.size = (900,400)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, Clock, StringProperty, ObjectProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line, Rectangle, Ellipse, Quad, Triangle
from kivy import platform
from kivy.uix.relativelayout import RelativeLayout
from kivy.lang.builder import Builder
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
import random, time
import pymongo

Builder.load_file("rank.kv")
Builder.load_file("menu.kv")

class MainWidget(RelativeLayout):
    from transforms import transform, transform_2D, transform_perspective
    from user_actions import on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up, keyboard_closed
    from bestscore_db import update_bestscore, update_bestscore_class, rank
    #Create properties for galaxy kv file to use
    menu_widget = ObjectProperty()
    rank_widget = ObjectProperty()
    bestscore = ObjectProperty()
    current_score = ObjectProperty()
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)
    
    number_vertical_lines = 8
    vertical_lines = []
    vertical_lines_spacing = .2 #percentage in screen width

    number_horizontal_lines = 15
    horizontal_lines = []
    horizontal_lines_spacing = .15 #percentage in screen height

    number_tiles = 20
    tile = []
    ti_x = 1
    ti_y = 5
    tiles_coordinates = []

    current_offset_y = 0
    speed = .2
    current_y_loop = 0

    current_offset_x = 0
    speedx = 11
    current_speed_x = 0

    ship = None
    ship_width = .1
    ship_height = 0.035
    ship_base_y = 0.04
    ship_coordinates = [(0,0),(0,0),(0,0)]

    state_game_over = False
    state_game_started = False
    rank_state = False

    menu_button_string = StringProperty("")
    menu_label_string = StringProperty("")

    score_txt = NumericProperty(0)
    bestscore_txt = NumericProperty(update_bestscore(0))


    #SOUND
    sound_begin = None
    sound_galaxy = None
    sound_gameover_impact = None
    sound_gameover_voice = None
    sound_music1 = None
    sound_restart = None

    def __init__(self,**kwargs):
        #super().__init__() is same as calling "Inheritclass.__init__()"
        #It is a way of calling the parent class without explicitly write it out
        #super can take two arguments (subclass, self)
        #super taking arguments is equivalent to super not taking arguments
        super(MainWidget, self).__init__(**kwargs)
        # the self.width and self.height is still the widget default value (100,100), since __init__ is the very first program to run
        # print(f'Width and height without updated yet: {self.width}, {self.height}')
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.pre_fill_tiles_coordinates()
        self.generate_tile_coordinate()
        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update,1/60)
        self.sound_galaxy.play()
    
    def init_audio(self):
        self.sound_begin = SoundLoader.load("audio/begin.ogg")
        self.sound_galaxy = SoundLoader.load("audio/galaxy.ogg")
        self.sound_gameover_impact = SoundLoader.load("audio/gameover_impact.ogg")
        self.sound_gameover_voice = SoundLoader.load("audio/gameover_voice.ogg")
        self.sound_music1 = SoundLoader.load("audio/music1.ogg")
        self.sound_restart = SoundLoader.load("audio/restart.ogg")

        self.sound_music1.volume = 1
        self.sound_begin.volme = .25
        self.sound_galaxy.volume =.25
        self.sound_gameover_impact.volume =.25
        self.sound_restart.volume = .25
        self.sound_gameover_voice.volume = .5

    def reset_game(self):
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_offset_x = 0
        self.score_txt = self.current_y_loop
        self.bestscore_txt = self.update_bestscore_class(self.score_txt)

        self.tiles_coordinates = []
        self.pre_fill_tiles_coordinates()
        self.generate_tile_coordinate()
        self.state_game_over = False
    
    def is_desktop(self):
        #The platform returns the device you're using
        if platform in ('linux','win','macosx'):
            return True
        return False

    #built in kivy function
    #it will triggers when the parent changes
    def on_parent(self,*args):
        pass

    #built in kivy function
    #It will triggers when the size of the windows change
    def on_size(self,*args):
        #The two lines at the bottom can also be called in kivy file
        #Uncomment the below two lines if they aren't in kv file
        # self.perspective_point_x = self.width/2
        # self.perspective_point_y = self.height*0.75
        pass
            
    #Variable "property_point_x" and "property_point_y" is created under widget class
        #Therefore, property object will live at the class level and manage the values attatec to instances
    #Observe when the property changes for vairable "perpective_point_x"
    #Use on_property(self, class_instance, value) to keep track the changes of the property
    def on_perspective_point_x(self, widget, value):
        #The passed in argument value is the new value
        # print(f"PX: {value}")
        pass
    def on_perspective_point_y(self, widget, value):
        #The passed in argument value is the new value
        # print(f"PY: {value}")
        pass    

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            #Since we call it from init, the self.width and self.height hasn't yet be updated
            #self.width and self.height is onnly updated when the window size changed
            #self.line = Line(points=[self.width/2,0,self.width/2,self.height])

            for i in range(0, self.number_vertical_lines):
                #Create i line objects in the vertical_lines list
                self.vertical_lines.append(Line())
    
    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)

            for i in range(0, self.number_horizontal_lines):
                #Create i line objects in the vertical_lines list
                self.horizontal_lines.append(Line())
    
    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0,self.number_tiles):
                self.tile.append(Quad())
    
    def pre_fill_tiles_coordinates(self):
        #Add 10 tiles in a straight line
        for i in range(0,11):
            self.tiles_coordinates.append((0,i))
    
    def init_ship(self):
        with self.canvas:
            Color(0,0,0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width/2
        base_y = self.ship_base_y*self.height
        ship_width = self.ship_width*self.width
        ship_height = self.ship_height*self.height

        self.ship_coordinates[0] = center_x-ship_width/2,base_y
        self.ship_coordinates[1] = center_x, base_y+ship_height
        self.ship_coordinates[2] = center_x+ship_width/2, base_y

        #The star sign expand the tuple to view it as two arguments
        x1, y1 = self.transform(*self.ship_coordinates[0] )
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])
        self.ship.points = [x1,y1,x2,y2,x3,y3]


    def generate_tile_coordinate(self):
        #Clean the coordinates that are out of the screen
        #ti_y<self.current_y_loop

        start_index = -int(self.number_vertical_lines/2)+1
        end_index = start_index + self.number_vertical_lines-1
        last_x = int(start_index+self.number_vertical_lines/2-1)
        last_y = 0
        #This iterates through the list in reverse
        for i in range(len(self.tiles_coordinates)-1,-1,-1):
            #The self.current_y_loop basically also records how many tiles has passed
            if self.tiles_coordinates[i][1]<self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1]+1

        #This limitted the iteration times to only the empty space
        for i in range(len(self.tiles_coordinates),self.number_tiles):
            random_x_position =  random.randint(0,2)
            #0: straight
            #1: right
            #2: left
            if (last_x<=start_index):
                random_x_position = random.choice([0,1])
            if (last_x>=end_index-1):
                random_x_position = random.choice([0,2])

            self.tiles_coordinates.append((last_x,last_y))
                
            if random_x_position ==1:
                last_x += 1
                self.tiles_coordinates.append((last_x,last_y))
                last_y+=1
                self.tiles_coordinates.append((last_x,last_y))
            if random_x_position == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x,last_y))
                last_y+=1
                self.tiles_coordinates.append((last_x,last_y))
            last_y+=1

                


    #The vertical lines
    def get_line_x_from_index(self,index):
        central_line_x = self.perspective_point_x
        spacing = self.vertical_lines_spacing*self.width
        offset = index-0.5
        #Have to track which specific line we're referring to; therefore, needse to add the current_offset_x
        #Adding the self.current_offset_x can shift everything to the right or the left
            #ex. self.current_off_set_x = 2 (Then every lines are moved to the right by 2)
        line_pos_x = central_line_x + offset*spacing + self.current_offset_x
        return line_pos_x


    def update_vertical_lines(self):
        #If there are 4 lines (-1,0,1,2): The start_index = -1
        start_index = -int(self.number_vertical_lines/2)+1
        for i in range(start_index, start_index+self.number_vertical_lines):
            line_pos_x = self.get_line_x_from_index(i)
            #defines the two points
            #here self.width, self.height has changed since the window has popped out --> self.width, self.height change automatically
            x1,y1 = self.transform(line_pos_x,0)
            x2,y2 = self.transform(line_pos_x,self.height)
            self.vertical_lines[i].points = [x1,y1,x2,y2]

    def get_line_y_from_index(self,index):
        start_line_y = 0
        spacing = self.horizontal_lines_spacing*self.height
        # line_pos_y = start_line_y + index*spacing
        line_pos_y = start_line_y + index*spacing - self.current_offset_y
        return line_pos_y

    def update_horizontal_lines(self):
        start_index = -int(self.number_vertical_lines/2)+1
        end_index = start_index + self.number_vertical_lines-1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)
        for i in range(0, self.number_horizontal_lines):
            line_pos_y = self.get_line_y_from_index(i)
            x1,y1 = self.transform(xmin,line_pos_y)
            x2,y2 = self.transform(xmax,line_pos_y)
            self.horizontal_lines[i].points = [x1,y1,x2,y2]

    def get_tile_coorindates(self, ti_x, ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x,y
    
    #Bottom left is (xmin, ymin)
    #Upper left is (xmin, ymax)
    #Upper right is (xmax, ymax)
    #Bottom right is (xmax, ymin)
    def update_tile(self):
        for i in range(0,self.number_tiles):
            ti_x,ti_y = self.tiles_coordinates[i]
            #This lock the tile at a specific vertical line and horizontal line position
            #Therefore, even the line moves, it follows the line
            xmin, ymin = self.get_tile_coorindates(ti_x, ti_y)
            xmax, ymax = self.get_tile_coorindates(ti_x+1, ti_y+1)

            x1,y1 = self.transform(xmin, ymin)
            x2,y2 = self.transform(xmin, ymax)
            x3,y3 = self.transform(xmax, ymax)
            x4,y4 = self.transform(xmax, ymin)

            #update the tile
            self.tile[i].points = [x1,y1,x2,y2,x3,y3,x4,y4]


    #If it is still on the track, then it will return True
    #return false if the ship is not on the track
    def check_ship_collision(self):
        for i in range(0, len(self.tiles_coordinates)):
            ti_x, ti_y = self.tiles_coordinates[i]
            #This checks only the first two column of the tiles
            #return False if the coordinates are not in the first two blocks
            # So it will exit the function, since no need to check
            if ti_y > self.current_y_loop+1:
                return False
                
            if self.check_ship_collision_with_tile(ti_x, ti_y):
                return True
        return False

    #It will return True if one of the point is still on the track
    def check_ship_collision_with_tile(self,ti_x,ti_y):
        xmin, ymin = self.get_tile_coorindates(ti_x,ti_y)
        xmax, ymax = self.get_tile_coorindates(ti_x+1,ti_y+1)

        for i in range(0,3):
            #px, py contains the coordinate of the ship
            px, py = self.ship_coordinates[i]
            #If one of the point is still in the track then just return True
            if xmin <= px <= xmax and ymin <= py <= ymax:
                return True
        return False
    
    #This function is called regularly (60 times per second)
    #dt: delta time 
        #The actual time between the previous time when the function is called 
    def update(self, dt):
        #Offset the actual time difference
        #This is the actual time of the update function being called 60 times
        time_factor = dt*60
       
        horizontal_line_spacing = self.horizontal_lines_spacing*self.height

        #The game hasn't started yet, gameover = false
        if not self.state_game_over and not self.state_game_started:
            self.menu_button_string = "START"
            self.menu_label_string = "G   A   L   A   X   Y"
            if self.rank_state == False:
                self.rank_widget.opacity = 0
        #Not game over and game has started
        if not self.state_game_over and self.state_game_started:
            #To make the speed consistenet no matter what window size
            self.speed = self.height*1/150
            #increase the speed as user plays
            self.speed += self.height * int(self.current_y_loop/30)/1500
            #If dt*60 is 2 (the actual time of running the update function 60 times is 2 sec, supposed to be 1 sec)
                #Then the speed should be faster to offset the real time difference
                    #This offset will make the speed the same no matter the real time delay is
            self.current_offset_y+= self.speed*time_factor
            #This means when one horizontal line is compeletely gone
            #set the offset_y back to 0, so the update_horizontal_line will redraw the initial horizontal lines
            #Conclusion: when one line vanished, redraw it
            while self.current_offset_y >= horizontal_line_spacing:
                self.current_offset_y -= horizontal_line_spacing
                self.current_y_loop+=1
                #record how many loops has passed
                self.score_txt = self.current_y_loop
            
            #To makes the speed constant in no matter what size
            self.speedx = self.width*15/900
            self.current_offset_x += self.current_speed_x*time_factor

        # These two functions are called 60 times every second
        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tile()
        self.generate_tile_coordinate()
        self.update_ship()

        #self.check_ship_collision = False (ship is not on the track), self.state_game_over = False (Still playing)
        if not self.check_ship_collision() and not self.state_game_over:
            self.menu_button_string = "RESTART"
            self.menu_label_string = "G A M E  O V E R"
            self.state_game_over = True
            self.sound_music1.stop()
            self.sound_gameover_impact.play()
            self.sound_gameover_voice.play()
            self.menu_widget.opacity = 1
            if (self.score_txt)> self.update_bestscore_class(0):
                self.bestscore_animation(True)
            self.bestscore_txt=self.update_bestscore_class(self.score_txt)
        
    def on_menu_button_pressed(self): 
        self.reset_game()
        self.state_game_started = True
        self.menu_widget.opacity = 0
        if self.menu_button_string == "START":
            self.sound_begin.play()
        if self.menu_button_string == "RESTART":
            self.bestscore_animation(False)
            self.sound_restart.play()
        self.sound_music1.loop = True
        self.sound_music1.play()
    
    def on_rank_button_pressed(self):
        #Show rank (Trigger point)
        if self.rank_widget.opacity == 0:
            self.rank_widget.opacity = .8
            self.rank_state = True
        

    def bestscore_animation(self, check):
        anim = Animation(color=(1,.3,.2,1), duration = .2) +  Animation(color=(1, 1, 1, 1), duration=.2)
        anim.repeat = True
        anim.start(self.bestscore)
        anim.start(self.current_score)
        if not check:
            anim.stop_all(self.bestscore)
            anim.stop_all(self.current_score)
            self.bestscore.color = (1,1,1,1)
            self.current_score.color = (1,1,1,1)
    
    def update_rank(self):
        bestscore_list = []
        bestscore_list = self.rank()
        self.rank_widget.ids.one.text = f"1: {bestscore_list[0]}"
        self.rank_widget.ids.two.text = f"2: {bestscore_list[1]}"
        self.rank_widget.ids.three.text = f"3: {bestscore_list[2]}"
        self.rank_widget.ids.four.text = f"4: {bestscore_list[3]}"
        self.rank_widget.ids.five.text = f"5: {bestscore_list[4]}"

        # self.one = StringProperty(str(bestscore_list[0]))
        # self.two = StringProperty(str(bestscore_list[1]))
        # self.three = StringProperty(str(bestscore_list[2]))
        # self.four = StringProperty(str(bestscore_list[3]))
        # self.five = StringProperty(str(bestscore_list[4]))



class GalaxyApp(App):
    pass

GalaxyApp().run()