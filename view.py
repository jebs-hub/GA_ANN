#interface gráfica da evolução

from tkinter import *
import random
import time
from PIL import ImageTk,Image
from model import OrganismBrain

# Define useful parameters
size_of_board = 600
rows = 10
cols = 10
DELAY = 100
snake_initial_length = 3
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 2
RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
Green_color = "#7BC043"

BLUE_COLOR_LIGHT = '#67B0CF'
RED_COLOR_LIGHT = '#EE7E77'

class Organism():

    def __init__(self, canvas,idx):
        self.x = random.randint(0,600)
        self.y = random.randint(0,600)
        self.start_x = random.randint(0,600)
        self.start_y = random.randint(0,600)
        self.size = 5
        self.canvas = canvas
        self.circle = self.canvas.create_oval(self.x, self.y, self.x+self.size, self.y+self.size, fill='#00f')
        self.nn = OrganismBrain(idx)
        self.dead = False
        self.food = Food(self.canvas)
    
    def set_x(self,x):
        self.x = x

    def set_y(self,y):
        self.y = y
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_start_x(self):
        return self.start_x

    def get_start_y(self):
        return self.start_y
    
    def set_canvas(self, canvas):
        self.canvas = canvas
    
    def move(self):
        new_x = random.randint(0,10)
        new_y = random.randint(-10,10)
        self.canvas.move(self.circle, new_x, new_y)
        coordinates = self.canvas.coords(self.circle)
        self.x = coordinates[0]
        self.y = coordinates[1]

        # if outside screen move to start position
        if(self.y < 10 or self.y>590):
            self.x = self.start_x
            self.y = self.start_y
        if (self.x < 10 or self.x>590):
            self.x = self.start_x
            self.y = self.start_y
        self.canvas.coords(self.circle, self.x, self.y, self.x + self.size, self.y + self.size)
    
    def feed(self):
        self.nn.increment_number_of_feeding()

    def die(self, time):
        self.nn.set_time_alive(time)
        self.dead = True
    
    def isDead(self):
        return self.dead

    def reproduce(self):
        return self.nn.copy_with_mutation()

    #TODO how to deal with collision? Here or in the other class
    

class Food():
    
    def __init__(self, canvas):
        self.x = random.randint(0,600)
        self.y = random.randint(0,600)
        self.start_x = random.randint(0,600)
        self.start_y = random.randint(0,600)
        self.size = 7
        self.canvas = canvas
        self.square = self.canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size, fill='#7f3667')
    
    def set_x(self,x):
        self.x = x

    def set_y(self,y):
        self.y = y
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_start_x(self):
        return self.start_x

    def get_start_y(self):
        return self.start_y
    
    def set_canvas(self, canvas):
        self.canvas = canvas

class Poison():
    pass

class environment:
   
    def __init__(self):
        self.window = Tk()
        self.window.title("Environment")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.should_stop = False
        self.orgs = []
        for i in range(100):
            self.orgs.append(Organism(self.canvas,i))

    def move(self):
        for org in self.orgs:
            if(not org.isDead()):
                org.move()
        self.window.after(500, self.move)

    def start(self):
        self.move()
        while True:
            self.window.update()

game_instance = environment()
environment.start(game_instance)