from organism.model import OrgsModel

class Organism():
    
    def __init__(self,size_env,coll_radius,vel,view=False,canvas=None):
        
        self.view = view
        self.size_env = size_env 
        self.coll_radius = coll_radius
        self.view = view 
        self.canvas = canvas
        self.vel = vel
        self.model = OrgsModel(self.size_env,self.coll_radius)
    

    def rise(self,gen,id,ancestral,neural_net=None):
        self.model.rise(gen,id,ancestral,neural_net)
    

    def rebuild(self,data,path):
        self.model.rebuild(data,path)
    

    def move(self):
        self.model.move()