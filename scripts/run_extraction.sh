#!/bin/bash

echo "############### FETCHING EXTRACTION MODEL ###########"
cd models
git clone https://github.com/matterport/Mask_RCNN.git
echo "###############            DONE           ###########"
cd Mask_RCNN
echo "###############  EXTRACTION PIPELINE   ###########"
python3 ../../bird_image_classification_mva/scripts/extraction_script.py
echo "###############          DONE          ###########"
cd ../../