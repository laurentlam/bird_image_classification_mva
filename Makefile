help:
	@echo "All the command expect the build to have been run first."
	@echo "build			Build the docker image."
	@echo "test			Run tests."
	@echo "format-check		Check (and run) Python style formatting according to black, mypy and isort."
	@echo "run			Run a notebook that can use parts of the pipeline."
	@echo "train			Trains the pipeline."
	@echo "bash			Will start a bash session in the docker container at the root of the project."
	@echo "predict			Runs the prediction."
	@echo "distclean		Removes the docker image."

build:
	bash scripts/run_build.sh

train:
	bash scripts/run_training.sh

extract:
	bash scripts/run_extraction.sh

predict:
	bash scripts/run_prediction.sh
