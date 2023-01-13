#interface gráfica da evolução

from tkinter import *
import random
import time
#import numpy as np
from PIL import ImageTk,Image

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


class environment:
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title("Environment")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        
        self.x = 0
        self.y = 0
        self.start_x = 10
        self.start_y = 10
        self.size = 5

        self.circle = self.canvas.create_oval(self.x, self.y, self.x+self.size, self.y+self.size, fill='#00f')
        self.should_stop = False

    def move(self):
        new_x = random.randint(0,10)
        new_y = random.randint(-10,10)
        self.canvas.move(self.circle, new_x, new_y)
        coordinates = self.canvas.coords(self.circle)
        self.x = coordinates[0]
        self.y = coordinates[1]

        #print('antes',self.x, self.y)

        # if outside screen move to start position
        if(self.y < 10 or self.y>590):
            self.x = self.start_x
            self.y = self.start_y
        if (self.x < 10 or self.x>590):
            self.x = self.start_x
            self.y = self.start_y
        self.canvas.coords(self.circle, self.x, self.y, self.x + self.size, self.y + self.size)
        self.window.after(500, self.move)

    def start(self):
        self.move()
        while True:
            self.window.update()
    


game_instance = environment()
environment.start(game_instance)