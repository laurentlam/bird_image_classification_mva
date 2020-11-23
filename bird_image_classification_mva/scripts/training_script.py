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
from bird_image_classification_mva.data.classes import retrieve_class_names
from bird_image_classification_mva.data.dataset import load_dataset
from bird_image_classification_mva.logger.logging import get_logger
from bird_image_classification_mva.models.efficientnet import build_model, unfreeze_model

logger = get_logger(__name__)


def main():
    dataset_path = CROPPED_DATASET_PATH if EXTRACT_IMAGES else DATASET_PATH
    _, num_classes, _ = retrieve_class_names(dataset_path)

    dataset_train_path = AUGMENT_DATASET_PATH if AUGMENT_DATASET else dataset_path
    dataset_val_path = RESAMPLED_DATASET_PATH if RESAMPLE_DATASET else dataset_path

    logger.info("Loading dataset")
    ds_train = load_dataset(dataset_train_path + "train_images/")
    ds_val = load_dataset(dataset_val_path + "val_images/")

    logger.info("Building EfficientNet model with {} architecture".format(EFFICIENTNET_MODE))
    model = build_model(num_classes=num_classes, model=EFFICIENTNET_MODE)
    _ = model.fit(ds_train, epochs=STAGE_0_EPOCHS, validation_data=ds_val, verbose=2)
    logger.info("Unfreezing top layers...")
    unfreeze_model(model)
    _ = model.fit(ds_train, epochs=STAGE_1_EPOCHS, validation_data=ds_val, verbose=2)
    logger.info("Training complete.")
    logger.info("Saving model at {}".format(MODEL_PATH))
    model.save(MODEL_PATH)


if __name__ == "__main__":
    main()
