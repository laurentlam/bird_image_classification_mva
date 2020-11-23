#!/bin/bash

echo "############### FETCHING EXTRACTION MODEL ###########"
pip3 uninstall mrcnn
cd models && git clone https://github.com/matterport/Mask_RCNN.git
tf_upgrade_v2 --intree Mask_RCNN --inplace --reportfile Mask_RCNN/report.txt
echo "###############            DONE           ###########"
echo "###############  EXTRACTION PIPELINE   ###########"
cd Mask_RCNN && python3.8 ../../bird_image_classification_mva/scripts/extraction_script.py
echo "###############          DONE          ###########"
cd ../../