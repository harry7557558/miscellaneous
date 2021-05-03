# make predictions in pure Python

import math

# hard-coded weights for the neural network

first_layer_weights = [
       [ 0.24909703,  0.17292255, -0.32153338,  0.11188712, -0.08203626,
        -0.14299247, -0.05016446, -0.45131373, -0.06753423, -0.32200044,
         0.57339287,  0.26860192],
       [ 0.8059807 , -0.19713548,  0.20419137, -0.14716053, -0.21787052,
        -0.48559412, -0.46336883, -0.65673125,  0.22414847,  1.0482327 ,
        -0.2814466 ,  0.36324584],
       [-0.7034015 , -0.26021636, -0.1343824 , -0.16210754,  0.6012616 ,
        -0.30573916, -0.42552173,  0.16218401, -0.5137206 , -0.6828526 ,
         0.3655935 ,  1.2660981 ],
       [-0.8147002 , -0.11617795, -0.3559445 ,  0.20457472,  1.0107673 ,
        -0.2534015 , -0.08893281,  0.49700758, -0.353359  , -0.27748573,
        -0.47398743,  1.311092  ]]
first_layer_biases = [
        0.74126524,  0.        , -0.00858215, -0.09071941, -0.07469946,
        0.        ,  0.        , -0.09091268, -0.05520378,  0.60702854,
        0.24403912,  0.46426222]
second_layer_weights = [
       [-0.72243595,  0.30460718,  0.14330775, -1.4520068 ,  1.715989  ,
        -0.49822858, -0.27589303, -0.01782358],
       [-0.22150782, -0.19686913, -0.44515178,  0.08774668,  0.4027599 ,
         0.33268094,  0.00546402,  0.21703142],
       [ 0.49903667,  0.03388274,  0.13998145, -0.45127857, -0.13974473,
        -0.10627228,  0.17565626, -0.45919058],
       [ 0.24071375, -0.09462965, -0.11782023, -0.37591094,  0.20847447,
        -0.44966984, -0.2441801 , -0.46086025],
       [ 0.31700405,  0.1752389 , -0.3568077 ,  0.7780605 , -1.1284682 ,
         0.2999714 , -0.44959438, -0.3814993 ],
       [-0.23934016,  0.09856558, -0.3690163 , -0.53602433, -0.39238828,
         0.1900751 , -0.5473584 ,  0.19634324],
       [-0.36181897,  0.20556861,  0.30603027, -0.221062  , -0.50123185,
        -0.10782731,  0.35281616, -0.36554188],
       [ 0.05418552, -0.17515576,  0.35582906, -0.274366  ,  0.48323253,
        -0.13667613, -0.32240176,  0.15573233],
       [ 0.3401386 ,  0.44855154, -0.26341757,  0.4556467 , -0.4763664 ,
        -0.4304521 , -0.12617864, -0.03560984],
       [-0.52457803,  0.1318622 , -0.1729585 , -0.4537712 ,  1.3214463 ,
         0.11766535,  0.30998343, -0.21904302],
       [ 0.8294087 , -0.41095877, -0.16112676, -0.28321916,  0.43322685,
         0.31460595, -0.31157243, -0.06434318],
       [ 0.7325361 , -0.4042586 , -0.17069462,  1.1158487 ,  0.1939688 ,
        -0.4231797 , -0.42452282,  0.09673254]]
second_layer_biases = [
        0.38717046, -0.07082497,  0.        ,  0.12318973,  0.38251755,
        0.        , -0.02053171, -0.00858294]
output_layer_weights = [
       [-0.92908436,  0.593379  ,  0.26105708],
       [ 0.09708206,  0.50682104,  0.43719125],
       [ 0.222157  ,  0.737076  , -0.6315481 ],
       [-1.2479445 , -0.41892   ,  0.23975445],
       [ 1.082513  , -0.37393802, -1.8352257 ],
       [ 0.08774501, -0.6063447 , -0.5678228 ],
       [ 0.34960672,  0.5913268 ,  0.37091887],
       [ 0.6193131 ,  0.7320166 ,  0.6733965 ]]
output_layer_biases = [-0.1887059 ,  0.01901347, -0.24142721]


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
    return (input_matrix, output_matrix)

training_input, training_output = load_data("iris_training.dat")
validation_input, validation_output = load_data("iris_validation.dat")
testing_input, testing_output = load_data("iris_testing.dat")


# classification

def relu(x):
    return max(x, 0)

def sigmoid(x):
    return 0.5*(1.0+math.tanh(x))

def classify(input0):
    layer1 = []
    for i in range(12):
        s = first_layer_biases[i]
        for j in range(4):
            s += first_layer_weights[j][i] * input0[j]
        layer1.append(relu(s))
    layer2 = []
    for i in range(8):
        s = second_layer_biases[i]
        for j in range(12):
            s += second_layer_weights[j][i] * layer1[j]
        layer2.append(relu(s))
    output = []
    for i in range(3):
        s = output_layer_biases[i]
        for j in range(8):
            s += output_layer_weights[j][i] * layer2[j]
        output.append(sigmoid(s))
    return output

def output_to_class(output):
    maxi = -1
    maxval = float("-inf")
    for i in range(len(output)):
        if output[i]>maxval:
            maxi, maxval = i, output[i]
    return maxi


# test accuracy

def test_accuracy(input, output):
    N = len(input)
    correct_count = 0
    for i in range(N):
        expected = output_to_class(output[i])
        predicted = output_to_class(classify(input[i]))
        if expected == predicted:
            correct_count += 1
    print(f"{correct_count}/{N} ({correct_count/N})")

test_accuracy(training_input, training_output)
test_accuracy(validation_input, validation_output)
test_accuracy(testing_input, testing_output)
