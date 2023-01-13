# Creation of neural network

class Neuron():

    def __init__(self, output=None, bias=None): 
        self.output = output
        self.bias = bias
    
    def set_output(self, output):
        self.output = output
    
    def set_bias(self, bias):
        self.bias = bias

class NeuralNetwork():

    def __init__(self, number_of_layers, number_of_neurons_per_layer, initial_biases=None, initial_weigths=None):
        self.number_of_layers = number_of_layers
        self.number_of_neurons_per_layer = number_of_neurons_per_layer
        self.neural_net = []
        for i in range(0, number_of_layers):
            layer = []
            for j in range(0, number_of_neurons_per_layer[i]):
                neuron = Neuron()



