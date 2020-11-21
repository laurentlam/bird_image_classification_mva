import numpy as np
import glob
import os

from bird_image_classification_mva.config.config import (
    DATASET_PATH,
    AUGMENT_DATASET_PATH,
    AUGMENT_DATASET,
    EFFICIENTNET_MODE,
    STAGE_0_EPOCHS,
    STAGE_1_EPOCHS,
    MODEL_PATH,
    SUBMISSION_CSV_PATH,
    SEED,
    RESAMPLE_DATASET,
    RESAMPLED_DATASET_PATH,
    CROPPED_DATASET_PATH,
    EXTRACT_IMAGES,
)


def decode_predictions(predictions):
    return np.argmax(predictions, axis=1)


def get_test_ids(path):
    ids = []
    filepaths = glob.glob(path + "/*.jpg")
    filepaths.sort()
    ids = [filepath.split("/")[-1][:-4] for filepath in filepaths]
    return ids, filepaths


def create_submission_file(predictions):
    class_predictions = decode_predictions(predictions)

    ids, _ = get_test_ids(DATASET_PATH + "test_images/mistery_category")

    if not os.path.isdir(SUBMISSION_CSV_PATH):
        os.makedirs(SUBMISSION_CSV_PATH)
    with open(
        "{}submission_{}_{}_{}_{}.csv".format(SUBMISSION_CSV_PATH, EFFICIENTNET_MODE, STAGE_0_EPOCHS, STAGE_1_EPOCHS, SEED), "w"
    ) as output:
        output.write("Id,Category\n")
        for id, pred in zip(ids, class_predictions):
            output.write("%s,%d\n" % (id, pred))
