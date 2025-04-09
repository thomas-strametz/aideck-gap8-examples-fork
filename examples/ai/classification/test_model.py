import numpy as np
import tensorflow as tf
from PIL import Image
from pathlib import Path


def test_model(quantized=True):
    model_path = 'model/classification_q.tflite' if quantized else 'model/classification.tflite'
    dtype = np.uint8 if quantized else np.float32

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    print(interpreter.get_input_details())
    print(interpreter.get_output_details())
    print(interpreter.get_signature_list())
    f = interpreter.get_signature_runner(signature_key='serving_default')

    # x = np.asarray(Image.open('training_data_1/train/no_patch/004922.png')).astype(dtype).transpose().reshape(1, 324, 244, 1)
    # print(x.min(), x.max())

    total = {
        0: 0,
        1: 0
    }
    for file in Path('training_data_1/train/no_patch/').iterdir():
        x = np.asarray(Image.open(file)).astype(dtype).transpose().reshape(1, 324, 244, 1)
        res = f(input_2=x)
        print(res)
        idx = np.argmax(res['dense'])
        total[idx] += 1

    print(total)


def main2():
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=10,
        shear_range=0.2,
        zoom_range=0.1,
        horizontal_flip=True,
        brightness_range=[0.5, 1.5],
    )
    train_generator = train_datagen.flow_from_directory(
        f"training_data_1/train",
        target_size=(324, 244),
        batch_size=1,
        class_mode="categorical",
        color_mode="grayscale",
    )

    for x, y in train_generator:
        x = x.reshape(324, 244)
        x = Image.fromarray(x)
        x.show()
        print(y)
        break


if __name__ == '__main__':
    test_model(True)
