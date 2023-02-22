from nn_library.nn import NeuralNetwork
import time
import random
import math

nn_eskeleton = [2,3,4] #default neural net for our model

class OrgsModel:
    

    def __init__(self,size_env,coll_radius):
        
        self.size_env = size_env
        self.start = time.time()
        self.dead = False
        self.coll_radius = coll_radius
        self.fed = False
        self.previous_move = None
        self.score_increment = 1

    
    def rise(self,gen,id,ancestral,neural_net=None):    
        #self.start_x = random.randint(20,self.size_env-20)
        #self.start_y = random.randint(20,self.size_env-20)
        self.start_x = random.randint(2,self.size_env/10-2)
        self.start_y = random.randint(2,self.size_env/10-2)
        self.start_x *= 10
        self.start_y *= 10
        self.x = self.start_x
        self.y = self.start_y
        self.start_xf, self.start_yf = self.generate_food_position()
        self.xf = self.start_xf
        self.yf = self.start_yf
        
        if(neural_net!=None):
            self.nn = neural_net
        else:
            self.nn = NeuralNetwork(number_of_neurons_per_layer=nn_eskeleton)

        self.id = id
        self.ancestral = ancestral
        self.score = 0
        self.gen = gen
        self.feeding = 0
        self.time_alive = 0
    

    def rebuild(self,data,path):
        file = path+"/brains/"+data[0]
        self.id = int(data[0])
        #self.score = float(data[1])
        self.score = 0
        self.gen = int(data[2])
        self.ancestral = int(data[3])
        self.time_alive = float(data[4])
        #self.feeding = int(data[5])
        self.feeding = 0
        self.start_x = int(data[6])
        self.start_y = int(data[7])
        self.x = int(data[6])
        self.y = int(data[7])
        self.start_xf = int(data[8])
        self.start_yf = int(data[9])
        self.xf = int(data[8])
        self.yf = int(data[9])
        self.nn = NeuralNetwork(file=file)
    

    def generate_food_position(self):
        lado = random.randint(1,4)
        x1 = self.x-10
        x2 = self.x+10
        y1 = self.y-10
        y2 = self.y+10
        
        sort = random.randint(1,2)
        if(sort == 1):
            if(x1>10):
                xf = x1 
            else: 
                xf = x2
        
        if(sort == 2):
            if(x2<690):
                xf = x2 
            else: 
                xf = x1
        
        sort = random.randint(1,2)
        if(sort == 1):
            if(y1>10):
                yf = y1 
            else: 
                yf = y2
        
        if(sort == 2):
            if(y2<690):
                yf = y2 
            else: 
                yf = y1
        #xf = random.randint(20,self.size_env-20)
        #yf = random.randint(20,self.size_env-20)
        xf = random.randint(2,self.size_env/10-2)
        yf = random.randint(2,self.size_env/10-2)
        xf*=10
        yf*=10
        return xf,yf


    def increment_number_of_feeding(self):
        self.number_of_feeding+=1
    

    def get_number_of_feeding(self):
        return self.number_of_feeding


    def reset_number_of_feeding(self):
        self.number_of_feeding = 0
    

    def set_time_alive(self, time): 
        self.time_alive = time
    

    def get_time_alive(self):
        return self.time_alive


    def copy_with_mutation(self):
        new_nn = self.nn.copy_with_mutation()
        return OrgsModel(neural_net=new_nn)

    
    def move(self):
        #test = 0.95
        vel = 10
        current_move = 'up'
        self.fed = False
        self.nn.input_data([self.xf-self.x,self.y-self.yf])
        self.nn.run_net()
        output = self.nn.get_output()
        #print(output)
        max = output[0]
        idx = 0
        stepsx = 0
        stepsy = 0
        for i in range(len(output)):
            if(output[i]>max):
                max = output[i]
                idx = i
        #if(max<test):
         #   idx=-1
          #  print("aqui",test,max)
        if(idx==0): #up
            if(self.yf<self.y):
                self.score+=self.score_increment
                self.score_increment+=1
            else:
                self.score_increment = 0
                #print("nota")
            self.y -= vel
            stepsy = -vel
            #print("up")
        elif(idx==1):
            if(self.yf>self.y):
                self.score+=self.score_increment
                self.score_increment+=1
            else:
                self.score_increment = 0
                #print("nota")
            self.y += vel
            stepsy = +vel
            current_move = 'down'
            #print("down")
        elif(idx==2):
            if(self.xf>self.x):
                self.score+=self.score_increment
                self.score_increment+=1
            else:
                self.score_increment = 0
                #print("nota")
            self.x += vel
            stepsx = vel
            current_move = 'right'
            #print("right")
        elif(idx==3):
            if(self.xf<self.x):
                self.score+=self.score_increment
                self.score_increment+=1
            else:
                self.score_increment = 0
                #print("nota")
            self.x -= vel
            stepsx = -vel
            current_move = 'left'
            #print("left")
        else:
            self.die()
            return 0,0
        if(self.isOutOfBounds()):
            self.die()
        else:
            if(self.isFoodReached()):
                self.feeding+=1
                self.fed = True
                self.new_food_coords()
            #elif(self.previous_move == 'down' and current_move == 'up'):
            #    self.die()
            #elif(self.previous_move == 'up' and current_move == 'down'):
            #    self.die()
            #elif(self.previous_move == 'right' and current_move == 'left'):
            #    self.die()
            #elif(self.previous_move == 'left' and current_move == 'right'):
            #    self.die()
        self.previous_move = current_move
        #print(self.score,self.xf,self.x)
        return stepsx,stepsy

    
    def isFoodReached(self):
        #distance = self.get_distance([self.xf,self.yf],[self.x, self.y])
        distance_x = abs(self.x-self.xf)
        distance_y = abs(self.y-self.yf)
        #print(distance_x,distance_y,self.x,self.y,self.xf,self.yf)
        if(distance_x<self.coll_radius and distance_y<self.coll_radius): #collision
            return True 
        return False


    def isOutOfBounds(self):
        if(self.y < 0 or self.y>self.size_env or self.x < 0 or self.x>self.size_env):
            return True 
        return False

    
    def scan(self,file):
        self.nn.write_nn(file)
    

    def die(self):
        self.time_alive = time.time() - self.start
        self.dead = True
    

    def isDead(self):
        return self.dead

    
    def reproduce(self,id):
        nn = self.nn.copy_with_mutation()
        next_gen = self.gen+1
        new = OrgsModel(self.size_env,self.coll_radius)
        new.rise(next_gen,id,self.id,neural_net=nn)
        return new
    

    def end(self):
        if(not self.dead):
            self.die() 
        self.define_score()
    

    def get_distance(self,point1, point2):
        return math.sqrt(((point1[0]-point2[0])**2+(point1[1]-point2[1])**2))
    

    def get_linear_distance(self,point1,point2):
        return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])


    def define_score(self): #TODO review score
        pass
        #if(self.feeding>=1):
            #initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            #self.score = self.time_alive + 10*self.feeding + initial_distance//120
        #else:
            #initial_distance = self.get_distance([self.start_x,self.start_y],[self.start_xf,self.start_yf])
            #final_distance = self.get_distance([self.x,self.y],[self.start_xf,self.start_yf])
            #self.score = self.time_alive + 10*(initial_distance-final_distance)//initial_distance
    

    def data_for_report(self):
        return [self.id,self.score,self.gen,self.ancestral,self.time_alive,self.feeding,self.start_x,self.start_y,self.start_xf,self.start_yf]
    

    def brain_for_report(self,prefix):
        file = prefix+"/"+str(self.id)
        self.scan(file)
        pass


    def print_orgs_report(self):
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.id,self.score,self.gen,self.ancestral,self.time_alive,self.feeding,self.start_x,self.start_y,self.start_xf,self.start_yf))


    def print_orgs_brain_report(self):
        self.nn.print()

    
    def get_food_coords(self):
        return [self.xf,self.yf]
    
    def new_food_coords(self):
        self.xf,self.yf = self.generate_food_position()