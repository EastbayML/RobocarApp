#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from __future__ import print_function
import numpy as np
#np.random.seed(1337)
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers.convolutional import ZeroPadding2D
from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json
import os
import matplotlib.pyplot as plt


# In[ ]:




# In[ ]:

batch_size = 16
nb_classes = 9
#image_size=(218,303)
#input_shape=(3,218,303)
image_size=(128,128)
input_shape=(3,128,128)
classes=["chicken","ostrich",'bluebird','finch','frog','salemander','cobra','bird','flamingo']


# In[ ]:

train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(
        '/Users/prav/cs231n_project/data/train',
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical')
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = train_datagen.flow_from_directory(
        '/Users/prav/cs231n_project/data/val',
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical')


# In[ ]:

nb_epoch = 2
nb_filters=32
kernel_size=(3,3)
pool_size=(2,2)


# In[ ]:

model = Sequential()
# model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
#                        border_mode='valid',
#                        input_shape=input_shape))
# model.add(Activation('relu'))
# model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=pool_size))
# model.add(Convolution2D(nb_filters, kernel_size[0], kernel_size[1]))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=pool_size))
# model.add(Dropout(0.25))
# model.add(Flatten())
# model.add(Dense(128))
# model.add(Activation('relu'))
# model.add(Dropout(0.5))
# model.add(Dense(nb_classes))
# model.add(Activation('softmax'))

model.add(ZeroPadding2D(padding=(1,1),input_shape=input_shape))
model.add(Convolution2D(64, kernel_size[0], kernel_size[1],
                        border_mode='valid',
                        input_shape=input_shape))
model.add(Activation('relu'))

model.add(ZeroPadding2D(padding=(1,1)))
model.add(Convolution2D(64, kernel_size[0], kernel_size[1],
                        border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))



model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(128, kernel_size[0], kernel_size[1],
                        border_mode='valid'))
model.add(Activation('relu'))

model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(128, kernel_size[0], kernel_size[1],
                        border_mode='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))


model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(256, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))

model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(256, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))

model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(256, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))

model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))

model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))

model.add(ZeroPadding2D((1,1)))
model.add(Convolution2D(512, kernel_size[0], kernel_size[1]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=pool_size))

model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(258))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes))
model.add(Activation('softmax'))


# In[ ]:

model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])


# In[ ]:

model.fit_generator(train_generator,samples_per_epoch=100, nb_epoch=nb_epoch, validation_data=test_generator,nb_val_samples=100,verbose=1)

model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
