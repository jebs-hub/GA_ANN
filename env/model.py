import time
import csv
import os 

from organism.organism import Organism

class EnvModel:
   
    def __init__(self,size_env,size_pop,vel,coll_radius,duration):   
        self.orgs = []
        self.start_time = time.time()
        self.gen = 0
        self.moves = 0
        self.avg = 0
        self.feeding = 0
        self.size_env = size_env
        self.size_pop = size_pop
        self.vel = vel 
        self.coll_radius = coll_radius
        self.duration = duration
        self.all_dead = False

    
    # --------------------------------------- Create Gen ----------------------------------------- #

    def start_gen(self): 
        for i in range(1,self.size_pop+1):
            new = Organism(self.size_env,self.coll_radius,self.vel)
            new.rise(0,i,-1)
            self.orgs.append(new)
    

    def rebuild_gen(self,path_gen,n=None):
        with open(path_gen+"/resume.csv","r") as file:
            csvreader = csv.reader(file)
            data = []
            for row in csvreader:
                data = row 
            self.gen = int(data[0])        
            self.size_env = int(data[1])
            self.size_pop = int(data[2])
            self.vel = int(data[3])
            self.coll_radius = float(data[4])
            self.moves = int(data[5])
            self.avg = float(data[6])
            self.feeding = int(data[7])
        i = 0
        with open(path_gen+"/performances.csv", 'r') as file:
            csvreader = csv.reader(file)
            first = True
            for row in csvreader:
                i+=1
                if(n==None):
                    if(not first):
                        new = Organism(self.size_env,self.coll_radius,self.vel)
                        new.rebuild(row,path_gen)
                        self.orgs.append(new)
                    else:
                        first = False
                elif(i<=n+1):
                    if(not first):
                        new = Organism(self.size_env,self.coll_radius,self.vel)
                        new.rebuild(row,path_gen)
                        self.orgs.append(new)
                    else:
                        first = False
    
    def grow(self,n=10):
        next_gen = []
        des = self.size_pop//n
        id = 1
        for i in range(n):
            #new = self.orgs[i].copy(id)
            #self.orgs[i].model.nn.print()
            #new.model.nn.print()
            self.orgs[i].model.isCopy = True
            self.orgs[i].model.score = 0
            self.orgs[i].model.dead = False
            next_gen.append(self.orgs[i])
            copy_id = id
            id+=1
            for j in range(des-1):
                new = self.orgs[i].reproduce(id)
                next_gen.append(new)
                id+=1
            self.orgs[i].reset(copy_id)
            self.orgs[i].model.gen+=1
            self.orgs[i].model.ancestral = self.orgs[i].model.id
            self.orgs[i].model.id = copy_id
        self.orgs = next_gen


    
    # -------------------------------------- Output info ----------------------------------------#
    

    def print_gen_report(self): #TODO print report in the same format of save report
        print("gen\tboard size\tpop\tvel\tcoll radius\tmoves\tavg score\tfeeding")
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.gen,self.size_env,self.size_pop,self.vel,self.coll_radius,self.moves,self.avg,self.feeding))


    def print_orgs_report(self,n=10):
        print("id\tscore\tgen\tancestral\ttime alive\tfeeding\txi\tyi\txfi\tyfi\tbirth gen")
        for i in range(n):
            self.orgs[i].model.print_orgs_report()
    

    def print_orgs_brain_report(self,n=10):
        for i in range(n):
            print("ID: {}",self.orgs[i].id)
            self.orgs[i].model.print_orgs_brain_report()
        

    def save_report(self,dir="",n=50): 
        os.makedirs(dir+"gen"+str(self.gen)+"/brains",exist_ok=True)
        file_gen = dir+"gen"+str(self.gen)+"/resume"
        file_orgs = dir+"gen"+str(self.gen)+"/performances"
        file_brain = dir+"gen"+str(self.gen)+"/brains"
        with open(file_gen+".csv", 'w') as f:
            writer = csv.writer(f)
            header = ["gen","board size","pop","vel","coll radius","moves","avg score","feeding"]
            writer.writerow(header)
            data = [self.gen,self.size_env,self.size_pop,self.vel,self.coll_radius,self.moves,self.avg,self.feeding]
            writer.writerow(data)
            f.close()
        with open(file_orgs+".csv", 'w') as f:
            writer = csv.writer(f)
            header = ["id","score","gen","ancestral","copy","time alive","feeding","xi","yi","xfi","yfi","birth gen"]
            writer.writerow(header)
            for i in range(n):
                data = self.orgs[i].model.data_for_report()
                writer.writerow(data)
                self.orgs[i].model.brain_for_report(file_brain)
            f.close()

    # --------------------------------------- Simulation ----------------------------------------- #

    def stop(self):
        return time.time()-self.start_time>self.duration or self.all_dead
    
    
    def move(self):
        all_dead = True
        for org in self.orgs:
            if(not org.model.isDead()):
                org.move()
                all_dead = False
        self.moves+=1
        self.all_dead = all_dead
    
    
    def rank(self):
        self.orgs.sort(key=lambda x: x.model.score, reverse=True)


    def end_simulation(self):
        for o in self.orgs:
            if(not o.model.isDead()):
                o.model.die()
            if(o.model.feeding>=1):
                self.feeding+=1           
            o.model.define_score()


    def update_gen(self):
        self.feeding = 0
        self.moves = 0
        self.gen+=1
        self.all_dead = False
                    

    def run_simulation(self):   ##run evolution
        self.start_time = time.time()
        print(self.gen)
        while (not self.stop()):
            self.move()
    
    # --------------------------------------- View -------------------------------------- #

    def create_view(self,canvas,color,size):
        for o in self.orgs:
            o.create_view(canvas,color,size)