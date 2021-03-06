import numpy as np
import random
from math import *

random.seed(0)


# load data

INPUT_COUNT = 4   # input vector size
OUTPUT_COUNT = 3   # output vector size

def load_data(filename):
    fs = open(filename, "r").read().split('\n')
    fs = [line.split(',') for line in fs]
    input_matrix = []
    output_matrix = []
    for i in range(len(fs)):
        input_data = [float(t) for t in fs[i][:INPUT_COUNT]]
        output_data = [float(fs[i][INPUT_COUNT][j] == '1') for j in range(OUTPUT_COUNT)]
        input_matrix.append(input_data[:])
        output_matrix.append(output_data[:])
    return [np.array(input_matrix), np.array(output_matrix)]

training_input, training_output = load_data("iris_training.dat")
validation_input, validation_output = load_data("iris_validation.dat")
testing_input, testing_output = load_data("iris_testing.dat")



# sigmoid function and its derivative
sigmoid = np.vectorize(lambda x: 0.5*(1.0+tanh(x)))
sigmoid_d = np.vectorize(lambda x: 0.5*(1.0-tanh(x)**2))


# initialize weight matrix, all value between -0.5 and 0.5
np.random.seed(0)
weight_mat = np.random.rand(INPUT_COUNT+1, OUTPUT_COUNT) - 0.5


# feed forward
def feed_forward(inputs):
    bias = np.full((inputs.shape[0], 1), 1.0)
    with_bias = np.concatenate((inputs, bias), axis=1)
    net = np.matmul(with_bias, weight_mat)
    return [sigmoid(net), net]

# evaluate error
def calc_error(output, target_output):
    diff = target_output - output
    return np.sum(diff**2) / diff.size



# back propagation

eta = 0.2   # learning rate

def backpropagation(inputs, target_output, weight):
    i = random.randrange(0, inputs.shape[0])
    output, net = feed_forward(np.array([inputs[i]]))
    diff = target_output[i] - output[0]
    delta = np.multiply(diff, sigmoid_d(net[0]))
    weight_delta = eta * np.tensordot(np.transpose(
        np.concatenate((inputs[i], [1]), axis=0)), delta, axes=0)
    return weight + weight_delta


# main train function

def train_main():
    global weight_mat
    iters = 0
    while iters < 10000:
        weight_mat = backpropagation(training_input, training_output, weight_mat)
        #output = feed_forward(training_input)[0]
        #err = calc_error(output, training_output)
        #print((iters, err), end=',')
        iters += 1
    output = feed_forward(training_input)[0]
    err = calc_error(output, training_output)
    return err

print(train_main())

print(weight_mat)



# test accuracy

def output_to_class(output):
    res = []
    for item in output:
        maxi = -1
        maxval = float("-inf")
        for i in range(len(item)):
            if item[i]>maxval:
                maxi, maxval = i, item[i]
        res.append(maxi)
    return res

output = feed_forward(testing_input)[0]
output = output_to_class(output)
expected_output = output_to_class(testing_output)

correct_count = 0
for i in range(len(output)):
    if output[i]==expected_output[i]:
        correct_count += 1
print("Accuracy:", correct_count/len(output))  # 0.92

