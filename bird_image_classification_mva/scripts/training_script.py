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
from bird_image_classification_mva.data.dataset import load_dataset
from bird_image_classification_mva.models.efficientnet import build_model, unfreeze_model
from bird_image_classification_mva.data.classes import retrieve_class_names


def main():
    dataset_path = CROPPED_DATASET_PATH if EXTRACT_IMAGES else DATASET_PATH
    _, num_classes, _ = retrieve_class_names(dataset_path)

    dataset_train_path = AUGMENT_DATASET_PATH if AUGMENT_DATASET else dataset_path
    dataset_val_path = RESAMPLED_DATASET_PATH if RESAMPLE_DATASET else dataset_path

    print("Loading dataset")
    ds_train = load_dataset(dataset_train_path + "train_images/")
    ds_val = load_dataset(dataset_val_path + "val_images/")

    print("Building EfficientNet model with {} architecture".format(EFFICIENTNET_MODE))
    model = build_model(num_classes=num_classes, model=EFFICIENTNET_MODE)
    _ = model.fit(ds_train, epochs=STAGE_0_EPOCHS, validation_data=ds_val, verbose=2)
    print("Unfreezing top layers...")
    unfreeze_model(model)
    _ = model.fit(ds_train, epochs=STAGE_1_EPOCHS, validation_data=ds_val, verbose=2)
    print("Training complete.")
    print("Saving model at {}".format(MODEL_PATH))
    model.save(MODEL_PATH)


if __name__ == "__main__":
    main()