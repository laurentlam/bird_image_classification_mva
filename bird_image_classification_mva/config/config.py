#!/bin/python3.7
"""
This file contains all the configuration needed to run the pipeline.
They are read from the file bird_image_classification_mva.conf at the root of the project.
"""

import pathlib

from environs import Env

THIS_FOLER = str(pathlib.Path(__file__).parent.absolute())
ROOT_FOLDER = THIS_FOLER.split("bird_image_classification_mva")[0]

env = Env()
env.read_env(ROOT_FOLDER + "bird_image_classification_mva.conf", recurse=True)

# SETUP
WORKERS = env.int('workers')
LOG_LEVEL = env.str('log_level')

# PYTHON
SEED = env.int('seed')

# MODEL TRAINING PARAMETERS
DO_TRAIN = env.bool('do_train')
DO_EVAL = env.bool('do_eval')
DO_PREDICT = env.bool('do_predict')

# IMAGES
WIDTH = env.int('width')
HEIGHT = env.int('height')

# PATHS
DATASET_PATH = env.str('dataset_path')
AUGMENT_DATASET_PATH = env.str('augment_dataset_path')
RESAMPLED_DATASET_PATH = env.str('resampled_dataset_path')
MODEL_PATH = env.str('model_path')
SUBMISSION_CSV_PATH = env.str('submission_csv_path')

# DATA AUGMENTATION
AUGMENT_DATASET = env.bool('augment_dataset')
N_AUGMENT_PER_FILE = env.int('n_augment_per_file')

# TRAINING
BATCH_SIZE = env.int('batch_size')
VAL_SIZE = env.float('val_size')
EFFICIENTNET_MODE = env.str('efficientnet_mode')

STAGE_0_EPOCHS = env.int('stage_0_epochs')
STAGE_1_EPOCHS = env.int('stage_1_epochs')
STAGE_2_EPOCHS = env.int('stage_2_epochs')