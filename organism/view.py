import random
from organism.food import Food

class OrgsView(): 
                                                       
    def __init__(self,canvas,organism_size,x,y,xf,yf,color=None): 
        
        self.size = organism_size
        self.canvas = canvas
        if(color==None):
            self.color = self.generate_color()
        else:
            self.color = color
        self.circle = self.canvas.create_oval(x,y,x+self.size,y+self.size,fill=self.color)
        self.new_food(xf,yf)

    
    def generate_color(self):
        r = lambda: random.randint(0,255)
        return '#%02X%02X%02X' % (r(),r(),r())
    

    def move(self,steps_x,steps_y):
        self.canvas.move(self.circle, steps_x, steps_y)


    def remove(self):
        self.canvas.delete(self.circle)
    
    def remove_food(self):
        self.food.remove()
    

    def new_food(self,xf,yf):
        self.food = Food(self.canvas,self.color,xf,yf)