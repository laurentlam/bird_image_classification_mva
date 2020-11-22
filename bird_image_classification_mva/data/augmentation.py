from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import tensorflow as tf
import os
from bird_image_classification_mva.config.config import (
    SEED,
    DATASET_PATH,
    RESAMPLED_DATASET_PATH,
    AUGMENT_DATASET_PATH,
    N_AUGMENT_PER_FILE,
    EXTRACT_IMAGES,
)
from bird_image_classification_mva.data.images import read_image

from tensorflow.keras.preprocessing.image import load_img, save_img, smart_resize
from tqdm import tqdm
import glob
from shutil import copyfile

import imgaug as ia
import imgaug.augmenters as iaa
import cv2


def build_augmenters(imgaug=True):
    if imgaug:
        ia.seed(SEED)
        sometimes = lambda aug: iaa.Sometimes(0.8, aug, seed=SEED)

        augmenters = iaa.Sequential(
            [
                iaa.SomeOf(
                    (1, 3) if EXTRACT_IMAGES else (2, 4),
                    [
                        iaa.Add((-10, 10), per_channel=0.5, seed=SEED),
                        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5, seed=SEED),
                        iaa.OneOf(
                            [
                                iaa.GaussianBlur(sigma=(0, 0.5), seed=SEED),
                                iaa.AverageBlur(k=1, seed=SEED),
                                iaa.MedianBlur(k=1, seed=SEED),
                            ],
                            seed=SEED,
                        ),
                        iaa.LinearContrast((0.8, 1.2), per_channel=0.5, seed=SEED),
                    ],
                ),
                sometimes(
                    iaa.OneOf(
                        [
                            iaa.Fliplr(0.5, seed=SEED),
                            iaa.Flipud(0.2, seed=SEED),
                        ],
                        seed=SEED,
                    ),
                ),
                sometimes(
                    iaa.Affine(
                        scale={"x": (0.5, 1) if EXTRACT_IMAGES else (0.8, 1.2), "y": (0.5, 1) if EXTRACT_IMAGES else (0.8, 1.2)},
                        translate_percent={
                            "x": (-0.01, 0.01) if EXTRACT_IMAGES else (-0.2, 0.2),
                            "y": (-0.01, 0.01) if EXTRACT_IMAGES else (-0.2, 0.2),
                        },
                        rotate=(-25, 25) if EXTRACT_IMAGES else (-45, 45),
                        shear=(-16, 16),
                        order=[0, 1],
                        cval=(0, 255),
                        mode=ia.ALL,
                        seed=SEED,
                    )
                ),
            ],
            random_order=True,
            seed=SEED,
        )
        return augmenters
    else:
        img_augmentation = Sequential(
            [
                preprocessing.RandomRotation(factor=0.3, seed=SEED),
                preprocessing.RandomTranslation(
                    height_factor=0.01 if EXTRACT_IMAGES else 0.2, width_factor=0.01 if EXTRACT_IMAGES else 0.2, seed=SEED
                ),
                preprocessing.RandomFlip(seed=SEED),
                preprocessing.RandomContrast(factor=0.1 if EXTRACT_IMAGES else 0.2, seed=SEED),
            ],
            name="img_augmentation",
        )
        return img_augmentation


def create_augmented_dataset(
    class_names,
    dataset_path=DATASET_PATH,
    new_dataset_path=AUGMENT_DATASET_PATH,
    imgaug=True,
    n_augment_per_file=N_AUGMENT_PER_FILE,
):
    if not os.path.isdir(new_dataset_path):
        os.makedirs(new_dataset_path)
        print("Creating folder at {}".format(new_dataset_path))
    if not os.path.isdir(new_dataset_path + "train_images/"):
        os.makedirs(new_dataset_path + "train_images/")
        print("Creating folder at {}".format(new_dataset_path + "train_images/"))
    augmenters = build_augmenters(imgaug=imgaug)
    for class_name in tqdm(class_names):
        train_filepaths_per_class = glob.glob(dataset_path + "train_images/" + class_name + "/*.jpg")
        if not os.path.isdir(new_dataset_path + "train_images/{}/".format(class_name)):
            os.makedirs(new_dataset_path + "train_images/" + class_name + "/")
        for filepath in train_filepaths_per_class:
            if imgaug:
                image = cv2.imread(filepath)
            else:
                image = read_image(filepath)
            new_img_path = new_dataset_path + "train_images/" + class_name + "/" + filepath.split("/")[-1]
            copyfile(filepath, new_img_path)
            for image_index in range(n_augment_per_file):
                if imgaug:
                    image_aug = augmenters(image=image)
                else:
                    image_aug = augmenters(tf.expand_dims(image, axis=0))
                image_aug_path = (
                    new_dataset_path
                    + "train_images/"
                    + class_name
                    + "/"
                    + filepath.split("/")[-1][:-4]
                    + "_{}".format(image_index)
                    + ".jpg"
                )
                if imgaug:
                    cv2.imwrite(image_aug_path, image_aug)
                else:
                    save_img(image_aug_path, image_aug[0])