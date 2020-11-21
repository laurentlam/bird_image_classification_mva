#!/bin/bash

echo "############### INSTALLING THE PACKAGE ###########"
pip3 install -r requirements.txt
pip3 install -e .
echo "###############          DONE          ###########"
echo "###############  STARTING PREDICTIONS   ###########"
python3 ./bird_image_classification_mva/scripts/prediction_script.py
echo "###############          DONE          ###########"
