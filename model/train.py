# This training script was adapted from https://github.com/rishab-sharma/cnn-hand-written-digit/blob/master/train.py

# 1. Declare Imports
import keras as k
import numpy as np

# 2. Declare Variables
batch_size = 128
# 10 classes represent the numbers 1-9
num_classes = 10
# 12 epochs for training - very short time
epochs = 12
# image dimensions are 28 x 28 pixels
img_rows, img_cols = 28, 28


# 3. LOAD DATA - Very easy using keras as mnist is built in
#    Split data into taining and test sets
(x_train, y_train), (x_test, y_test) = k.datasets.mnist.load_data()

# https://keras.io/backend/
# For 3D data:
# Channels_first assumes (channels, conv_dim1, conv_dim2, conv_dim3).
if k.backend.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    # Otherwise we assume its channels_last and uses (conv_dim1, conv_dim2, conv_dim3, channels)
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

# Lets make sure it's ok
print("Length of x_train: %s" % type(x_train)) # a numpy matrix perfect for keras
print("Length of x_train: %d" % len(x_train)) # 60000
print(len(x_test), len(y_test)) # 10000, 10000
print(y_train[0:20]) # The first 20 classes in y_train

# 4. FORMAT THE DATA FOR TRAINING
#    Scale the inputs to be in the range [0-1] rather than [0-255]
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# 5.    CONVERT THE MATRICES INTO ONE HOT FORMAT
#       https://keras.io/utils/
#       Using .to_categorical Converts a class vector (integers) to binary class matrix.
#       Keras.utils.to_categorical(y, num_classes=None)
y_train = k.utils.to_categorical(y_train, num_classes)
y_test = k.utils.to_categorical(y_test, num_classes)

# Print the first 10 elements of y_train
print("First 10 Elements in y_train:")
print(y_train[0:10])

# 6. BUILD THE NEURAL NETWORK
model = k.models.Sequential()
# This layer creates a convolution kernel that is coiled with the layer input 
# over a single spatial (or temporal) dimension to produce a tensor of outputs.
# https://keras.io/layers/convolutional/
model.add(k.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
# Add another Convolutional layer
model.add(k.layers.Conv2D(64, (3, 3), activation='relu'))
# Max pooling operation for spatial data.
model.add(k.layers.MaxPooling2D(pool_size=(2, 2)))
# Randomly turn neurons on and off to improve convergence
model.add(k.layers.Dropout(0.25))
# Flattens the input without effecting the batch size. https://keras.io/layers/core/#flatten
model.add(k.layers.Flatten())
# Just a regular densely-connected NN layer. https://keras.io/layers/core/
model.add(k.layers.Dense(128, activation='relu'))
# Add another dropout
model.add(k.layers.Dropout(0.5))
# Add the softmax activation function to the final layer
model.add(k.layers.Dense(num_classes, activation='softmax'))

# 7. COMPILE THE MODEL
model.compile(loss=k.losses.categorical_crossentropy,
              optimizer=k.optimizers.Adadelta(),
              metrics=['accuracy'])

# 8. FIT THE MODEL
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
 #how well did it do? 
score = model.evaluate(x_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

# The predict_classes function outputs the highest probability class
# according to the trained classifier for each input example.
y_pred = model.predict_classes(x_test)

# How many did we get wrong?!
true_indices = np.nonzero(y_pred == y_test)[0]
false_indices = np.nonzero(y_pred != y_test)[0]
print("Number of false predictions = %d (out of %d samples)" % (len(false_indices), len(y_test)))

#Save the model
# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("MODEL SAVED!")