from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import tensorflow as tf
import os
from bird_image_classification_mva.config.config import SEED, DATASET_PATH, AUGMENT_DATASET_PATH, N_AUGMENT_PER_FILE
from bird_image_classification_mva.data.classes import retrieve_class_names
from bird_image_classification_mva.data.images import read_image

from tensorflow.keras.preprocessing.image import load_img, save_img, smart_resize
from tqdm import tqdm
import glob
from shutil import copyfile

import imgaug as ia
import imgaug.augmenters as iaa
import cv2


ia.seed(SEED)

sometimes = lambda aug: iaa.Sometimes(0.8, aug)

augmenters = iaa.Sequential(
    [
        iaa.SomeOf(
            (2, 4),
            [
                iaa.Add((-10, 10), per_channel=0.5),
                iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05 * 255), per_channel=0.5),
                iaa.OneOf(
                    [
                        iaa.GaussianBlur(sigma=(0, 0.5)),
                        iaa.AverageBlur(k=1),
                        iaa.MedianBlur(k=1),
                    ]
                ),
                iaa.OneOf(
                    [
                        iaa.Fliplr(1), 
                        iaa.Flipud(1), 
                    ]
                ),
                iaa.LinearContrast((0.8, 1.2), per_channel=0.5),
            ],
        ),
        sometimes(
            iaa.Affine(
                scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
                translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
                rotate=(-45, 45),
                shear=(-16, 16),
                order=[0, 1],
                cval=(0, 255),
                mode=ia.ALL,
            )
        ),
    ],
    random_order=True,
)


img_augmentation = Sequential(
    [
        preprocessing.RandomRotation(factor=0.35, seed=SEED),
        preprocessing.RandomTranslation(height_factor=0.2, width_factor=0.2, seed=SEED),
        preprocessing.RandomFlip(seed=SEED),
        preprocessing.RandomContrast(factor=0.2, seed=SEED),
    ],
    name="img_augmentation",
)


def create_augmented_dataset(
    dataset_path=DATASET_PATH, new_dataset_path=AUGMENT_DATASET_PATH, augmenters=img_augmentation, n_augment_per_file=N_AUGMENT_PER_FILE
):
    if not os.path.isdir(new_dataset_path):
        os.makedirs(new_dataset_path)
    class_names, _, _ = retrieve_class_names(dataset_path)
    for class_name in tqdm(class_names):
        train_filepaths_per_class = glob.glob(dataset_path + "train_images/{}".format(class_name) + "/*.jpg")
        if not os.path.isdir(dataset_path + "train_images/{}".format(class_name)):
            os.makedirs(dataset_path + "train_images/" + class_name + "/")
        for filepath in train_filepaths_per_class:
            # image = read_image(filepath)
            image = cv2.imread(filepath)
            new_img_path = dataset_path + "train_images/" + class_name + "/" + filepath.split("/")[-1]
            copyfile(filepath, new_img_path)
            for image_index in range(n_augment_per_file):
                # image_aug = img_augmentation(tf.expand_dims(image, axis=0))
                image_aug = augmenters(image=image)
                image_aug_path = (
                    dataset_path + "train_images/" + class_name + "/" + filepath.split("/")[-1][:-4] + "_{}".format(image_index) + ".jpg"
                )
                # save_img(image_aug_path, image_aug[0])
                cv2.imwrite(image_aug_path, image_aug)
