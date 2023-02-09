import tensorflow as tf
import numpy as np

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
from tensorflow.keras.applications.xception import preprocess_input

###
from config import *
import telebot
from telebot.types import ReplyKeyboardRemove #to remove keypad
import threading
import requests

#bot instance
bot = telebot.TeleBot(BOT_TOKEN)

###

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
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "give the welcome"),
        #telebot.types.BotCommand("/", ""),
        ])      #Here we add them so that they appear in the menu

    print('Initializing the bot')
    hilo_bot = threading.Thread(name="hilo_bot", target=receive_messages) #thread that receives messages and continues execution
    hilo_bot.start()
    print("Bot started")
    
    return {"Message": "This is Index go to /docs"}

### BOT

#respond to start command
@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    "Show available commands"
    markup = ReplyKeyboardRemove()

    intro = "This model classifies images of different kitchen utensils into 6 classes:\n"
    intro+= "*Cups \n*Glasses \n*Plates \n*Spoons \n*Forks \n*Knives"
    
    bot.send_message(message.chat.id, intro, reply_markup=markup)
    bot.send_message(message.chat.id, "Upload an image to classify it.", reply_markup=markup)

#responds when not commands
@bot.message_handler(content_types=["photo"])
def bot_mensajes_texto(message):
    "Manage received picture messages"
    file_id = message.photo[-1].file_id
    # get URL by id
    file_path = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}').json()['result']['file_path']
    # open URL with Pillow
    img = Image.open(requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}', stream=True).raw)
    # save on the disk if needed
    #img.save('photo.jpg')

    img = img.convert("RGB")
    img = img.resize((299,299))
    arr = np.array(img)
    arr = np.expand_dims(arr, axis=0)
    arr = preprocess_input(arr)
    prediction = MODEL.predict([arr])

    clases = ["Cup", "Fork", "Glass", "Knive", "Plate", "Spoon"]
    result = dict(zip(prediction[0], clases))
    pred = result[max(result)]
    response = f'In the photo there is a {pred}'
    markup = ReplyKeyboardRemove()
    #bot.send_message(message.chat.id, "Received", reply_markup=markup)

    bot.send_message(message.chat.id, response, reply_markup=markup)


def receive_messages():
    "Infinite loop checking for new messages"
    bot.infinity_polling() #repeat infinitely
    
### MAIN ###
#if __name__ == '__main__':
