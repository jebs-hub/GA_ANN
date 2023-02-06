from organism.model import OrgsModel
from organism.view import OrgsView

class Organism():
    
    def __init__(self,size_env,coll_radius,vel,model=None):
    
        self.size_env = size_env 
        self.coll_radius = coll_radius
        self.vel = vel
        if(model!=None):
            self.model=model
        else:
            self.model = OrgsModel(self.size_env,self.coll_radius)
        self.view = None
        self.created = False
    
    def create_view(self,canvas,color=None,size=5):
        if(self.created):
            self.view = OrgsView(canvas,size,self.model.x,self.model.y,self.model.xf,self.model.yf,color)
        else:
            raise Exception("First, rise or rebuild a model")

    def rise(self,gen,id,ancestral,neural_net=None):
        self.model.rise(gen,id,ancestral,neural_net)
        self.created = True
    

    def rebuild(self,data,path):
        self.model.rebuild(data,path)
        self.created = True
    

    def move(self):
        stepsx, stepsy = self.model.move()
        if(self.view!=None):
            self.view.move(stepsx,stepsy)
            pass
            if(self.model.dead):
                self.view.remove()
                self.view.remove_food()
            elif(self.model.fed):
                self.view.remove_food()
                self.view.new_food(self.model.xf,self.model.yf)
    
    def reproduce(self,id):
        new_model = self.model.reproduce(id)
        new = Organism(self.size_env,self.coll_radius,self.vel,model=new_model)
        new.created = True
        return new