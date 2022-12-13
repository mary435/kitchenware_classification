#!/usr/bin/env python
# coding: utf-8
# Marilina Orihuela: mary.orihuela@gmail.com

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.applications.xception import decode_predictions
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#%% Files
path = './kitchenware-classification/'
name = 'train.csv'
fullname_train = f'{path}/{name}'
train = pd.read_csv(fullname_train)

ext = '.jpg'
train['file'] = train['id'].astype(str).str.zfill(4)+ ext

name = 'test.csv'
fullname_test = f'{path}/{name}'
test = pd.read_csv(fullname_test)
test['file'] = test['id'].astype(str).str.zfill(4) + ext

# %%Model

def make_model(input_size = 150,learning_rate=0.01, size_inner=100, 
               droprate=0.5):
    base_model = Xception(
        weights='imagenet',
        include_top=False,
        input_shape=(input_size, input_size, 3)
    )

    base_model.trainable = False

    #########################################

    inputs = keras.Input(shape=(input_size, input_size, 3))
    base = base_model(inputs, training=False)
    vectors = keras.layers.GlobalAveragePooling2D()(base)
    
    inner = keras.layers.Dense(size_inner, activation='relu')(vectors)
    drop = keras.layers.Dropout(droprate)(inner)
    
    outputs = keras.layers.Dense(6)(drop)
    
    model = keras.Model(inputs, outputs)
    
    #########################################

    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    loss = keras.losses.CategoricalCrossentropy(from_logits=True)

    model.compile(
        optimizer=optimizer,
        loss=loss,
        metrics=['accuracy']
    )
    
    return model

#%%
train_datagen = ImageDataGenerator(rescale=1./255.,
                           validation_split=0.25)

train_ds = train_datagen.flow_from_dataframe(
    dataframe = train,
    directory = "kitchenware-classification/images/",
    x_col = 'file',
    y_col = 'label',
    has_ext=True,
    target_size=(input_size, input_size),
    batch_size=32,
    shuffle=True,
    class_mode='categorical',
    subset = "training"
    
)

val_datagen=ImageDataGenerator(rescale=1./255.,validation_split=0.25)

val_ds = val_datagen.flow_from_dataframe(
    dataframe = train,
    directory = "kitchenware-classification/images/",
    x_col = 'file',
    y_col = 'label',
    has_ext = True,
    target_size = (input_size, input_size),
    batch_size = 32,
    shuffle = False,
    class_mode = 'categorical',
    subset = "validation"
    
)

chechpoint = keras.callbacks.ModelCheckpoint(
    'xception_v4_{epoch:02d}_{val_accuracy:.3f}_larger.h5',
    save_best_only=True,
    monitor='val_accuracy',
    mode='max'
)

learning_rate = 0.01
size = 100
droprate = 0.5
input_size = 299

model = make_model(
        input_size = 299,
        learning_rate=learning_rate,
        size_inner=size,
        droprate=droprate
)

history = model.fit(train_ds, epochs=10, 
                        validation_data=val_ds,
                       callbacks=[chechpoint])



#Best model xception_v4_06_0.955_larger.h5
#kitchenware-model.h5