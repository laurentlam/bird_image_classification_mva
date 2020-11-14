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
)
from bird_image_classification_mva.data.augmentation import create_augmented_dataset
from bird_image_classification_mva.data.dataset import load_dataset
from bird_image_classification_mva.models.models import build_model, unfreeze_model
from bird_image_classification_mva.data.classes import retrieve_class_names
from bird_image_classification_mva.models.predictions import decode_predictions
from bird_image_classification_mva.data.submission import get_test_ids

def main():
    create_resampled_dataset(DATASET_PATH)
    if AUGMENT_DATASET:
        create_augmented_dataset()
    dataset_path = AUGMENT_DATASET_PATH if AUGMENT_DATASET else DATASET_PATH

    ds_train = load_dataset(dataset_path + "train_images/")
    ds_val = load_dataset(dataset_path + "val_images/")
    ds_test = load_dataset(dataset_path + "test_images/", shuffle=False)

    num_classes = len(ds_train.class_names)

    model = build_model(num_classes=num_classes, model=EFFICIENTNET_MODE)
    _ = model.fit(ds_train, epochs=STAGE_0_EPOCHS, validation_data=ds_val, verbose=2)

    unfreeze_model(model)
    _ = model.fit(ds_train, epochs=STAGE_1_EPOCHS, validation_data=ds_val, verbose=2)

    model.save(MODEL_PATH)

    predictions = model.predict(ds_test)

    class_predictions = decode_predictions(predictions)

    ids, _ = get_test_ids(DATASET_PATH + "test_images/mistery_category")

    with open(
        "{}submission_{}_{}_{}_{}.csv".format(SUBMISSION_CSV_PATH, EFFICIENTNET_MODE, STAGE_0_EPOCHS, STAGE_1_EPOCHS, SEED), "w"
    ) as output:
        output.write("Id,Category\n")
        for id, pred in zip(ids, class_predictions):
            output.write("%s,%d\n" % (id, pred))
    print("DONE.")


if __name__ == "__main__":
    main()