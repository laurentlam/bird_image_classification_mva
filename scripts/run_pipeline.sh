echo "############### INSTALLING THE PACKAGE ###########"
pip install -r requirements.txt
pip install -e .
echo "###############          DONE          ###########"
echo "###############  STARTING PIPELINE   ###########"
python3 ./bird_image_classification_mva/scripts/pipeline_script.py
echo "###############          DONE          ###########"
