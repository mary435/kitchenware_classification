#!/usr/bin/env python
# coding: utf-8
#Marilina Orihuela: mary.orihuela@gmail.com

#%%
import numpy as np

import tensorflow as tf
from tensorflow import keras

import tensorflow.lite as tflite


#%%
model = keras.models.load_model('kitchenware-model.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)

tflite_model = converter.convert()

with open('kitchenware-model.tflite', 'wb') as f_out:
    f_out.write(tflite_model)


