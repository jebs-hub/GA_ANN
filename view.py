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
size_of_board = 600
collision_radius = 6.5
organism_size = 7
food_size = 5
population = 2001
vel = 10
duration = 2

class Food():

    def __init__(self,canvas,color):
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
                                                       
    def __init__(self,canvas,id,ancestral,gen,brain=None):
        
        #canvas set up

        self.start_x = random.randint(20,size_of_board-20)
        self.start_y = random.randint(20,size_of_board-20)
        self.x = self.start_x
        self.y = self.start_y
        self.size = organism_size
        self.canvas = canvas
        self.color = self.generate_color()
        self.circle = self.canvas.create_oval(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=self.color)
        
        if(brain==None):
            self.brain = OrganismBrain()
        else:
            self.brain = brain

        self.food = Food(self.canvas,self.color)
        self.start_xf = self.food.start_x
        self.start_yf = self.food.start_y
        
        #set up important information

        self.dead = False
        self.start = time.time()
        self.id = id
        self.ancestral = ancestral
        self.score = 0
        self.gen = gen
        self.succed = False
        self.all_distance = 0

    
    def generate_color(self):
        r = lambda: random.randint(0,255)
        return '#%02X%02X%02X' % (r(),r(),r())


    def input_information(self):

        d_wall_up = self.y
        d_wall_down = size_of_board-self.y
        d_wall_right = size_of_board-self.x
        d_wall_left = self.x

        d_food_up = self.y-self.food.get_y()
        d_food_right = self.food.get_x()-self.x

        self.brain.get_environment_info([d_wall_up,d_wall_down,d_wall_right,d_wall_left,d_food_up,-d_food_up,d_food_right,-d_food_right])
    

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
        elif(direction=="down"):
            self.y += 10
            steps_y = 10
        elif(direction=="right"):
            self.x += 10
            steps_x = 10
        elif(direction=="left"):
            self.x -= 10
            steps_x = -10
        else:
            print("no COMMAND")

        # if outside screen, organism dies
        if(self.isOutOfBounds()):
            self.die()
        else:
            self.canvas.move(self.circle, steps_x, steps_y)
            if(self.isFoodReached()):
                self.feed()

    
    def feed(self):
        self.brain.increment_number_of_feeding()
        old = self.food 
        self.food = Food(self.canvas, self.color)
        old.eat()


    def die(self):
        self.all_distance = self.get_linear_distance([self.start_x, self.start_y],[self.x, self.y])
        time_alive = time.time() - self.start
        self.brain.set_time_alive(time_alive)
        self.dead = True
        self.remove()
    

    def isDead(self):
        return self.dead


    def reproduce(self, id):
        brain = self.brain.copy_with_mutation()
        next_gen = self.gen+1
        return OrganismView(self.canvas,id,self.id,next_gen,nn=brain)
    

    def define_score(self): #TODO review score
        if(self.brain.get_number_of_feeding()>=1):
            initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            self.score = self.brain.time_alive + 10*self.brain.get_number_of_feeding() + initial_distance//120
        else:
            initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            final_distance = self.get_distance([self.x,self.y],[self.start_xf,self.start_yf])
            self.score = self.brain.time_alive + 10*(initial_distance-final_distance)//initial_distance


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
        file = prefix+"_brain_scan_id"+str(self.id)
        self.brain.scan(file)
        pass

    def print_orgs_report(self):
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.id,self.score,self.gen,self.ancestral,self.brain.time_alive,self.brain.number_of_feeding,self.start_x,self.start_y,self.start_xf,self.start_yf))


    def print_orgs_brain_report(self):
        self.brain.nn.print()

class environment:
   
    def __init__(self):                          #TODO modify constructor
        self.window = Tk()
        self.window.title("Environment")
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)    #TODO check atributes
        self.canvas.pack()
        self.should_stop = False
        self.orgs = []
        for i in range(1,population):
            self.orgs.append(OrganismView(self.canvas,i,-1,0,brain=None))
        self.start_time = time.time()
        self.gen = 0
        self.moves = 0
        self.avg = 0
        self.feeding = 0
        #self.ret = self.canvas.create_rectangle(0, 0, 10, size_of_board, fill='green')
    

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
        

    def save_report(self,dir="./",n=50): 
        os.mkdir(dir+"gen"+str(self.gen))
        file_gen = dir+"gen"+str(self.gen)+"/gen"+str(self.gen)
        file_orgs = file_gen+"_performance_orgs"
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
                self.orgs[i].brain_for_report(file_gen)
            f.close()
        pass 


    def start_gen(self): ##TODO build gen from zero
        pass    


    def rebuild_gen(self): ##TODO reconstruct gen from files or specific orgs
        pass    
    

    def end_simulation(self):
        for o in self.orgs:
            if(not o.isDead()):
                o.die()              
            o.define_score()
    
    #TODO function to print the csv of previous generations
                    

    def run_simulation(self):   ##run evolution
        self.window.after(500, self.move)
        self.start_time = time.time()
        while (time.time()-self.start_time<=duration):
            self.window.update()


env = environment()
env.start_gen()
env.run_simulation()
env.end_simulation()
env.rank()
env.save_report()