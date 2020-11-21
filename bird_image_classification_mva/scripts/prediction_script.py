from tensorflow import keras
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
from bird_image_classification_mva.models.predictions import create_submission_file


def main():
    dataset_path = CROPPED_DATASET_PATH if EXTRACT_IMAGES else DATASET_PATH

    dataset_test_path = RESAMPLED_DATASET_PATH if RESAMPLE_DATASET else dataset_path

    print("Loading dataset at {}".format(dataset_test_path + "test_images/"))
    ds_test = load_dataset(dataset_test_path + "test_images/", shuffle=False)

    print("Loading fine-tuned model at {}".format(MODEL_PATH))
    model = keras.models.load_model(MODEL_PATH)

    print("Starting predictions")
    predictions = model.predict(ds_test)

    print("Creating submissions csv file...")
    create_submission_file(predictions)
    print("DONE.")


if __name__ == "__main__":
    main()
