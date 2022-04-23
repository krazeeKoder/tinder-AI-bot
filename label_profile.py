import os
import numpy as np
from PIL import Image
import tensorflow as tf


def load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]


def get_res(image, model_file, label_file, input_mean, input_std):
    interpreter = tf.lite.Interpreter(model_path=model_file)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # check the type of the input tensor
    floating_model = input_details[0]['dtype'] == np.float32

    # NxHxWxC, H:1, W:2
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    img = Image.open(image).resize((width, height))

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    final_res = {}
    for i in top_k:
        if floating_model:
            final_res[float(results[i])] = labels[i]
        else:
            final_res[float(results[i] / 255.0)] = labels[i]

    return final_res


def get_key(val, dict):
    for key, value in dict.items():
        if val == value:
            return key


def get_score(res):
    face_like = get_key('face_like', res)
    body_like = get_key('body_like', res)
    indifferent = get_key('indifferent', res)
    body_dislike = get_key('body_dislike', res)
    face_dislike = get_key('face_dislike', res)

    score = ((face_like + body_like) - (face_dislike + body_dislike)) / indifferent
    return score


def label_all_pictures(current_profile_dir):
    score = 0

    # for each pic print labels and score
    for photo in os.listdir(current_profile_dir):
        image = current_profile_dir + photo
        res = get_res(image, "model.tflite", "class_labels.txt", 0, 255)
        score += get_score(res)

    print(score)
    if score > 0:
        return True
    return False
