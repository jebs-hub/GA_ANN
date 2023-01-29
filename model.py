from nn import NeuralNetwork
import random

class Organisms:
    
    def __init__(self):
        self.number_of_feeding = 0
        self.time_aliving = 0
        self.nn = NeuralNetwork(number_of_neurons_per_layer=[3,4,5,4])

    def increment_number_of_feeding(self):
        self.number_of_feeding+=1
    

    def reset_number_of_feeding(self):
        self.number_of_feeding = 0
    

    def set_time_aliving(self, time): 
        self.time_alive = time
    

    #def copy(self):
    #    new_neural_net = []
    #    for layer in self.neural_net:
    #        new_layer = []
    #        for neuron in layer:
    #            new_neuron = neuron.copy()
    #            new_layer.append(new_neuron)
    #        new_neural_net.append(new_layer)
    #    return NeuralNetwork(self.number_of_layers, self.number_of_neurons_per_layer,new_neural_net)


    def copy_with_mutation(self):
        new_neural_net = []        
        for layer in self.neural_net[:-1]:  
            new_layer = []
            for neuron in layer:
                sort = random.randint(0,2) #zero or 1
                if(sort == 0):
                    new_neuron = neuron.copy() #don't mutate
                else:
                    new_neuron = neuron.copy_with_mutation()
                new_layer.append(new_neuron)
            new_neural_net.append(new_layer)
            new_layer = []
            for neuron in self.neural_net[-1]:
                sort = random.randint(0,2) #zero or 1
                if(sort == 0):
                    new_neuron = neuron.copy() #don't mutate
                else:
                    new_neuron = neuron.copy()
                    new_neuron.set_bias(random.uniform(-5,5))
                new_layer.append(new_neuron)
                new_neural_net.append(new_layer)

        return NeuralNetwork(self.number_of_layers, self.number_of_neurons_per_layer,new_neural_net)

class Ecosystem:
    pass

