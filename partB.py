"""import os
os.system('pip install numpy')
os.system('pip install matplotlib')"""

import numpy as np
import matplotlib.pyplot as mtp
# import dataFiles_generator as df
from pathlib import Path

# df.return_files()
np.random.seed(0)
learn_rate = 4.5
loss_descend = []
training_epochs = []


# gets from the training data file the unary input and the classification for each of these unary numbers
def reading(file_train='training_data.txt'):
    file = open(file_train)
    data_set = []
    targets = []
    for x in file:
        unary_number, target1, target2 = x.strip('\n').split(',')
        data_set.append(list(map(int, list(unary_number))))  # converts the unary number into a set of bits
        targets.append([int(target1), int(target2)])

    return data_set, targets


dataset, Targets = reading()
dataset = np.array(dataset)
Targets = np.array(Targets)


# a function to start the training process
def initiation(n_epochs, network):
    file = open('training_progress.txt', 'w')
    global learn_rate
    print('')
    for i in range(n_epochs + 1):  # the network trains for n_epochs
        # for every fifty epochs decrease the learning rate by 1 %
        if i % 50 == 0:
            learn_rate = l_rate_decay(learn_rate)

        if i % 100 == 0:  # every 100 epochs the loss is displayed on screen
            # loss is calculated as the mean of differences squared
            print("        Loss: " + str(np.mean(np.square(Targets - network.feed_forward(dataset)))))
            file.write(f'Loss after {i} epochs is: {np.mean(np.square(Targets - network.feed_forward(dataset)))}\n')
            # every 100 epochs the loss is saved in order to plit the graph in opt 4
            loss_descend.append(np.mean(np.square(Targets - network.feed_forward(dataset))))
            training_epochs.append(i)
        # the network is trained with the dataset of inputs expecting the Targets as outputs
        network.train(dataset, Targets)


# a function that converts the approximated output into binary values
def binary(value):
    if value < 0.5:
        value = 0
    else:
        value = 1

    return value


# a function that zeroes the training of the neural network on the previous runs
# it is called every time the user asks to give a new topology
def training_zeroed():
    network = NeuralNet()
    loss_descend.clear()
    training_epochs.clear()
    return network


# a function that decays the learning rate by 1% every 50 epochs
def l_rate_decay(learning_rate):
    learning_rate = learning_rate - (learning_rate / 100)
    return learning_rate


# NeuralNet is the class representing the whole of a 3 layer Neural
# #network which take as arguments the number neurons in each layer
class NeuralNet(object):
    def __init__(self, hidden_layer=14, input_layer=10, output_layer=2):
        self.inputSize = input_layer
        self.outputSize = output_layer
        self.hiddenSize = hidden_layer
        # generates random weights for each connection in the network
        self.Weights1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.Weights2 = np.random.randn(self.hiddenSize, self.outputSize)

    # the process of calculating the outputs based on the usage of formulas and activation functions
    def feed_forward(self, data_set):
        self.outputs1 = np.dot(data_set, self.Weights1)  # + self.bias1  #added bias
        self.outputs1s = self.sigmoid(self.outputs1)
        self.outputs2 = np.dot(self.outputs1s, self.Weights2)  # + self.bias2   #added bias
        outputs2s = self.sigmoid(self.outputs2)
        return outputs2s

    # the activation function for the perceptron
    @staticmethod
    # the sigmoid takes a value as input ant returns a probability
    def sigmoid(s, derivative=False):
        if derivative:
            return s * (1 - s)
        return 1 / (1 + np.exp(-s))

    # here is where back propagation starts
    def backprop(self, data_set, targets, output):
        # calculates the error between the target and prediction
        output_error = targets - output
        output_delta = output_error * self.sigmoid(output, derivative=True)
        # calculates the error specific for each set of weights
        z2_error = output_delta.dot(self.Weights2.T)
        z2_delta = z2_error * self.sigmoid(self.outputs1s, derivative=True)
        # changes every weight in the network according to its specific weight in the overall error
        self.Weights1 += data_set.T.dot(z2_delta) * learn_rate
        self.Weights2 += self.outputs1s.T.dot(output_delta) * learn_rate

    # a function that takes the network through the forward pass and back propagation
    def train(self, data_set, targets):
        output = self.feed_forward(data_set)
        self.backprop(data_set, targets, output)


# instance of the artificial neural network
network = NeuralNet()

while 1:
    try:
        # menu for the user
        choice = int(input('''
        1) Enter network topology 
        2) Initiate a training pass
        3) Classify test data
        4) Display training result graphics
        5) Exit
             
        Please choose an option: '''))

    # checks if the type of the input is comaptible with the expected input
    except ValueError:  # in case the input is not an integer thn display the appropriate message
        print("        Not a Valid Input!!")
    # if the user input is acceptable the program proceeds with the menu
    else:
        # if the user chooses option one then the program will ask about the topology
        # however since the training dataset that we are providing dictates that the input layer will have
        # 10 neurons and the output layer will have 2 neurons then the difference between
        # topologies is decided by the size of the hidden layer
        if choice == 1:
            print("        you have selected option 1, '\n"
                  "        the default topology for this network is set to 10-14-2")

            while 1:
                try:
                    hidden_size = input("        Size of the Hidden Layer: ")
                    if hidden_size == "":
                        network = training_zeroed()
                        break
                    else:
                        hidden_size = int(hidden_size)

                except ValueError:
                    print("        an integer value is needed to create the hidden layer")
                else:
                    # every time a new topology is selected every advancement achieved by
                    # the previous trainings will be zeroed
                    network = training_zeroed()
                    # the new size of the hidden layer for the neural network is set according to users input
                    network.hiddenSize = hidden_size
                    break

        elif choice == 2:
            print("        you have selected option 2")
            # asks the user for the training file
            while 1:
                train_file = input('        What is the training file for this run: ')
                if train_file == '':
                    break
                else:
                    path = Path(train_file)

                if path.is_file():
                    break
                else:
                    print("        that file doe1s not exist")
                    continue
            # asks the user for the learning rate
            while 1:
                try:
                    learn_step = input("        Learning Rate: ")
                    if learn_step == '':
                        break
                    else:
                        learn_rate = float(learn_step)
                except ValueError:
                    print("        the value needs to be a float")
                else:
                    break
            # asks the user for the number of epochs. THIS VARIABLE DOES NOT HAVE A DEFAULT VALUE
            while 1:
                try:
                    n_Epochs = int(input("        Number of Epochs: "))
                except ValueError:
                    print("        the value needs to be an integer")
                else:
                    break
            # it starts the training process
            initiation(n_Epochs, network)

        elif choice == 3:
            # opens the file for the inputs
            input_file = open('input_data.txt')
            # opens the file for the outputs
            output_file = open('training_output.txt', 'w')
            # it reads every line in the input file
            # converts it into data that the network can use
            # runs that data through the trained network
            # it puts the binary approximated results in the output file
            for line in input_file:
                input_data = line.rstrip('\n').rstrip('')
                network_input = list(map(int, list(input_data)))
                network_output = network.feed_forward(network_input)
                output_file.write(f"{input_data},{binary(network_output[0])},{binary(network_output[1])}" + '\n')

            print('        the file: input_data.txt has been fed to the network ')
            print('        the results can be found in training_outputs.txt')

        elif choice == 4:
            print("        you have selected option 4")
            # takes the data to be plotted in the X and Y axis
            X = training_epochs
            Y = loss_descend

            mtp.plot(X, Y, "--")
            # labels the graph and axis
            mtp.xlabel('Training Epochs')
            mtp.ylabel('Loss Value')
            mtp.title('Loss descent')
            # sets the graph to be displayed in a logarithmic function
            mtp.yscale("log")
            mtp.show()

        elif choice == 5:
            break
        else:
            print("        not exactly a valid option")
