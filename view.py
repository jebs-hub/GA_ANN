#interface gráfica da evolução

from tkinter import *
import random
import time
from PIL import ImageTk,Image
from model import OrganismBrain
import math

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
        self.start = time.time()
    
    def input_information(self):
        self.nn.set_food_location([self.food.get_x(), self.food.get_y()])
    
    def reaction(self):
        return self.nn.get_command()
    
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
    
    def treat_collision(self):
        x_food = self.food.get_x()
        y_food = self.food.get_y()
        distance = math.sqrt(((x_food-self.x)**2+(y_food-self.y)**2))
        if(distance<=5):
            #collision
            self.feed()
    
    def move(self):
        self.input_information()
        new_x = self.x 
        new_y = self.y
        direction = self.reaction()
        if(direction=="up"):
            new_y = 1
        if(direction=="down"):
            new_y = -1
        if(direction=="right"):
            new_x = 1
        if(direction=="left"):
            new_x = -1

        self.canvas.move(self.circle, new_x, new_y)
        coordinates = self.canvas.coords(self.circle)
        self.x = coordinates[0]
        self.y = coordinates[1]

        # if outside screen move to start position
        if(self.y < 10 or self.y>590):
            self.die(time.time()-self.start)
        if (self.x < 10 or self.x>590):
            self.die(time.time()-self.start)
        self.canvas.coords(self.circle, self.x, self.y, self.x + self.size, self.y + self.size)

        if(not self.dead): #detect collision
            self.treat_collision()

    
    def feed(self):
        self.nn.increment_number_of_feeding()
        old = self.food 
        self.food = Food(self.canvas)
        old.eat()

    def die(self, time):
        self.nn.set_time_alive(time)
        self.dead = True
    
    def isDead(self):
        return self.dead

    def reproduce(self):
        return self.nn.copy_with_mutation()
     
    def isSelected(self):
        if((not self.dead) and self.nn.number_of_feeding>=1):
            #print(not self.dead, self.nn.number_of_feeding)
            return True 
        else: 
            return False

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

    def eat(self):
        self.canvas.delete(self.square)

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
        for i in range(2000):
            self.orgs.append(Organism(self.canvas,i))
        self.start = time.time()

    def move(self):
        for org in self.orgs:
            if(not org.isDead()):
                org.move()
        if(time.time()-self.start<=5):
            self.window.after(500, self.move)
    
    def select(self):
        survivors = 0
        full = 0
        for o in self.orgs:
            if(o.isSelected()):
                print("SUCCED")
            if(not o.isDead()):
                survivors+=1
            if(o.nn.number_of_feeding>0):
                full+=1
        print(survivors, full)

    def start(self):
        self.move()
        while (time.time()-self.start<=3):
            self.window.update()
        self.select()

game_instance = environment()
environment.start(game_instance)