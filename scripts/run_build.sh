#!/bin/bash

echo "############### INSTALLING THE PACKAGE ###########"
pip3 install -r requirements.txt
pip3 install -e .
echo "###############          DONE          ###########"
echo "###############    FETCHING DATASET    ###########"
wget https://www.di.ens.fr/willow/teaching/recvis18orig/assignment3/bird_dataset.zip -P ./data
unzip -q ./data/bird_dataset.zip -d ./data/
rm ./data/bird_dataset.zip
echo "###############          DONE          ###########"