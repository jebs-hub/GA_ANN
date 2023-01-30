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

    def __init__(self,canvas,idx,nn=None):
        self.x = random.randint(0,600)
        self.y = random.randint(0,600)
        self.start_x = random.randint(0,600)
        self.start_y = random.randint(0,600)
        self.size = 5
        self.canvas = canvas
        self.circle = self.canvas.create_oval(self.x, self.y, self.x+self.size, self.y+self.size, fill='#00f')
        if(nn==None):
            self.nn = OrganismBrain(idx)
        else:
            self.nn = nn
        self.dead = False
        self.food = Food(self.canvas)
        self.start = time.time()
    
    def input_information(self):

        d_wall_up = self.y
        d_wall_down = 600-self.y
        d_wall_right = 600-self.x
        d_wall_left = self.x

        d_food_up = self.y-self.food.get_y()
        d_food_right = self.food.get_x()-self.x

        self.nn.sense_environment([d_wall_up,d_wall_down,d_wall_right,d_wall_left,d_food_up,-d_food_up,d_food_right,-d_food_right])
    
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
    
    def get_distance(self,point1, point2):
        return math.sqrt(((point1[0]-point2[0])**2+(point1[1]-point2[1])**2))
    
    def treat_collision(self):
        x_food = self.food.get_x()
        y_food = self.food.get_y()
        distance = self.get_distance([x_food,y_food],[self.x, self.y])
        if(distance<=15):
            #collision
            self.feed()
    
    def move(self):
        self.input_information()
        direction = self.reaction()
        if(direction=="up"):
            self.y -= 2
        if(direction=="down"):
            self.y += 2
        if(direction=="right"):
            self.x -= 2
        if(direction=="left"):
            self.x += 2

        self.canvas.move(self.circle, self.x, self.y)

        # if outside screen move to start position
        if(self.y < 10 or self.y>590):
            self.die(time.time()-self.start)
        if (self.x < 10 or self.x>590):
            self.die(time.time()-self.start)
        #self.canvas.coords(self.circle, self.x, self.y, self.x + self.size, self.y + self.size)

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
        brain = self.nn.copy_with_mutation()
        return Organism(self.canvas, 0,nn=brain)
     
    def isSelected(self):
        if((not self.dead) and self.nn.number_of_feeding>=1):
            #print(not self.dead, self.nn.number_of_feeding)
            return True 
        else: 
            return False
    
    def remove(self):
        self.canvas.delete(self.circle)
        self.food.eat()

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
        self.gen = 1

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
        self.start_time = time.time()
        self.gen = 0

    def move(self):
        for org in self.orgs:
            if(not org.isDead()):
                org.move()
        if(time.time()-self.start_time<=5):
            self.window.after(500, self.move)
    
    def select(self):
        survivors = []
        #full = 0
        #success = 0
        for o in self.orgs:
            if(o.isSelected()):
                print("SUCCED")
                survivors.append(o)
            else: ##kill
                o.remove()
            self.organisms = []
            if(len(survivors)>0):
                number_of_decendents = 2000//len(survivors)
                for o in survivors:
                    self.organisms.append(o)
                    for i in range(0,number_of_decendents):
                        new = o.reproduce()
                        self.organisms.append(new)
                self.gen+=1
                print("gen {}".format(self.gen))
                self.start()
            #if(not o.isDead()):
             #   survivors+=1
            #if(o.nn.number_of_feeding>0):
                #full+=1
        #print(survivors, full)

    def start(self):
        self.move()
        while (time.time()-self.start_time<=3):
            self.window.update()
        self.select()

game_instance = environment()
environment.start(game_instance)