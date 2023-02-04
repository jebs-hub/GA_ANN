# Creation of neural network

import random
import math

class Neuron():

    def __init__(self, bias:float=None, weights:list[float]=[], activate_function="reLU"):
        self.output = None
        self.bias = bias
        self.weights = weights
        self.sum = 0
        self.weights_times_output = []
        self.activate_function = activate_function
    
    def set_output(self, output: float):
        self.output = output
    
    def get_outpu(self):
        return self.output
    
    def set_bias(self, bias: float):
        self.bias = bias
    
    def get_bias(self):
        return self.bias
    
    def set_weights(self, weights: list[float]): #none a concern of neuron itself
        self.weights = weights                   #if length of weights changes
    
    def set_weight(self, i: int, new: float):
        self.weights[i] = new
    
    def get_weights(self):
        return self.weights
    
    def get_weight(self, i):
        return self.weights[i]
    
    def increment_sum(self, sum: float):
        self.sum += sum

    def set_sum(self, sum:float):
        self.sum = sum
    
    def get_sum(self):
        return self.sum
    
    def calculate_output(self): #get sum, use bias and function
        if(self.bias!=None):
            self.output = self.bias + self.sum
        else:
            self.output = self.sum
        self.calc_activate_function()
        return self.output
    
    def calculate_weights_times_output(self): #It's a list of the inputs that will be used in the some 
        self.weights_times_output = []        #of neuron of next layer
        for w in self.weights:
            product = self.output*w
            self.weights_times_output.append(product)
        return self.weights_times_output
    
    def copy(self):
        copy = Neuron(self.bias, self.weights, self.activate_function)
        return copy
    
    def set_activate_function(self, function):
        self.activate_function = function
    
    def activate_function(self):
        return self.activate_function
    
    def calc_activate_function(self):
        if(self.activate_function=="reLU"):
            if(self.output < 0):
                self.output = 0
            elif(self.output>170):
                self.output = 236
        else:
            self.output = 1/(1 + math.exp(-self.output))
        return self.output


class NeuralNetwork():


    def __init__(self, number_of_neurons_per_layer:list[int]=None,neural_net:list[list[Neuron]]=None, file=None):
        
        ##We suppose the file or the given neural net are valid
        #We aren't validating entry

        #Once the network is set, It can't be changed

        choosen = self.select_arguments(number_of_neurons_per_layer, neural_net, file) 
                                                                                
        if choosen==1 :    
            self.neural_net = self.read_nn(file)
            self.number_of_layers = len(self.neural_net)
            self.number_of_neurons_per_layer = self.count_neurons_per_layer()
        elif choosen==2 :
            self.number_of_layers = len(number_of_neurons_per_layer)
            self.number_of_neurons_per_layer = number_of_neurons_per_layer
            self.neural_net = []
            self.create_random_neural_net()
        elif choosen==3 :
            self.neural_net = neural_net
            self.number_of_layers = len(neural_net)
            self.number_of_neurons_per_layer = self.count_neurons_per_layer()


    # ----------------------------------------- Constructor auxiliary functions -------------------------------------------- #
    
    def select_arguments(self,number_of_neurons_per_layer, neural_net,file):
        not_none = 0
        choosen = 0
        if(file!=None):
            choosen = 1
            not_none+=1
        if(number_of_neurons_per_layer!=None):
            choosen = 2
            not_none+=1
        if(neural_net!=None):
            choosen = 3
            not_none+=1
        if(not_none!=1):
            self.Error("You must choose only one way to create the neural net: from a file, randonly or a given neural neral")
        else:
            return choosen
    

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
                weight = self.get_random_value()
                weights.append(weight)
            neuron = Neuron(None, weights)
            layer.append(neuron) 
        self.neural_net.append(layer)

        for i in range(1, self.number_of_layers-1): #hidden layers, with bias and weghts 
            layer = []
            for j in range(self.number_of_neurons_per_layer[i]):
                weights = []
                bias = self.get_random_value()
                for k in range(self.number_of_neurons_per_layer[i+1]): 
                    weight = self.get_random_value()
                    weights.append(weight)
                neuron = Neuron(bias, weights)
                layer.append(neuron) 
            self.neural_net.append(layer)
        
        layer = []
        for i in range(self.number_of_neurons_per_layer[-1]): #set last layer = output layer, no weghts
            bias = self.get_random_value()
            neuron = Neuron(bias=bias, activate_function="sigmoid")
            layer.append(neuron)
        self.neural_net.append(layer)


    #TODO see if is pssible to write a compact and descompact function to be used by write and read

    def  isfloat(self,value):
        try:
            float(value)
        except:
            return False 
        return True
    
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
                if(self.isfloat(values[0])):
                    bias = float(values[0])
                else:
                    bias = None
                weights = values[1:]
                weights = [float(w) for w in weights]
                if(weights==[]):   
                    neuron = Neuron(bias, weights, "sigmoid")
                else:
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
        f.close()
        return neural_net

    
    # --------------------------------------- Functions for general proposes ------------------------------------------ # 
    

    def write_nn(self,file):
        compact_nn = []
        for i in range(self.number_of_layers):
            layer = self.neural_net[i]
            len_layer = self.number_of_neurons_per_layer[i]
            compact_nn.append(str(len_layer))
            for neuron in layer:
                infos = str(neuron.get_bias())
                if(i<self.number_of_layers-1):
                    infos+=" "
                    infos+=" ".join(map(str, neuron.get_weights()))
                compact_nn.append(infos)
        with open(file, 'w') as f:
            f.write("\n".join(compact_nn))


    def Error(self, message):
        raise Exception(message)
    

    def get_random_value(self):
        return random.uniform(-1,1)


    def print(self):
        for i, layer in enumerate(self.neural_net):
            print("Layer {}".format(i))
            for j, neuron in enumerate(layer):
                print("\tNeuron {}, bias: {}".format(j, neuron.bias))
                if(neuron.output != None):
                    print("\t\toutput: {}".format(neuron.output))
                for k, weight in enumerate(neuron.weights):
                    print("\t\t\tweight: {}".format(weight))
    

    def sum_vectors(self,vector1, vector2):
        vector3 = []
        for i in range(len(vector1)):
            vector3.append(vector1[i]+vector2[i])
        return vector3
    

    # ------------------------------------------- Neural Netowrk functions ---------------------------------------------- #

    def get_output(self):
        output = []
        for n in self.neural_net[self.number_of_layers-1]:
            output.append(n.output)
        return output
    
    
    def input_data(self, data):
        for i in range(len(data)):
            self.neural_net[0][i].set_output(data[i])


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


    def copy(self):
        new_neural_net = []
        for layer in self.neural_net:
            new_layer = []
            for neuron in layer:
                new_neuron = neuron.copy()
                new_layer.append(new_neuron)
            new_neural_net.append(new_layer)
        return NeuralNetwork(neural_net=new_neural_net)


    def mutate_weights(self, neuron):
        sort = random.randint(0,1) #zero or 1
        if(sort == 1): #mutate wegths
            number_of_mutate_weights = random.randint(0, len(neuron.weights))
            for i in range(number_of_mutate_weights):
                idx_mutate = random.randint(0,len(neuron.weights)-1)
                new_weight = self.get_random_value()
                neuron.set_weight(idx_mutate,new_weight)
    

    def mutate_bias(self, neuron):
        sort = random.randint(0,1) #zero or 1
        if(sort == 1): #mutate wegths
            neuron.set_bias(self.get_random_value())


    def copy_with_mutation(self): #TODO where to mutation things, maybe limit the number of mutation?
        new_neural_net = []    
        for k in range(len(self.neural_net)):  
            layer = self.neural_net[k]
            new_layer = []
            for neuron in layer:
                new_neuron = neuron.copy() 
                if(k<self.number_of_layers-1):
                    self.mutate_bias(new_neuron)
                if(k>0):
                    self.mutate_weights(new_neuron)
                new_layer.append(new_neuron)
            new_neural_net.append(new_layer)
        return NeuralNetwork(neural_net = new_neural_net)

    # ------------------------------------------------------------------------------------------------------------------- #

#n = NeuralNetwork(file="gen0/brains/309")
#n.write_nn("test.txt")
#n.print()
#n2 = n.copy_with_mutation()
#n2.print()
#n.input_data([-571,519])
#n.run_net()
#print(n.get_output())