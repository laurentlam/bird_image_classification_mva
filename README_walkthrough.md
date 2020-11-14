# **Cookie cutter repository**

This `README` walkthrough is presenting the cookie cutter repository for any Python project.
The aim is that anyone can download this cookie cutter repository to have a standardized repository before starting their project.

Of course this is only a general template aimed at being versatile and multi-purpose, nothing is set in stone.
Feel free to change anything you find irrelevant, add new folders/files, remove some modules if it better meets your needs.

**Please refer to the description of the `scripts` folder or the `Makefile` to have an overview of the different commands implemented by default in this repository.**

## How to change your repository name

We have written a script to help you modify and rename all the folders, files and content into the new repository name of your choice.
This script `rename_repo.sh` would need to be run at the root of the repository.
You will need to provide a valid repository name and it will replace every occurrences of the old repository name into the new one.
It will also prompt you to delete the `.git` folder from the `research_cookie_cutter` repository.
At the end of the script you will also be able to delete this script as it will no longer be of use.

When you are done with this process, you can copy the contents of this new repository into your new repository and use it as-is.

**You will also need to change the name and the description of the project in the following files:**

- `setup.py`
- `README.md`

However in the following, we will still keep the repository name `research_cookie_cutter` for better understanding.

## **Walkthrough of the repository**

The **repository root view** is represented below:

- `research_cookie_cutter`/
- |__ `data`/
- |__ `docker`/
- |__ `models`/
- |__ `notebooks`/
- |__ `research_cookie_cutter`/
- |__ `scripts`/
- |__ `.dockerignore`
- |__ `.flake8`
- |__ `.gitignore`
- |__ `Makefile`
- |__ `README.md`
- |__ `research_cookie_cutter.conf`
- |__ `requirements.txt`
- |__ `setup.py`
- |__ `VERSION`

### Folder: `data`
The `data` folder is where you store your different data-sets.
They are not to be pushed, which is partially prevented with the `.gitignore` file.
There is a `README.md` file where you can describe each of your data-sets.

### Folder: `docker`
The `docker` folder is where you store your `Dockerfile`.
The present Dockerfile allows you to run a notebook in a container from a Python 3.7 image.
It will install the requirements stated in the `requirements.txt` file beforehand.

### Folder: `models`
The `models` folder is where you store your different models.
They are not to be pushed, which is partially prevented with the `.gitignore` file.
There is a `README.md` file where you can describe the use of each of your models.

### Folder: `notebooks`
The `notebooks` folder is where you store your different notebooks.
They must be pushed only after clearing their cells.
There is a `README.md` file where you can describe the use of each of your notebooks.

### Folder: `scripts`
The `scripts` folder is where you store your different bash scripts.
It contains 4 scripts by default:

- `format-check.sh`: This script will start a new container mounting the repository and run the type checking, linting, code formatter and import formatter.
- `run_notebook.sh`: This script will solve the permissions problems with docker at launch and quit of the notebook.
- `run_training.sh` : This script will solve the permissions problems with docker when running your training script.
**The training script name within this bash file will need to be changed into your own training script before running**.
- `run_prediction.sh` : This script will solve the permissions problems with docker when running your prediction script.
**The prediction script name within this bash file will need to be changed into your own prediction script before running**.

### Folder: `research_cookie_cutter`
The `research_cookie_cutter` folder is where all the Python code is supposed to be.
It contains different pre-defined Python modules, each of them having a specific purpose.

- `research-cookie-cutter`/
- |__ `...`/
- |__ `research_cookie_cutter`/
  - |__ `config`/
  - |__ `data`/
  - |__ `eval`/
  - |__ `logger`/
  - |__ `models`/
  - |__ `scripts`/
  - |__ `tests`/
  - |__ `train`/
  - |__ `utils`/

#### Folder: `research_cookie_cutter`/`config`
The `config` folder contains everything linked to the configuration file such as reading and defining the different variables.
The present `config.py` file have all the default functions to read from the configuration file at the root of the repository.
You will be able to import the different variables from this module.

#### Folder: `research_cookie_cutter`/`data`
The `data` folder contains everything linked to data such as data pre-processing or data transformation.
You will be able to import the different pre-processing or transformation functions from modules here.

#### Folder: `research_cookie_cutter`/`eval`
The `eval` folder contains everything linked to a Machine Learning model evaluation such as its `def predict()` function or its `def eval()` function.
You will be able to write and evaluate all your models in here.

#### Folder: `research_cookie_cutter`/`logger`
The `logger` folder contains everything linked to the logs.
You will be able to import the logger for each file from this module.

#### Folder: `research_cookie_cutter`/`models`
The `models` folder contains everything linked to the models used.
You will be able to write and load models from here.

#### Folder: `research_cookie_cutter`/`scripts`
The `scripts` folder contains everything linked to Python scripts.
You will be able to write all your Python scripts here.

#### Folder: `research_cookie_cutter`/`tests`
The `tests` folder contains everything linked to testing such as unitary or integration tests.
You will be able to write and test all your unitary and integration test functions in here.

#### Folder: `research_cookie_cutter`/`train`
The `train` folder contains everything linked to training models.
You will be able to write all training modules here and import them from here.

#### Folder: `research_cookie_cutter`/`utils`
The `utils` folder contains everything linked to utilities functions.
You will be able to write all your utilities functions here and import them from here.

---

### File: `Makefile`
The `Makefile` helps you run various docker commands associated to the repository:

- `make build`: Build the docker image.
- `make test`: Run tests.
- `make format-check`: Check (and run) Python style formatting according to black, mypy and isort.
- `make run`: Run a notebook that can use parts of the pipeline.
- `make train`: Trains the pipeline.
*Please refer to the `run_training.sh` description above.*
- `make bash`: Will start a bash session in the docker container at the root of the project. 
- `make predict`: Runs the prediction.
*Please refer to the `run_prediction.sh` description above.*
- `make distclean`: Removes the docker image.

You can add or modify commands if you think it might suit your project better. 
The configuration parameters to run the docker image and container will be taken from the `research_cookie_cutter.conf` and the `Dockerfile`in the `docker`folder.
You can add and modify the *number of CPU cores*, the *memory limit* or the *port of the notebook* you will run in. 
**The port is to be changed before starting your project so that not all project are linked to the same port.**

---

### File: `.dockerignore`
The `.dockerignore` file allows you to exclude files and directories from the context of this root directory.
It helps increase docker build's speed and performance.
You can add any file or pattern you may find irrelevant for the build in this context.

### File: `.flake8`
The `.flake8` file allows you to configure your Python format-check rules via Flake8.
This default file aims to provide a standardized guideline to code our next Python repositories.

### File: `.gitignore`
The `.gitignore` file allows you to exclude files and directories from the context of this root directory.
You can add any file or pattern you may find irrelevant in this context.

### File: `README.md`
The `README.md` file introduces and explains the project.
This one contains by default the sections **Prerequisites**, **Configuration**, **Building the projects**, **Training the Pipeline** and **Running the Pipeline**.
You may need to fill those sections and add your own sections for anything your project would need.

### File: `research_cookie_cutter.conf`
The `research_cookie_cutter.conf` file is a configuration file used to for parameters and initial settings for the repository.
You will need to add your own parameters corresponding to your project.

### File: `requirements.txt`
The `requirements.txt` file is a text file listing all the Python packages required to be able to build and run this repository correctly.
You will need to add all packages you are using, and if necessary their versions.

### File: `setup.py`
The `setup.py` file is a Python file that describes all of the metadata of the project.
It builds and turns your repository into a Python package you can call from in your Python scripts.
You would need to change the version for each pull/merge request or release in order to have a structured versioning system.

### File: `VERSION`
The `VERSION` file is a text file containing the version of the package.
You would need to change the version for each pull/merge request or release in order to have a structured versioning system.
