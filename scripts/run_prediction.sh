#!/bin/bash
# This script will solve the permissions problems with docker when running your prediction script
echo "############### INSTALLING THE PACKAGE ###########"
chown -R "$1:$1" /deploy
pip install -e .
echo "###############          DONE          ###########"
echo "###############  STARTING PREDICTION   ###########"
python3 MY_PREDICTION_SCRIPT
chown -R "$1:$1" /deploy
echo "###############          DONE          ###########"
