# Creation of neural network

import random

class Neuron():

    def __init__(self, bias=None, weigths=[]): 
        self.output = None
        self.bias = bias
        self.weigths = weigths
    
    def set_output(self, output):
        self.output = output
    
    def set_bias(self, bias):
        self.bias = bias
    
    def set_weigths(self, weigths):
        self.wegths = weigths

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
                print("Neuron {}, bias: {}".format(j, neuron.bias))
                for k, weigth in enumerate(neuron.weigths):
                    print("weigth: {}".format(weigth))


nn = NeuralNetwork(3, [2,5,2])
nn.print_neural_net()



                    



