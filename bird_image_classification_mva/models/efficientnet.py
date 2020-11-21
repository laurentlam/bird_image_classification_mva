from tensorflow.keras.layers.experimental import preprocessing

from keras.preprocessing import image
from keras import layers
from keras.layers import Input, Flatten, Dense
from keras.models import Model
import numpy as np
from tensorflow.keras.applications import (
    EfficientNetB0,
    EfficientNetB1,
    EfficientNetB2,
    EfficientNetB3,
    EfficientNetB4,
    EfficientNetB5,
    EfficientNetB6,
    EfficientNetB7,
)
from bird_image_classification_mva.config.config import WIDTH, HEIGHT, SEED

import matplotlib.pyplot as plt
import tensorflow as tf


def build_model(num_classes, model="B7"):
    inputs = layers.Input(shape=(WIDTH, HEIGHT, 3))
    if model == "B7":
        model = EfficientNetB7(include_top=False, input_tensor=inputs, weights="imagenet")
    elif model == "B6":
        model = EfficientNetB6(include_top=False, input_tensor=inputs, weights="imagenet")
    elif model == "B5":
        model = EfficientNetB5(include_top=False, input_tensor=inputs, weights="imagenet")
    elif model == "B4":
        model = EfficientNetB4(include_top=False, input_tensor=inputs, weights="imagenet")
    elif model == "B3":
        model = EfficientNetB3(include_top=False, input_tensor=inputs, weights="imagenet")
    elif model == "B2":
        model = EfficientNetB2(include_top=False, input_tensor=inputs, weights="imagenet")
    elif model == "B1":
        model = EfficientNetB1(include_top=False, input_tensor=inputs, weights="imagenet")
    elif model == "B0":
        model = EfficientNetB0(include_top=False, input_tensor=inputs, weights="imagenet")
    # Freeze the pretrained weights
    model.trainable = False

    # Rebuild top
    x = layers.GlobalAveragePooling2D(name="avg_pool")(model.output)
    x = layers.BatchNormalization()(x)

    top_dropout_rate = 0.2
    x = layers.Dropout(top_dropout_rate, name="top_dropout", seed=SEED)(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    # Compile
    model = tf.keras.Model(inputs, outputs, name="EfficientNet")
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-2)
    model.compile(
        optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=[tf.keras.metrics.SparseTopKCategoricalAccuracy(k=1)]
    )
    return model


def plot_hist(hist):
    plt.plot(hist.history["sparse_top_k_categorical_accuracy"])
    plt.plot(hist.history["val_sparse_top_k_categorical_accuracy"])
    plt.title("model sparse_top_k_categorical_accuracy")
    plt.ylabel("sparse_top_k_categorical_accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "validation"], loc="upper left")
    plt.show()


def unfreeze_model(model):
    # We unfreeze the top 20 layers while leaving BatchNorm layers frozen
    for layer in model.layers[-20:]:
        if not isinstance(layer, layers.BatchNormalization):
            layer.trainable = True

    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(
        optimizer=optimizer, loss="sparse_categorical_crossentropy", metrics=[tf.keras.metrics.SparseTopKCategoricalAccuracy(k=1)]
    )
