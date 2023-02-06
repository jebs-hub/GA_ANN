from env.env import Environment

class Train():

    #num_gens,start,origin_dir,dest_dir,score_method,pop,size,size,size,duration,vel,radius

    def train_from_previous(self,num_gens,train_dir,last_gen):
        #get infos with the last gen (score_method,sizes,pop,etc)
        pass

    def new_training(self,num_gens,dest_dir,score_method,pop_size,board_size,org_size,food_size,duration,vel,coll_radius,n_firsts):
        self.num_gens = num_gens
        self.dest_dir = dest_dir
        self.score_method = score_method   #TODO all variables must be used through classes
        self.pop_size = pop_size
        self.board_size = board_size
        self.org_size = org_size
        self.food_size = food_size
        self.duration = duration
        self.vel = vel
        self.coll_radius = coll_radius
        self.n_firsts = n_firsts
        self.env = Environment(board_size,pop_size,vel,coll_radius,duration)
        self.env.model.start_gen()
    

    def simulate(self,logs,reports):
        #self.env.create_view()
        self.env.run_simulation()
        self.env.model.end_simulation()
        self.env.model.rank()
        if(logs):
            self.env.model.print_orgs_report(n=self.n_firsts)
            self.env.model.print_gen_report()
        if(reports):
            self.env.model.save_report(dir=self.dest_dir,n=self.n_firsts) #TODO function must receive a path


    def train(self,logs=False,reports=False):
        count = 0
        while(count<self.num_gens):
            self.simulate(logs,reports)
            self.env.model.update_gen()
            self.env.model.grow(n=self.n_firsts)
            count+=1
    

    #def view_gen(self):
        #if(self.env!=None):
            #self.env.create_view()
            #self.simulate(False,False)
    
    def view_gen(self,dir):
        rebuilt = Environment(self.board_size,self.pop_size,self.vel,self.coll_radius,self.duration)
        rebuilt.model.rebuild_gen(dir)
        rebuilt.create_view()
        rebuilt.run_simulation()
        rebuilt.model.print_gen_report()
        rebuilt.model.print_orgs_report(n=13)

    
    def view_org(self,id): 
        pass 


train = Train()
train.new_training(20,"train3/",1,2000,500,5,5,120,10,10,100)
#train.train(reports=True)
train.view_gen("prod")