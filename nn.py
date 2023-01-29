# Creation of neural network

import random

class Neuron():

    def __init__(self, bias:float=None, weights:list[float]=[]): 
        self.output = None
        self.bias = bias
        self.weights = weights
        self.sum = 0
        self.weights_times_output = []
    
    def set_output(self, output: float):
        self.output = output
    
    def set_bias(self, bias: float):
        self.bias = bias
    
    def set_weights(self, weights: list[float]): #none a concern of neuron itself
        self.weights = weights                   #if length of weights changes
    
    def set_weigth(self, i: int, new: float):
        self.weights[i] = new
    
    def increment_sum(self, sum: float):
        self.sum += sum

    def set_sum(self, sum:float):
        self.sum = sum
    
    def calculate_output(self): #get sum, use bias and function
        if(self.bias!=None):
            self.output = self.bias + self.sum
        else:
            self.output = self.sum
        if(self.output < 0):
            self.output = 0
        return self.output
    
    def calculate_weights_times_output(self):
        self.weights_times_output = []
        for w in self.weights:
            product = self.output*w
            self.weights_times_output.append(product)
        return self.weights_times_output
    
    def copy(self):
        copy = Neuron(self.bias, self.weights)
        return copy


class NeuralNetwork():


    def __init__(self, number_of_neurons_per_layer:list[int]=None,neural_net:list[list[Neuron]]=[], file=None):
        
        if(file!=None):
            self.neural_net = self.read_nn(file)
            self.number_of_layers = len(self.neural_net)
            self.number_of_neurons_per_layer = self.count_neurons_per_layer()
        elif(number_of_neurons_per_layer==None and neural_net==[]): 
            raise Exception("It is not possible create a empty Neural Network. Input a model or number of neurons per layer")
        elif(number_of_neurons_per_layer!=None and neural_net!=[]):
            raise Exception("You cannot set two parameters at same time. Choose between number_of_neurons_per_layer/neural_net")
        elif neural_net == [] and self.isValid():
            self.number_of_layers = len(number_of_neurons_per_layer)
            self.number_of_neurons_per_layer = number_of_neurons_per_layer
            self.neural_net = []
            self.create_random_neural_net()
        elif neural_net != [] and self.isValid():
            self.neural_net = neural_net
            self.number_of_layers = len(neural_net)
            self.number_of_neurons_per_layer = self.count_neurons_per_layer()
        else:
            raise Exception("Check your arguments, they are not valid")
    
    def isValid(self): #TODO isValid function and test constructor
        return True

    def count_neurons_per_layer(self):
        number_of_neurons_per_layer = []
        for i in range(self.number_of_layers):
            number_of_neurons = len(self.neural_net[i])
            number_of_neurons_per_layer.append(number_of_neurons)
        return number_of_neurons_per_layer
    
    def create_random_neural_net(self):
        
        layer = []
        for i in range(self.number_of_neurons_per_layer[0]): #set first layer = input layer, no bias
            weights = []
            for k in range(self.number_of_neurons_per_layer[1]): 
                weight = random.uniform(-5,5)
                weights.append(weight)
            neuron = Neuron(None, weights)
            layer.append(neuron) 
        self.neural_net.append(layer)

        for i in range(1, self.number_of_layers-1): #hidden layers, with bias and weghts 
            layer = []
            for j in range(self.number_of_neurons_per_layer[i]):
                weights = []
                bias = random.uniform(-5,5)
                for k in range(self.number_of_neurons_per_layer[i+1]): 
                    weight = random.uniform(-5,5)
                    weights.append(weight)
                neuron = Neuron(bias, weights)
                layer.append(neuron) 
            self.neural_net.append(layer)
        
        layer = []
        for i in range(self.number_of_neurons_per_layer[-1]): #set last layer = output layer, no weghts
            bias = random.uniform(-5,5)
            neuron = Neuron(bias=bias)
            layer.append(neuron)
        self.neural_net.append(layer)


    def print(self):
        for i, layer in enumerate(self.neural_net):
            print("Layer {}".format(i))
            for j, neuron in enumerate(layer):
                print("\tNeuron {}, bias: {}".format(j, neuron.bias))
                if(neuron.output != None):
                    print("\t\toutput: {}".format(neuron.output))
                for k, weight in enumerate(neuron.weights):
                    print("\t\t\tweigth: {}".format(weight))
    

    def input_data(self, datas):
        for i, neuron in enumerate(self.neural_net[0]):
            neuron.set_output(datas[i])
    

    def sum_vectors(self,vector1, vector2):
        vector3 = []
        for i in range(len(vector1)):
            vector3.append(vector1[i]+vector2[i])
        return vector3
    

    def run_net(self):
        for i in range(self.number_of_layers-1): 
            sum_results = [0]*self.number_of_neurons_per_layer[i+1]
            for n in self.neural_net[i]: #para cada neuronio n da layer i atual
                n.calculate_weights_times_output()
                result = n.weights_times_output
                sum_results = self.sum_vectors(sum_results, result)
            if(i < self.number_of_layers-1):
                for idx, n in enumerate(self.neural_net[i+1]):
                    n.set_sum(sum_results[idx])
                    n.calculate_output()
    

    def get_output(self):
        output = []
        for n in self.neural_net[self.number_of_layers-1]:
            output.append(n.output)
        return output
    
    def read_nn(self, file):
        #one with number of neurons
        #next n lines, one for one neuron. The first number are bias
        f = open(file, "r")
        first_line = True
        count_neurons = 0
        number_of_neurons = 0
        layer = []
        neural_net = []
        for line in f:
            line = line[:-1]
            if(first_line):
                first_line = False
                number_of_neurons = int(line.split(" ")[0])
                layer = []
            elif(count_neurons < number_of_neurons):
                count_neurons+=1
                values = line.split(" ")
                if(values[0].isnumeric()):
                    bias = int(values[0])
                else:
                    bias = None
                weights = values[1:]
                weights = [int(w) for w in weights]
                neuron = Neuron(bias, weights)
                layer.append(neuron)
            elif(count_neurons == number_of_neurons):
                neural_net.append(layer)
                layer = []
                count_neurons = 0
                number_of_neurons = int(line.split(" ")[0])
            else:
                pass
        neural_net.append(layer)
        return neural_net




    #TODO the next methods should be in organism class 

    def increment_number_of_feeding(self):
        self.number_of_feeding+=1
    

    def reset_number_of_feeding(self):
        self.number_of_feeding = 0
    

    def set_time_aliving(self, time): 
        self.time_alive = time
    

    def copy(self):
        new_neural_net = []
        for layer in self.neural_net:
            new_layer = []
            for neuron in layer:
                new_neuron = neuron.copy()
                new_layer.append(new_neuron)
            new_neural_net.append(new_layer)
        return NeuralNetwork(self.number_of_layers, self.number_of_neurons_per_layer,new_neural_net)


    def copy_with_mutation(self): #where to mutation things, maybe limit the number of mutation?
        new_neural_net = []        #TODO mutation should be within organism class
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

#n = NeuralNetwork(file="my_net.txt")
#n.print()
#n.input_data([1,1])
#n.run_net()
#print(n.get_output())