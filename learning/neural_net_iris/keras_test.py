# tutorial: https://machinelearningmastery.com/tutorial-first-neural-network-python-keras/

print("import modules...")
import numpy as np
from keras.models import Sequential
from keras.layers import Dense

# load dataset
print("load dataset...")
dataset = np.loadtxt('pima-indians-diabetes.dat', delimiter=',')
X = dataset[:,0:8]  # input
Y = dataset[:,8]  # output

# define keras model
print("define keras model...")
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))  # first hidden layer: 12 nodes
model.add(Dense(8, activation='relu'))  # second hidden layer: 8 nodes
model.add(Dense(1, activation='sigmoid'))

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
model.fit(X, Y, epochs=20, batch_size=10)

# test accuracy
N = len(X)
predictions = model.predict(X).reshape((N))
Y = Y.reshape((N))
correct_count = 0
for i in range(N):
    actual = Y[i]
    predicted = round(predictions[i])
    if actual==predicted:
        correct_count += 1
print(f"Accuracy: {correct_count/N}")

# get weights and biases
first_layer_weights, first_layer_biases = model.layers[0].get_weights()
second_layer_weights, second_layer_biases = model.layers[1].get_weights()
output_layer_weights, output_layer_biases = model.layers[2].get_weights()
