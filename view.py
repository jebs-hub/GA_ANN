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

class Organism(): #TODO need to change time alive considering the generations, change fitness score to considere survivor
                                                       #score = (time alive) * (0.1+number of feeding)
    def __init__(self,canvas,idx,ancestral,nn=None):
        self.start_x = random.randint(0,600)
        self.start_y = random.randint(0,600)
        self.x = self.start_x
        self.y = self.start_x
        self.size = 5
        self.canvas = canvas
        r = lambda: random.randint(0,255)
        self.color = '#%02X%02X%02X' % (r(),r(),r())
        self.circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=self.color)
        if(nn==None):
            self.nn = OrganismBrain()
        else:
            self.nn = nn
        self.dead = False
        self.food = Food(self.canvas,self.color)
        self.start = time.time()
        self.idx = idx
        self.ancestral = ancestral
        self.score = 0
        self.start_xf = self.food.start_x
        self.start_yf = self.food.start_y
    
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
        if(distance<=6.5):
            #collision
            self.feed()
    
    def move(self):
        self.input_information()
        direction = self.reaction()
        if(direction=="up"):
            self.y -= 10
        elif(direction=="down"):
            self.y += 10
        elif(direction=="right"):
            self.x -= 10
        elif(direction=="left"):
            self.x += 10
        else:
            print("no COMMAND")

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
        self.food = Food(self.canvas, self.color)
        old.eat()

    def die(self, time):
        self.nn.set_time_alive(time)
        self.dead = True
        self.remove()
    
    def isDead(self):
        return self.dead

    def reproduce(self, idx):
        brain = self.nn.copy_with_mutation()
        return Organism(self.canvas, idx,self.idx,nn=brain)
     
    def isSelected(self):
        if(not self.dead):
            self.nn.time_alive = 10
        if(self.nn.number_of_feeding>=1):
            initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            self.score = self.nn.time_alive + 10*self.nn.number_of_feeding + initial_distance//120
        else:
            initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            final_distance = self.get_distance([self.x,self.y],[self.start_xf,self.start_yf])
            self.score = self.nn.time_alive + 10*(initial_distance-final_distance)//initial_distance
        if((not self.dead) and self.nn.number_of_feeding>=1):
            #print(not self.dead, self.nn.number_of_feeding)
            return True 
        else: 
            return False
    
    def remove(self):
        if(not self.isDead()):
            self.canvas.delete(self.circle)
            self.food.eat()
    

class Food():

    def __init__(self, canvas,color):
        self.start_x = random.randint(0,600)
        self.start_y = random.randint(0,600)
        self.x = self.start_x
        self.y = self.start_y
        self.size = 7
        self.canvas = canvas
        self.square = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=color)
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
        for i in range(1,2001):
            self.orgs.append(Organism(self.canvas,i,-1))
        self.start_time = time.time()
        self.gen = 0
        self.moves = 0
        self.ret = self.canvas.create_rectangle(0, 0, 10, 600, fill='green')
    

    def move(self):
        for org in self.orgs:
            if(not org.isDead()):
                org.move()
        if(time.time()-self.start_time<=120):
            self.window.after(500, self.move)
        self.moves+=1
    
    def select(self):
        survivors = []
        #full = 0
        #success = 0
        ok = 0
        s = 0
        for o in self.orgs:
            if(o.isSelected()):
                print("SUCCED",o.score, o.nn.number_of_feeding, o.nn.time_alive,o.start_x,o.start_y,o.start_xf,o.start_yf)
                ok+=1
            #else:
                #if(o.score>0):
                    #print("FAILED",o.score,o.nn.number_of_feeding, o.nn.time_alive)
            #if(o.nn.time_alive==10):
                #s+=1
        print("survivors: {}, alives: {}".format(ok,s))
             #   survivors.append(o)
            #else: ##kill
             #   o.remove()
            #self.orgs = []
            #if(len(survivors)>0):
                #number_of_decendents = 2000//len(survivors)
                #for o in survivors:
                    #self.organisms.append(o)
                 #   for i in range(0,number_of_decendents):
                  #      new = o.reproduce(i)
                   #     self.orgs.append(new)
                #self.gen+=1
                #print("gen {}".format(self.gen))
                #self.start()
            #if(not o.isDead()):
             #   survivors+=1
            #if(o.nn.number_of_feeding>0):
                #full+=1
        #print(survivors, full)
        print(self.moves, time.time(), self.start_time, time.time()-self.start_time)

    def start(self):
        self.move()
        self.start_time = time.time()
        #self.window.update()
        while (time.time()-self.start_time<=120):
            self.window.update()
        self.select()

game_instance = environment()
environment.start(game_instance)