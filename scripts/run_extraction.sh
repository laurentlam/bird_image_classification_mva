#!/bin/bash

echo "############### FETCHING EXTRACTION MODEL ###########"
cd models
pip3 uninstall mrcnn
git clone https://github.com/matterport/Mask_RCNN.git
tf_upgrade_v2 --intree Mask_RCNN --inplace --reportfile Mask_RCNN/report.txt
echo "###############            DONE           ###########"
cd Mask_RCNN
echo "###############  EXTRACTION PIPELINE   ###########"
python3 ../../bird_image_classification_mva/scripts/extraction_script.py
echo "###############          DONE          ###########"
cd ../../