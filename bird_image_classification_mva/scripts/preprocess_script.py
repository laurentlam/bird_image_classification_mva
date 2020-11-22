from bird_image_classification_mva.data.resampling import create_resampled_dataset
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
from bird_image_classification_mva.data.augmentation import create_augmented_dataset
from bird_image_classification_mva.data.classes import retrieve_class_names


def main():
    dataset_path = CROPPED_DATASET_PATH if EXTRACT_IMAGES else DATASET_PATH
    class_names, _, _ = retrieve_class_names(dataset_path)
    if RESAMPLE_DATASET:
        create_resampled_dataset(dataset_path)
    if AUGMENT_DATASET:
        create_augmented_dataset(class_names, dataset_path=RESAMPLED_DATASET_PATH if RESAMPLED_DATASET_PATH else dataset_path)


if __name__ == "__main__":
    main()