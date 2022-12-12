import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.applications.xception import decode_predictions
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#%%
def test_model_image(file):
    path = './kitchenware-classification/images'
    classes = ['cup', 'fork', 'glass', 'knife', 'plate', 'spoon']
    ###
    fullname_img = f'{path}/{file}'
    img = load_img(fullname_img, target_size=(299, 299))
    x = np.array(img)
    X = np.array([x])
    X1 = preprocess_input(X)
    pred = model.predict(X1)
    result = dict(zip(pred[0], classes))
    
    return result[max(result)]

#%%
# Test model
model_name = 'xception_v4_06_0.955_larger.h5'
model = keras.models.load_model(model_name)
    
###
path = './kitchenware-classification/'
name = 'sample_submission.csv'
fullname_sample = f'{path}/{name}'
sample = pd.read_csv(fullname_sample)
#sample.columns = sample.columns.str.lower().str.replace(' ', '-')
ext = '.jpg'
sample['file'] = sample['Id'].astype(str).str.zfill(4) + ext 

###
del sample['label']
sample['label'] = sample['file'].apply(test_model_image)    

del sample['file']
sample.to_csv('submission.csv', index=False)


