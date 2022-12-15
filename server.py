import time
import base64
import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np
from tensorflow import keras
import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

segmentor = SelfiSegmentation()
black = (0, 0, 0)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/screenshot', methods=['POST'])
def screenshot():
    image = get_image_from_request()
    image_norm, imgNoBg = preprocess_image(image)
    result = classify(image_norm)
    print(f'RESULT: {result}')
    cv2.imwrite(f'images/scr-{time.time()}-{result}.png', imgNoBg)
    return result


def get_image_from_request():
    json = request.get_json()
    image_base64 = json['image'].split(',')[1]
    image = cv2.imdecode(np.fromstring(base64.b64decode(image_base64), np.uint8), cv2.COLOR_BGR2RGB)
    return image


def classify(image_norm):
    model = keras.models.load_model('model')
    predicted = np.round(model.predict(image_norm))
    with open("model/encoder.pickle", "rb") as f:
        encoder = pickle.load(f)
    result = encoder.inverse_transform(predicted)[0]
    return result


def preprocess_image(image):
    crop = image[50:400, 100:650]
    image = cv2.resize(crop, (270, 175))
    imgNoBg = segmentor.removeBG(image, black, threshold=0.50)
    image_norm = np.array(imgNoBg) / 255.0
    image_norm = np.expand_dims(image_norm, axis=0)
    return image_norm, imgNoBg
