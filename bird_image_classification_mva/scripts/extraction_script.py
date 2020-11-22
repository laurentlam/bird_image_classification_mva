import tensorflow.compat.v1 as tensorflow
import keras
import cython
import skimage

import os
import sys
import random
import skimage.io
from pycocotools.coco import COCO
from tqdm import tqdm
import glob
from keras.engine import saving
import warnings

tensorflow.disable_v2_behavior()
ROOT_DIR = os.path.abspath('./')
warnings.filterwarnings("ignore")
#Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
#Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
import coco


# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join('', "mask_rcnn_coco.h5")

# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on

IMAGE_DIR = os.path.join(ROOT_DIR, "..", "..", "data", "bird_dataset")
RESULT_IMAGE_DIR = os.path.join(ROOT_DIR, "..", "..", "data", "cropped_bird_dataset")
if not os.path.isdir(RESULT_IMAGE_DIR):
    os.makedirs(RESULT_IMAGE_DIR)

BATCH_SIZE = 1
class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = BATCH_SIZE


CLASS_NAMES = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

BIRD_CLASS_INDEX = CLASS_NAMES.index('bird')

def roi_area(rois):
  return (rois[2]-rois[0])*(rois[3]-rois[1])


def make_extraction_directories(extract_dataset_path, filepaths):
    folder_paths = {'/'.join(filepath.split('/')[:-1]) for filepath in filepaths}
    for folder_path in folder_paths:
        new_path_split_folder = os.path.join(extract_dataset_path, folder_path.split('/')[-2])
        if not os.path.isdir(new_path_split_folder):
            os.makedirs(new_path_split_folder)
        new_path_class_folder = os.path.join(new_path_split_folder, folder_path.split('/')[-1])
        if not os.path.isdir(new_path_class_folder):
            os.makedirs(new_path_class_folder)

def extract_images_from_batch(model, batch_filepaths, extract_dataset_path, failed_files):
    images = [skimage.io.imread(file) for file in batch_filepaths]
    try:
        results = model.detect(images)
    except:
        failed_files += batch_filepaths
    else:
        for image_index, result_image in enumerate(results):
            bird_results = [(result_image['rois'][ind], result_image['scores'][ind]) for ind, r in enumerate(result_image['class_ids']) if r == BIRD_CLASS_INDEX]
            if not bird_results:
                failed_files.append(batch_filepaths[image_index])
            else:
                rois = max(bird_results, key=lambda x: roi_area(x[0]))
            if rois:
                x1, y1, x2, y2 = rois[0]
                cropped_image = images[image_index][x1:x2, y1:y2,:]
                cropped_image_path = os.path.join(extract_dataset_path, *(batch_filepaths[image_index].split('/')[-3:]))
                skimage.io.imsave(cropped_image_path, cropped_image)
    return failed_files



def main():
    # Find image paths to process
    filepaths_to_process = glob.glob(IMAGE_DIR + "/*/*/*.jpg")
    filepaths_to_process.sort()
    print("Number of images to process: {}".format(len(filepaths_to_process)))
    # Prepare new directories for the extracted images
    make_extraction_directories(RESULT_IMAGE_DIR, filepaths_to_process)
    print("Create new directories at: {}".format(RESULT_IMAGE_DIR))
    # Prepare batches of images
    batches = [filepaths_to_process[i:i + BATCH_SIZE] for i in range(0, len(filepaths_to_process), BATCH_SIZE)]
    # Load pre-trained model
    print("Load Mask-RCNN model")
    config = InferenceConfig()
    model = modellib.MaskRCNN(mode="inference", config=config, model_dir=ROOT_DIR)
    print("Load pre-trained MS COCO weigths")
    model.load_weights(COCO_MODEL_PATH, by_name=True)
    failed_files = []
    print("Starting extraction on {} batches...".format(len(batches)))
    for batch in tqdm(batches):
        failed_files = extract_images_from_batch(model, batch, RESULT_IMAGE_DIR, failed_files)
    print("Number of failed extracted images: {}".format(len(failed_files)))
    
    
if __name__ == "__main__":
    main()