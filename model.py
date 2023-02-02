from nn_library.nn import NeuralNetwork

nn_eskeleton = [8,6,4] #default neural net for our model

class OrganismBrain:
    

    def __init__(self,neural_net=None):
        self.number_of_feeding = 0
        self.time_alive = 0
        if(neural_net == None):
            self.nn = NeuralNetwork(number_of_neurons_per_layer=nn_eskeleton)
        else: 
            self.nn = neural_net


    def increment_number_of_feeding(self):
        self.number_of_feeding+=1
    

    def get_number_of_feeding(self):
        return self.number_of_feeding


    def reset_number_of_feeding(self):
        self.number_of_feeding = 0
    

    def set_time_alive(self, time): 
        self.time_alive = time
    

    def get_time_alive(self):
        return self.time_alive


    def copy_with_mutation(self):
        new_nn = self.nn.copy_with_mutation()
        return OrganismBrain(neural_net=new_nn)
        

    def get_environment_info(self, coords):
        self.nn.input_data(coords)
    

    def response(self):
        self.nn.run_net()
        output = self.nn.get_output()
        max = output[0]
        idx = 0
        for i in range(len(output)):
            if(output[i]>max):
                max == output[i]
                idx = i
        if(idx==0):
            return "up"
        if(idx==1):
            return "down"
        if(idx==2):
            return "right"
        if(idx==3):
            return "left"
    
    def scan(self,file):
        self.nn.write_nn(file)