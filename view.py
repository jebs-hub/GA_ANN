#interface gráfica da evolução

from tkinter import *
import random
import time
from PIL import ImageTk,Image
from model import OrganismBrain
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

    def eat(self):
        self.canvas.delete(self.square)


class Poison():
    pass


class OrganismView(): 
                                                       
    def __init__(self,canvas):   #TODO refactor the constructor with the two functions
        
        self.size = organism_size
        self.canvas = canvas
        self.start = time.time()
        self.dead = False
        self.previous_move = None
        self.brownian = False
    

    def rise(self,gen,id,ancestral,brain=None):
        
        self.start_x = random.randint(20,size_of_board-20)
        self.start_y = random.randint(20,size_of_board-20)
        self.x = self.start_x
        self.y = self.start_y
        
        self.color = self.generate_color()
        self.circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=self.color)
        
        if(brain!=None):
            self.brain = brain
        else:
            self.brain = OrganismBrain()

        self.food = Food(self.canvas,self.color)
        self.start_xf = self.food.start_x
        self.start_yf = self.food.start_y

        self.id = id
        self.ancestral = ancestral
        self.score = 0
        self.gen = gen
        self.feeding = 0


    def rebuild(self,data,path):
        file = path+"/brains/"+data[0]
        self.id = int(data[0])
        self.score = float(data[1])
        self.gen = int(data[2])
        self.ancestral = int(data[3])
        self.time_alive = float(data[4])
        self.feeding = int(data[5])
        self.start_x = int(data[6])
        self.start_y = int(data[7])
        self.x = int(data[6])
        self.y = int(data[7])
        self.start_xf = int(data[8])
        self.start_yf = int(data[9])
        self.color = self.generate_color()
        self.circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=self.color)
        self.brain = OrganismBrain(path=file)
        self.food = Food(self.canvas,self.color,self.start_xf,self.start_yf)


    
    def generate_color(self):
        r = lambda: random.randint(0,255)
        return '#%02X%02X%02X' % (r(),r(),r())


    def input_information(self):

        d_food_up = self.y-self.food.get_y()
        d_food_right = self.food.get_x()-self.x

        self.brain.get_environment_info([d_food_up,d_food_right])
    

    def reaction(self):
        return self.brain.response()


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
    
    
    def get_distance(self,point1, point2):
        return math.sqrt(((point1[0]-point2[0])**2+(point1[1]-point2[1])**2))
    

    def get_linear_distance(self,point1,point2):
        return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])
    

    def isFoodReached(self):
        x_food = self.food.get_x()
        y_food = self.food.get_y()
        distance = self.get_distance([x_food,y_food],[self.x, self.y])
        if(distance<=collision_radius): #collision
            return True 
        return False


    def isOutOfBounds(self):
        if(self.y < 0 or self.y>size_of_board or self.x < 0 or self.x>size_of_board):
            return True 
        return False

    
    def move(self):
        self.input_information()
        direction = self.reaction()
        steps_x = 0
        steps_y = 0
        if(direction=="up"):
            self.y -= 10
            steps_y = -10
            if(self.food.get_y()<self.x):
                self.score+=1
            if(self.previous_move=="down"):
                self.brownian = True
                self.die()
        elif(direction=="down"):
            if(self.food.get_y()>self.x):
                self.score+=1
            self.y += 10
            steps_y = 10
            if(self.previous_move=="up"):
                self.brownian = True
                self.die()
        elif(direction=="right"):
            if(self.food.get_x()>self.x):
                self.score+=1
            self.x += 10
            steps_x = 10
            if(self.previous_move=="left"):
                self.brownian = True
                self.die()
        elif(direction=="left"):
            if(self.food.get_x()<self.x):
                self.score+=1
            if(self.previous_move=="right"):
                self.brownian = True
                self.die()
            self.x -= 10
            steps_x = -10
        else:
            print("no COMMAND")
        
        self.previous_move = direction

        # if outside screen, organism dies
        if(self.isOutOfBounds()):
            self.die()
        else:
            self.canvas.move(self.circle, steps_x, steps_y)
            if(self.isFoodReached()):
                self.feed()
                self.previous_move = None
        print(self.x,self.y,self.start_xf,self.start_yf)

    
    def feed(self):
        self.brain.increment_number_of_feeding()
        old = self.food 
        self.food = Food(self.canvas, self.color)
        old.eat()


    def die(self):
        time_alive = time.time() - self.start
        self.brain.set_time_alive(time_alive)
        self.dead = True
        self.remove()
    

    def isDead(self):
        return self.dead


    def reproduce(self, id):
        brain = self.brain.copy_with_mutation()
        next_gen = self.gen+1
        new = OrganismView(self.canvas)
        new.rise(next_gen,id,self.id,brain=brain)
        return new
    

    def define_score(self): #TODO review score
        #if(self.brain.get_number_of_feeding()>=1):
            #initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            #self.score = self.brain.time_alive + 10*self.brain.get_number_of_feeding() + initial_distance//120
        #else:
            #initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            #final_distance = self.get_distance([self.x,self.y],[self.start_xf,self.start_yf])
            #self.score = self.brain.time_alive + 10*(initial_distance-final_distance)//initial_distance
        pass

    def define_status(self):
        if(self.brain.get_number_of_feeding()>=1 and self.brain.get_time_alive()>=110):
            self.succed = True 
    

    def end(self):
        if(self.brain.get_number_of_feeding()==0 and not self.isDead()):
            self.die() 
        self.define_score()
        self.define_status()


    def survive(self):
        return self.succed


    def remove(self):
        self.canvas.delete(self.circle)
        self.food.eat()
    
    def data_for_report(self):
        return [self.id,self.score,self.gen,self.ancestral,self.brain.time_alive,self.brain.number_of_feeding,self.start_x,self.start_y,self.start_xf,self.start_yf]

    def brain_for_report(self,prefix):
        file = prefix+"/"+str(self.id)
        self.brain.scan(file)
        pass

    def print_orgs_report(self):
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.id,self.score,self.gen,self.ancestral,self.brain.time_alive,self.brain.number_of_feeding,self.start_x,self.start_y,self.start_xf,self.start_yf))


    def print_orgs_brain_report(self):
        self.brain.nn.print()

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
            new = OrganismView(self.canvas)
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
                    new = OrganismView(self.canvas)
                    new.rebuild(row,path_gen)
                    self.orgs.append(new)
                else:
                    first = False

    def end_simulation(self):
        for o in self.orgs:
            if(not o.isDead()):
                o.die()              
            o.define_score()
    
    def grow_pop(self):
        c = 1
        self.gen+=2
        count = len(self.orgs)
        desc = population//count 
        next = []
        for i in self.orgs:
            for j in range(desc):
                next.append(i.reproduce(c))
                c+=1
        self.orgs = next


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
#env.save_report(n=10)
env.rebuild_gen("gen3")
#env.grow_pop()
env.run_simulation()
#env.end_simulation()
#env.rank()
#env.save_report(n=10)
