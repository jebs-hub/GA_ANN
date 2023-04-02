from tkinter import *
import time
from PIL import ImageTk,Image

class EnvView:
   
    def __init__(self,duration,size_of_board):        #TODO modify constructor
        self.window = Tk()
        self.window.title("Environment")
        self.size_of_board = size_of_board
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)   
        self.canvas.pack()
        self.duration = duration
    

    def run_simulation(self):   ##run evolution
        self.window.after(500, self.move)
        self.start_time = time.time()
        while (time.time()-self.start_time<=self.duration):
            self.window.update()