import numpy as np
import tensorflow as tf
from matplotlib import image
import matplotlib.pyplot as plt

# shape=(256,256), dtype=float
image = image.imread('cameraman.png').min(2)


x = np.zeros((256*256,2))
for i in range(256*256):
    x[i][0] = (i//256)/255
    x[i][1] = (i%256)/255

y = image.reshape((256*256, 1))



activation = tf.math.sin

model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, input_dim=2),
    tf.keras.layers.Activation(activation),
    tf.keras.layers.Dense(16, input_dim=2),
    tf.keras.layers.Activation(activation),
    tf.keras.layers.Dense(16, input_dim=2),
    tf.keras.layers.Activation(activation),
    tf.keras.layers.Dense(16, input_dim=2),
    tf.keras.layers.Activation(activation),
    tf.keras.layers.Dense(1)
])

model.compile(
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.03, momentum=0.9),
    loss='mean_squared_error', metrics=['accuracy'])

for i in range(100):
    model.fit(x, y, epochs=10, batch_size=len(x)//100, verbose=0)
    
    loss = model.evaluate(x, y, verbose=0)[0]
    print("loss =", loss)
    

    y1 = model.predict(x)

    plt.clf()
    fig, axes = plt.subplots(ncols=2)
    axes[0].imshow(y.reshape((256,256)), cmap=plt.get_cmap('gray'))
    axes[1].imshow(y1.reshape((256,256)), cmap=plt.get_cmap('gray'))
    plt.savefig('.temp/reg_2d_siren_{:002d}.png'.format(i+1))



