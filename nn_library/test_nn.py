import unittest
import sys
sys.path.append('.')
import nn_library.nn as nn


class TestNeuron(unittest.TestCase):
    
    def __init__(self,*args, **kw):
        super().__init__(*args, **kw)
        self.nn1 = nn.Neuron()
        self.nn2 = nn.Neuron(bias=2.5)
        self.nn3 = nn.Neuron(weights=[1,1,3,2.5])
        self.nn4 = nn.Neuron(2.5,[4,1,3,2.5])
        

    def test_constructor(self): 
        self.assertEqual(self.nn2.bias,2.5)
        self.assertEqual(self.nn3.weights,[1,1,3,2.5])
        self.assertEqual(self.nn4.weights,[4,1,3,2.5])
        self.assertEqual(self.nn4.bias,2.5)
    
    def teste_set_output(self): #TODO era para falhar
        pass
    
    def test_set_bias(self): #TODO fazer falhar tbm
        pass

    #TODO fazer teste para todos set's e verificar que o 
    #tipo é respeitado

    def test_calculate_output(self):
        self.nn1.set_sum(3.5)
        self.nn1.set_bias(2)
        result = self.nn1.calculate_output()
        self.assertEqual(result, 5.5)
        self.nn1.set_sum(-3.5)
        result = self.nn1.calculate_output()
        self.assertEqual(result, 0)
    
    def test_calculate_weights_times_output(self):
        self.nn4.set_output(2)
        result = self.nn4.calculate_weights_times_output()
        self.assertEqual(result,[8,2,6,5])
        self.nn4.set_output(3)
        result = self.nn4.calculate_weights_times_output()
        self.assertEqual(result,[12,3,9,7.5])

class TestNeuralNet(unittest.TestCase):
    def __init__(self,*args, **kw):
        super().__init__(*args, **kw)
        self.nn = nn.NeuralNetwork(file="my_net.txt")
    
    def test_output(self):
        input = [1,1]
        self.nn.input_data(input)
        self.nn.run_net()
        output = self.nn.get_output()
        self.assertEqual(output, [168,200])


if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()