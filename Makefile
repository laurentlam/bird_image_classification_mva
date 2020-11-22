help:
	@echo "All the command expect the build to have been run first."
	@echo "build			Build the repository with its dependancies."
	@echo "extract			Extracts the Regions of Interest from the dataset."
	@echo "train			Trains the pipeline."
	@echo "predict			Runs the prediction."

build:
	bash scripts/run_build.sh

extract:
	bash scripts/run_extraction.sh

train:
	bash scripts/run_training.sh

predict:
	bash scripts/run_prediction.sh
