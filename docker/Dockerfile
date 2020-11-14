# original image to use
FROM python:3.7

# python package setup
COPY setup.py /deploy/
COPY requirements.txt /deploy/

WORKDIR /deploy

# install the requirements and download stopwords list and the python package
RUN pip install -r requirements.txt && pip install -e .

# default behavior of the docker image when not running a command (runs a notebook)
CMD /deploy/scripts/run_notebook.sh ${ID}
