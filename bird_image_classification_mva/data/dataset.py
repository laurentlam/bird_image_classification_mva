from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.preprocessing import image

from bird_image_classification_mva.config.config import WIDTH, HEIGHT, BATCH_SIZE, SEED


def load_dataset(path, batch_size=BATCH_SIZE, image_size=(WIDTH, HEIGHT), shuffle=True):

    return image_dataset_from_directory(
        path,
        labels="inferred",
        label_mode="int",
        class_names=None,
        color_mode="rgb",
        batch_size=batch_size,
        image_size=image_size,
        shuffle=shuffle,
        seed=SEED,
        validation_split=None,
        subset=None,
        interpolation="bilinear",
        follow_links=False,
    )
