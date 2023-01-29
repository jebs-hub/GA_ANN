from nn import NeuralNetwork
import random

class OrganismBrain:
    
    def __init__(self, idx, neural_net=None):
        self.number_of_feeding = 0
        self.idx = idx
        self.time_alive = 0
        if(neural_net == None):
            self.nn = NeuralNetwork(number_of_neurons_per_layer=[3,4,5,4])
        else: 
            self.nn = neural_net

    def increment_number_of_feeding(self):
        self.number_of_feeding+=1
    

    def reset_number_of_feeding(self):
        self.number_of_feeding = 0
    

    def set_time_alive(self, time): 
        self.time_alive = time

    def copy_with_mutation(self):
        new_nn = self.nn.copy_with_mutation()
        return Organisms(new_nn)
    
    def isSelected(self):
        if(self.time_alive>=5 and self.number_of_feeding>=2):
            return True
        else:
            return False
    
    def get_command(self):
        output = self.nn.get_output()
        if(output[0]==1):
            return "up"
        if(output[1]==1):
            return "down"
        if(output[2]==1):
            return "right"
        if(output[3]==1):
            return "left"



class Ecosystem:
    def __init__(self, number_of_organisms):
        self.number_of_organisms = number_of_organisms
        self.organisms = []
        for i in range(number_of_organisms):
            self.organisms.append(Organisms(i))
        self.abs_vel = 2
    
    def select(self):
        new_organisms = []
        number_of_organisms = 0
        for i in range(self.number_of_organisms):
            if(self.organisms[i].isSelected()):
                new_organism = self.organisms[i].copy_with_mutation()
                new_organisms.append(new_organism)
                new_organisms.append(self.organisms[i])
                number_of_organisms+=2
        self.number_of_organisms = number_of_organisms
        self.organisms = new_organisms
    
    def feed(self,idx):
        self.organisms[idx].increment_feeding()

    def set_time_alive(self,idx, time):
        self.organisms[idx].set_time_alive(time)
    
    def get_command(self, idx):
        return self.organisms[idx].get_command()