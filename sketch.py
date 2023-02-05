from tkinter import *
import random
import time
from PIL import ImageTk,Image
from nn_library.organism.model import OrganismBrain
import math
import csv
import os

#Parameters
size_of_board = 500
collision_radius = 15
organism_size = 7
food_size = 5
population = 2001
vel = 10
duration = 70

class Food():

    def __init__(self,canvas,color,xi=None,yi=None):
        if(xi!=None):
            self.start_x = xi 
            self.start_y = yi
        else:
            self.start_x = random.randint(0,size_of_board)
            self.start_y = random.randint(0,size_of_board)
        self.x = self.start_x
        self.y = self.start_y
        self.size = food_size
        self.canvas = canvas
        self.square = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=color)

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

    def remove(self):
        self.canvas.delete(self.square)


class Poison():
    pass


class OrgsmView(): 
                                                       
    def __init__(self,canvas,x,y,xf,yf,color=None):   #TODO refactor the constructor with the two functions
        
        self.size = organism_size
        self.canvas = canvas

        self.start_x = x
        self.start_y = y
        
        if(color==None):
            self.color = self.generate_color()
        else:
            self.color = color
        self.circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=self.color)

        self.food = Food(self.canvas,self.color,xf,yf)
        self.xf = xf
        self.yf = yf

    
    def generate_color(self):
        r = lambda: random.randint(0,255)
        return '#%02X%02X%02X' % (r(),r(),r())

    
    def move(self,step):
        self.canvas.move(self.circle, step[0], step[1])

    
    #def feed(self):
        #self.brain.increment_number_of_feeding()
        #old = self.food 
        #self.food = Food(self.canvas, self.color)
        #old.eat()

    def remove_food(self):
        self.food.remove()

    def remove(self):
        self.canvas.delete(self.circle)


class environment:
   
    def __init__(self):        #TODO modify constructor
        self.window = Tk()
        self.window.title("Environment")
        self.orgs = []
        self.start_time = time.time()
        self.gen = 0
        self.moves = 0
        self.avg = 0
        self.feeding = 0
    

    def move(self):
        for org in self.orgs:
            if(not org.isDead()):
                org.move()
        if(time.time()-self.start_time<=duration):
            self.window.after(500, self.move)
        self.moves+=1
    
    
    def rank(self):
        self.orgs.sort(key=lambda x: x.score, reverse=True)
        pass
    

    def print_gen_report(self): #TODO print report in the same format of save report
        print("gen\tboard size\tpop\tvel\tcoll radius\tmoves\tavg score\tfeeding")
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.gen,size_of_board,population,vel,collision_radius,self.moves,self.avg,self.feeding))


    def print_orgs_report(self,n=10):
        print("id\tscore\tgen\tancestral\ttime alive\tfeeding\txi\tyi\txfi\tyfi")
        for i in range(n):
            self.orgs[i].print_orgs_report()
    

    def print_orgs_brain_report(self,n=10):
        for i in range(n):
            print("ID: {}",self.orgs[i].id)
            self.orgs[i].print_orgs_brain_report()
        

    def save_report(self,dir="",n=50): 
        os.makedirs(dir+"gen"+str(self.gen)+"/brains",exist_ok=True)
        file_gen = dir+"gen"+str(self.gen)+"/resume"
        file_orgs = dir+"gen"+str(self.gen)+"/performances"
        file_brain = dir+"gen"+str(self.gen)+"/brains"
        with open(file_gen+".csv", 'w') as f:
            writer = csv.writer(f)
            header = ["gen","board size","pop","vel","coll radius","moves","avg score","feeding"]
            writer.writerow(header)
            data = [self.gen,size_of_board,population,vel,collision_radius,self.moves,self.avg,self.feeding]
            writer.writerow(data)
            f.close()
        with open(file_orgs+".csv", 'w') as f:
            writer = csv.writer(f)
            header = ["id","score","gen","ancestral","time alive","feeding","xi","yi","xfi","yfi"]
            writer.writerow(header)
            for i in range(n):
                data = self.orgs[i].data_for_report()
                writer.writerow(data)
                self.orgs[i].brain_for_report(file_brain)
            f.close()


    def start_gen(self): 
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)   
        self.canvas.pack()
        for i in range(1,population):
            new = OrgsmView(self.canvas)
            new.rise(0,i,-1,brain=None)
            self.orgs.append(new)


    def rebuild_gen(self,path_gen):
        global size_of_board, population, vel, collision_radius
        with open(path_gen+"/resume.csv","r") as file:
            csvreader = csv.reader(file)
            data = []
            for row in csvreader:
                data = row 
            self.gen = int(data[0])        
            size_of_board = int(data[1])
            population = int(data[2])
            vel = int(data[3])
            collision_radius = float(data[4])
            self.moves = int(data[5])
            self.avg = float(data[6])
            self.feeding = int(data[7])
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)  
        self.canvas.pack()
        with open(path_gen+"/performances.csv", 'r') as file:
            csvreader = csv.reader(file)
            first = True
            for row in csvreader:
                if(not first):
                    new = OrgsmView(self.canvas)
                    new.rebuild(row,path_gen)
                    self.orgs.append(new)
                else:
                    first = False

        

    def end_simulation(self):
        for o in self.orgs:
            if(not o.isDead()):
                o.die()              
            o.define_score()
                    

    def run_simulation(self):   ##run evolution
        
        self.window.after(500, self.move)
        self.start_time = time.time()
        while (time.time()-self.start_time<=duration):
            self.window.update()


env = environment()
#env.start_gen()
#env.run_simulation()
#env.end_simulation()
#env.rank()
#env.save_report()
env.rebuild_gen("gen0")
env.run_simulation()
env.print_gen_report()