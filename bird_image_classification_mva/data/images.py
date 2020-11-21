from tensorflow.keras.preprocessing.image import save_img
import tensorflow as tf
from bird_image_classification_mva.config.config import WIDTH, HEIGHT


def read_image(path, label=None, shape=(WIDTH, HEIGHT)):
    im_file = tf.io.read_file(path)
    im = tf.io.decode_jpeg(im_file, channels=3)
    im = tf.image.convert_image_dtype(im, tf.float32)
    im = tf.image.resize(im, shape)
    if label:
        return im, label
    else:
        return im


def write_image(path, img):
    save_img(path, img)
