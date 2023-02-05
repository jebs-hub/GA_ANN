from env.model import EnvModel
from env.view import EnvView

class Environment():

    def __init__(self,size_env,size_pop,vel,coll_radius,duration):

        self.model = EnvModel(size_env,size_pop,vel,coll_radius,duration)
        self.view = None
    
    def create_view(self,color=None,size=5):
        self.view = EnvView(self.model.duration,self.model.size_env)
        self.model.create_view(self.view.canvas,color,size) #creating orgs view
    
    def move(self):
        self.model.move()
        if(not self.model.stop()):
            self.view.window.after(500, self.move)


    def run_simulation(self):
        if(self.view==None):
            self.model.start_simulation()
        else:
            self.view.window.after(500, self.move)
            while (not self.model.stop()):
                self.view.window.update()

