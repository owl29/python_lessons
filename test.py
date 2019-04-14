# cording UTF-8
import sys
import numpy as np
data = np.random.rand(250,5)
labels = (np.sum(data, axis=1) > 2.5) * 1
print("labels:")
print(labels)
from keras.utils import np_utils
labels = np_utils.to_categorical(labels)
print("labels to_categorical")
print(labels)
from keras.models import Sequential
from keras.layers import Dense, Activation
model = Sequential()
model.add(Dense(20, input_dim=5))
model.add(Activation('relu'))
model.add(Dense(2, activation='softmax'))
model.compile('rmsprop', 'categorical_crossentropy', metrics=['accuracy'])
model.fit(data, labels, nb_epoch=300, validation_split=0.2)
#model.fit(data, labels, nb_epoch=10, validation_split=0.2)
test = np.random.rand(200, 5)
#print('test:')
#print(test)
predict = np.argmax(model.predict(test), axis=1)
print('model.predict')
print(model.predict(test).shape)
print(model.predict(test))

real = (np.sum(test, axis=1) > 2.5) * 1
print('real')
print(real)
print('sum=' , sum(predict == real) / 200.0)
