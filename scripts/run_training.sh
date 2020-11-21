#!/bin/bash

echo "############### INSTALLING THE PACKAGE ###########"
pip3 install -r requirements.txt
pip3 install -e .
echo "###############          DONE          ###########"
echo "############### STARTING PREPROCESSING ###########"
python3 ./bird_image_classification_mva/scripts/preprocess_script.py
echo "###############          DONE          ###########"
echo "###############   STARTING TRAINING    ###########"
python3 ./bird_image_classification_mva/scripts/training_script.py
echo "###############          DONE          ###########"
