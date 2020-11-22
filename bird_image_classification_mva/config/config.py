#!/bin/python3.7
"""
This file contains all the configuration needed to run the pipeline.
They are read from the file bird_image_classification_mva.conf at the root of the project.
"""

import pathlib

from environs import Env

THIS_FOLER = str(pathlib.Path(__file__).parent.absolute())
ROOT_FOLDER = THIS_FOLER.split("bird_image_classification_mva")[0]

THIS_FOLDER = ROOT_FOLDER + "bird_image_classification_mva/"
env = Env()
env.read_env(THIS_FOLDER + "bird_image_classification_mva.conf", recurse=True)

# SETUP
LOG_LEVEL = env.str("log_level")

# PYTHON
SEED = env.int("seed")

# IMAGES
WIDTH = env.int("width")
HEIGHT = env.int("height")

# PATHS
DATASET_PATH = THIS_FOLDER + env.str("dataset_path")
RESAMPLED_DATASET_PATH = THIS_FOLDER + env.str("resampled_dataset_path")
AUGMENT_DATASET_PATH = THIS_FOLDER + env.str("augment_dataset_path")
CROPPED_DATASET_PATH = THIS_FOLDER + env.str("cropped_dataset_path")
MODEL_PATH = THIS_FOLDER + env.str("model_path")
SUBMISSION_CSV_PATH = THIS_FOLDER + env.str("submission_csv_path")

# DATA AUGMENTATION
AUGMENT_DATASET = env.bool("augment_dataset")
N_AUGMENT_PER_FILE = env.int("n_augment_per_file")

# RESAMPLE DATASET
RESAMPLE_DATASET = env.bool("resample_dataset")

# EXTRACT IMAGES
EXTRACT_IMAGES = env.bool("extract_images")

# TRAINING
BATCH_SIZE = env.int("batch_size")
VAL_SIZE = env.float("val_size")
EFFICIENTNET_MODE = env.str("efficientnet_mode")

STAGE_0_EPOCHS = env.int("stage_0_epochs")
STAGE_1_EPOCHS = env.int("stage_1_epochs")
