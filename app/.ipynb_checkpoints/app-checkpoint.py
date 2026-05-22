from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

MODEL_PATH = "D:\PomegranateGuard\model\pomegranate_final_model.h5"

model = load_model(MODEL_PATH)

classes = [
    "Healthy",
    "Bacterial Blight",
    "Anthracnose",
    "Fruit Rot"
]

@app.route("/", methods=["GET", "POST"])
def index():

    prediction = None

    if request.method == "POST":

        file = request.files["file"]

        if file:

            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            pred = model.predict(img_array)
            class_index = np.argmax(pred)

            prediction = classes[class_index]

    return render_template(
        "index.html",
        prediction=prediction
    )

if __name__ == "__main__":
    app.run(debug=True)