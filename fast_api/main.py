import tensorflow as tf
import numpy as np

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
from tensorflow.keras.applications.xception import preprocess_input

MODEL = tf.keras.models.load_model('model/')

app_description = """
Classify images of different kitchenware items into 6 classes:

* cups
* glasses
* plates
* spoons
* forks
* knives

Use the "Try it" option and upload an image.    
Upon execution, you will receive the response with the probability of each class and the most probable class.
"""

app = FastAPI(
    title="Kitchenware Classification",
    description=app_description,
    contact={
        "name": "Marilina Orihuela",
        "email": "mary.orihuela@gmail.com"
    }
)

@app.post("/image/upload")
async def upload_image(file: UploadFile = File(...)):
    # código para procesar la imagen

    picture = Image.open(file.file)
    picture = picture.convert("RGB")
    picture = picture.resize((299, 299))

    arr = np.array(picture)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    
    prediction = MODEL.predict([arr])

    clases = ["cup", "fork", "glass", "knife", "plate", "spoon"]
    result = dict(zip(prediction[0], clases))

    cup = float(prediction[0][0])
    fork = float(prediction[0][1]) 
    glass = float(prediction[0][2])
    knife = float(prediction[0][3])
    plate = float(prediction[0][4])
    spoon = float(prediction[0][5])

    return JSONResponse({
        "filename":file.filename, 
        "prediction": result[max(result)],
        "cup": cup, 
        "fork": fork, 
        "glass": glass, 
        "knife": knife, 
        "plate": plate, 
        "spoon": spoon},
        status_code=200)


@app.get('/')
async def index():
    return {"Message": "This is Index go to /docs"}