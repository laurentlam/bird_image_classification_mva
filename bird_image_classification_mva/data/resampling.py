import glob
import os
from shutil import copyfile

from bird_image_classification_mva.config.config import (
    DATASET_PATH, RESAMPLED_DATASET_PATH, SEED, VAL_SIZE)
from bird_image_classification_mva.data.classes import retrieve_class_names
from bird_image_classification_mva.logger.logging import get_logger
from sklearn.model_selection import train_test_split
from tqdm import tqdm

logger = get_logger(__name__)


def retrieve_files(path, ext=None, sort=True):
    path_pattern = path + "*/*/*.{}".format(ext) if ext else path
    files = glob.glob(path_pattern, recursive=True)
    if sort:
        files.sort()
    logger.info("Number of files found: {}".format(len(files)))
    return files


def retrieve_dataset_splits(filepaths):
    test_filepaths, rest_filepaths = zip(
        *[(filepath, None) if filepath.split("/")[-3] == "test_images" else (None, filepath) for filepath in filepaths]
    )
    test_filepaths = [filepath for filepath in test_filepaths if filepath]
    rest_filepaths = [filepath for filepath in rest_filepaths if filepath]
    logger.info("Number of Test files: {}".format(len(test_filepaths)))
    logger.info("Number of files to resample: {}".format(len(rest_filepaths)))
    return rest_filepaths, test_filepaths


def resample_train_val_splits(filepaths_per_class):
    train_filepaths, val_filepaths = [], []
    for class_name in filepaths_per_class.keys():
        train_filepaths_class, val_filepaths_class = train_test_split(
            filepaths_per_class[class_name], test_size=VAL_SIZE, shuffle=True, random_state=SEED
        )
        train_filepaths += train_filepaths_class
        val_filepaths += val_filepaths_class
    return train_filepaths, val_filepaths


def resample_dataset(filepaths):
    rest_filepaths, test_filepaths = retrieve_dataset_splits(filepaths)
    class_names, _, _ = retrieve_class_names(DATASET_PATH)
    filepaths_by_class = {class_name: [file for file in rest_filepaths if file.split("/")[-2] == class_name] for class_name in class_names}
    train_filepaths, val_filepaths = resample_train_val_splits(filepaths_by_class)
    logger.info("Train split: {}; Val split: {}; Test split: {}".format(len(train_filepaths), len(val_filepaths), len(test_filepaths)))
    return train_filepaths, val_filepaths, test_filepaths


def copy_resampled_split(split_files, split):
    new_path = RESAMPLED_DATASET_PATH + split + "_images/"
    logger.debug("Copying new split path at: {}".format(new_path))
    class_names, _, _ = retrieve_class_names(DATASET_PATH)
    if split in ["train", "val"]:
        for class_name in tqdm(class_names):
            new_class_path = new_path + class_name + "/"
            if not os.path.isdir(new_class_path):
                os.makedirs(new_class_path)
            for file in split_files:
                if file.split("/")[-2] == class_name:
                    copyfile(file, new_class_path + file.split("/")[-1])
    elif split == "test":
        new_class_path = new_path + "mistery_category/"
        if not os.path.isdir(new_class_path):
            os.makedirs(new_class_path)
        for file in tqdm(split_files):
            copyfile(file, new_class_path + file.split("/")[-1])


def copy_resampled_dataset(train_filepaths, val_filepaths, test_filepaths):
    logger.info("Copying resampled training split...")
    copy_resampled_split(train_filepaths, "train")
    logger.info("Copying resampled validation split...")
    copy_resampled_split(val_filepaths, "val")
    logger.info("Copying resampled testing split...")
    copy_resampled_split(test_filepaths, "test")
    logger.info("Done.")


def create_resampled_dataset(dataset_folder):
    logger.info("Retrieving filepaths from dataset at: {}".format(dataset_folder))
    filepaths = retrieve_files(dataset_folder, ext="jpg", sort=True)
    logger.info("Resampling dataset with val split size: {}".format(VAL_SIZE))
    train_filepaths, val_filepaths, test_filepaths = resample_dataset(filepaths)
    logger.info("Copying resampled dataset at: {}".format(RESAMPLED_DATASET_PATH))
    copy_resampled_dataset(train_filepaths, val_filepaths, test_filepaths)
