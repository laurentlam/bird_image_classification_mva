from bird_image_classification_mva.config.config import (
    AUGMENT_DATASET,
    AUGMENT_DATASET_PATH,
    CROPPED_DATASET_PATH,
    DATASET_PATH,
    EFFICIENTNET_MODE,
    EXTRACT_IMAGES,
    MODEL_PATH,
    RESAMPLE_DATASET,
    RESAMPLED_DATASET_PATH,
    SEED,
    STAGE_0_EPOCHS,
    STAGE_1_EPOCHS,
    SUBMISSION_CSV_PATH,
)
from bird_image_classification_mva.data.dataset import load_dataset
from bird_image_classification_mva.logger.logging import get_logger
from bird_image_classification_mva.models.predictions import create_submission_file
from tensorflow import keras

logger = get_logger(__name__)


def main():
    dataset_path = CROPPED_DATASET_PATH if EXTRACT_IMAGES else DATASET_PATH

    dataset_test_path = RESAMPLED_DATASET_PATH if RESAMPLE_DATASET else dataset_path

    logger.info("Loading dataset at {}".format(dataset_test_path + "test_images/"))
    ds_test = load_dataset(dataset_test_path + "test_images/", shuffle=False)

    logger.info("Loading fine-tuned model at {}".format(MODEL_PATH))
    model = keras.models.load_model(MODEL_PATH)

    logger.info("Starting predictions")
    predictions = model.predict(ds_test)

    logger.info("Creating submissions csv file...")
    create_submission_file(predictions)
    logger.info("DONE.")


if __name__ == "__main__":
    main()
