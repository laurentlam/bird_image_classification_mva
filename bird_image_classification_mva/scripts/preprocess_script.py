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
from bird_image_classification_mva.data.augmentation import create_augmented_dataset
from bird_image_classification_mva.data.classes import retrieve_class_names
from bird_image_classification_mva.data.resampling import create_resampled_dataset
from bird_image_classification_mva.logger.logging import get_logger

logger = get_logger(__name__)


def main():
    dataset_path = CROPPED_DATASET_PATH if EXTRACT_IMAGES else DATASET_PATH
    class_names, _, _ = retrieve_class_names(dataset_path)
    if RESAMPLE_DATASET:
        logger.info("Resampling dataset...")
        create_resampled_dataset(dataset_path)
    if AUGMENT_DATASET:
        logger.info("Augmenting train dataset...")
        create_augmented_dataset(class_names, dataset_path=RESAMPLED_DATASET_PATH if RESAMPLED_DATASET_PATH else dataset_path)


if __name__ == "__main__":
    main()
