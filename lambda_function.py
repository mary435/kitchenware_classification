#!/usr/bin/env python
# coding: utf-8
#Marilina Orihuela: mary.orihuela@gmail.com

import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor


preprocessor = create_preprocessor('xception', target_size=(299,299))


interpreter = tflite.Interpreter(model_path='kitchenware-model.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


classes = ['cup', 
    'fork', 
    'glass', 
    'knife', 
    'plate', 
    'spoon'
    ]

url = 'https://raw.githubusercontent.com/mary435/kitchenware_classification/main/images/6172.jpg'

def predict(url):
    X = preprocessor.from_url(url)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)

    float_predictions = preds[0].tolist()

    return dict(zip(classes, float_predictions))


def lambda_handler(event, context):
    url = event['url']
    result = predict(url)
    return result

