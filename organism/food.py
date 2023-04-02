class Food():

    def __init__(self,canvas,color,xi,yi):
        self.start_x = xi 
        self.start_y = yi
        self.x = self.start_x
        self.y = self.start_y
        self.size = 5                    #TODO deal with food size
        self.canvas = canvas
        self.square = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x+self.size, self.start_y+self.size, fill=color)

    def remove(self):
        self.canvas.delete(self.square)