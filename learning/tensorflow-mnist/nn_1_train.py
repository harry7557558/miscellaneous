import tensorflow as tf
import numpy as np
import arr2str

# load train data
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images / 255.0
test_images = test_images / 255.0

if True:
    def to_arr(a):
        return np.array([[float(i == x) for i in range(10)] for x in a])
    train_labels = to_arr(train_labels)
    test_labels = to_arr(test_labels)

# define and compile model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# train model
model.fit(train_images, train_labels, epochs=20)

test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print("\nTest accuracy:", test_acc)

# hard-code weights
weights, biases = model.layers[1].get_weights()
weights_str = arr2str.arr_to_str_2d(weights)
biases_str = arr2str.arr_to_str_1d(biases)
fp = open("weights.py", 'w')
fp.write("weights = " + weights_str + "\n")
fp.write("biases = " + biases_str + "\n")
fp.close()
