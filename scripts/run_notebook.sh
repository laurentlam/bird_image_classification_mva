#!/bin/bash
# this script will solve the permissions problems with docker at launch and quit of the notebook
chown -R "$1:$1" /deploy
pip install -e .
jupyter notebook --NotebookApp.token='' --NotebookApp.password='' --ip 0.0.0.0 --port 8700 --no-browser --allow-root .
chown -R "$1:$1" /deploy
