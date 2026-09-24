from pathlib import Path
import tensorflow
import numpy
from io import BytesIO

IMAGE_SIZE = (128, 128)

MODEL_PATH = Path(__file__).resolve().parent / "DATA" / "waste_model.keras"
CLASS_NAMES_PATH = Path(__file__).resolve().parent / "DATA" / "class_names.txt"

model = tensorflow.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r") as f:
    class_names = [line.strip() for line in f]


def predict_image(image):

    image = tensorflow.keras.utils.load_img(
        BytesIO(image.read()),
        target_size=IMAGE_SIZE
    )

    image_array = tensorflow.keras.utils.img_to_array(image)

    image_array = tensorflow.expand_dims(image_array, 0)

    predictions = model.predict(image_array, verbose=0)

    predicted_index = numpy.argmax(predictions[0])

    predicted_class = class_names[predicted_index]

    confidence = predictions[0][predicted_index] * 100

    return predicted_class, confidence