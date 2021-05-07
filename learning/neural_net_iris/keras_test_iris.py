# tutorial: https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/

print("import modules...")
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# load dataset
print("load dataset...")

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

training_input = np.append(training_input, validation_input, axis=0)
training_output = np.append(training_output, validation_output, axis=0)
training_input = np.append(training_input, testing_input, axis=0)
training_output = np.append(training_output, testing_output, axis=0)


# define keras model
print("define keras model...")
model = Sequential()
model.add(Dense(12, input_dim=4, activation='relu'))  # first hidden layer: 12 nodes
model.add(Dense(8, activation='relu'))  # second hidden layer: 8 nodes
model.add(Dense(3, activation='softmax'))


# compile the keras model
# loss function, optimizer, metrics??
print("compile keras model...")
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# fit keras model
# training occurs over epoches and each epoch is split into batches
# epoch: one pass through all rows in the training dataset
# batch: one or more samples within an epoch before weights are updated
# train runs a fixed number of iterations through epochs
# batch_size: "number of dataset rows considered before the model weights are updated within each epoch"
print("fit keras model...")
old_accuracy = 0
for i in range(10):
    model.fit(training_input, training_output, epochs=100, batch_size=10)
    _, accuracy = model.evaluate(validation_input, validation_output)
    if abs(accuracy-old_accuracy) < 0.001:
        break
    old_accuracy = accuracy


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

expected = output_to_class(testing_output)
predicted = output_to_class(model.predict(testing_input))
correct_count = 0
for i in range(len(expected)):
    if expected[i]==predicted[i]:
        correct_count += 1
print(f"Accuracy: {correct_count/len(expected)}")


# get weights and biases
first_layer_weights, first_layer_biases = model.layers[0].get_weights()
second_layer_weights, second_layer_biases = model.layers[1].get_weights()
output_layer_weights, output_layer_biases = model.layers[2].get_weights()

print("first_layer_weights =", first_layer_weights.tolist())
print("first_layer_biases =", first_layer_biases.tolist())
print("second_layer_weights =", second_layer_weights.tolist())
print("second_layer_biases =", second_layer_biases.tolist())
print("output_layer_weights =", output_layer_weights.tolist())
print("output_layer_biases =", output_layer_biases.tolist())

