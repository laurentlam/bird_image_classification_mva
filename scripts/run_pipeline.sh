echo "############### INSTALLING THE PACKAGE ###########"
pip3 install -r requirements.txt
pip3 install -e .
echo "###############          DONE          ###########"
echo "############### FETCHING DATASET ###########"
wget https://www.di.ens.fr/willow/teaching/recvis18orig/assignment3/bird_dataset.zip -P ./data
unzip -q bird_dataset.zip -d ./data/
rm ./data/bird_dataset.zip
echo "###############          DONE          ###########"
echo "###############  STARTING PIPELINE   ###########"
python3 ./bird_image_classification_mva/scripts/pipeline_script.py
echo "###############          DONE          ###########"
