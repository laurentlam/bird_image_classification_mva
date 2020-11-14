#!/bin/bash
# This script will solve the permissions problems with docker when running your training script
echo "############### INSTALLING THE PACKAGE ###########"
chown -R "$1:$1" /deploy
pip install -e .
echo "###############          DONE          ###########"
echo "###############   STARTING TRAINING    ###########"
python3 MY_TRAINING_SCRIPT
chown -R "$1:$1" /deploy
echo "###############          DONE          ###########"
