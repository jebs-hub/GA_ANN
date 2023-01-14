# Creation of neural network

import random

class Neuron():

    def __init__(self, bias=None, weigths=[]): 
        self.output = None
        self.bias = bias
        self.weigths = weigths
        self.sum = 0
        self.weigths_times_output = []
    
    def set_output(self, output):
        self.output = output
    
    def calculate_output(self): #get sum, use bias and function
        self.output = self.bias + self.sum
        if(self.output < 0):
            self.output = 0
    
    def set_bias(self, bias):
        self.bias = bias
    
    def set_weigths(self, weigths):
        self.wegths = weigths
    
    def increment_sum(self, sum):
        self.sum += sum

    def set_sum(self, sum):
        self.sum = sum
    
    def calculate_weigths_times_output(self):
        for w in self.weigths:
            product = self.output*w
            self.weigths_times_output.append(product)

class NeuralNetwork():

    def __init__(self, number_of_layers, number_of_neurons_per_layer):
        self.number_of_layers = number_of_layers
        self.number_of_neurons_per_layer = number_of_neurons_per_layer
        self.neural_net = []
        for i in range(0, number_of_layers):
            layer = []
            for j in range(number_of_neurons_per_layer[i]):
                if(i < number_of_layers-1): #existe pesos nos neurônios
                    weigths = []
                    bias = random.uniform(-5,5)
                    for k in range(number_of_neurons_per_layer[i+1]): #cria os pesos
                        weigth = random.uniform(-5,5)
                        weigths.append(weigth)
                    neuron = Neuron(bias, weigths)
                else:
                    bias = random.uniform(-5,5)
                    neuron = Neuron(bias)
                layer.append(neuron)
            self.neural_net.append(layer)


    def print_neural_net(self):
        for i, layer in enumerate(self.neural_net):
            print("Layer {}".format(i))
            for j, neuron in enumerate(layer):
                print("\tNeuron {}, bias: {}".format(j, neuron.bias))
                if(neuron.output != None):
                    print("\t\toutput: {}".format(neuron.output))
                for k, weigth in enumerate(neuron.weigths):
                    print("\t\t\tweigth: {}".format(weigth))
    
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
                n.calculate_weigths_times_output()
                result = n.weigths_times_output
                sum_results = self.sum_vectors(sum_results, result)
            if(i < self.number_of_layers-1):
                for idx, n in enumerate(self.neural_net[i+1]):
                    n.set_sum(sum_results[idx])
                    n.calculate_output()



nn = NeuralNetwork(5, [3,5,2,7,1])
nn.input_data([0,3,2])
nn.run_net()
nn.print_neural_net()



                    



