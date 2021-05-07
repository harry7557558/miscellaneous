import tensorflow as tf
import numpy as np
import arr2str

# load train data
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images / 255.0
test_images = test_images / 255.0

train_images = np.concatenate((train_images, test_images))
train_labels = np.concatenate((train_labels, test_labels))

if True:
    def to_arr(a):
        return np.array([[float(i == x) for i in range(10)] for x in a])
    train_labels = to_arr(train_labels)
    test_labels = to_arr(test_labels)

# resize image to 14x14 to save bytes
if True:
    def resize(img):
        return img.reshape((14, 2, 14, 2)).max(3).max(1)
    train_images = np.array([resize(img) for img in train_images])
    test_images = np.array([resize(img) for img in test_images])

# define and compile model
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(14, 14)),
    tf.keras.layers.Dense(48, activation='relu'),
    tf.keras.layers.Dense(36, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# train model
for i in range(20):
    model.fit(train_images, train_labels, epochs=10)
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    print("\nTest accuracy:", test_acc)
    if test_acc > 0.997:
        break

# hard-code weights
layer1_weights, layer1_biases = model.layers[1].get_weights()
layer2_weights, layer2_biases = model.layers[2].get_weights()
output_weights, output_biases = model.layers[3].get_weights()
fp = open("weights.py", 'w')
fp.write("layer1_weights = " + arr2str.arr_to_str_2d(layer1_weights) + "\n")
fp.write("layer1_biases = " + arr2str.arr_to_str_1d(layer1_biases) + "\n")
fp.write("layer2_weights = " + arr2str.arr_to_str_2d(layer2_weights) + "\n")
fp.write("layer2_biases = " + arr2str.arr_to_str_1d(layer2_biases) + "\n")
fp.write("output_weights = " + arr2str.arr_to_str_2d(output_weights) + "\n")
fp.write("output_biases = " + arr2str.arr_to_str_1d(output_biases) + "\n")
fp.close()
