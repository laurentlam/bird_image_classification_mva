# gathers information about the user to solve
# docker permission issues
USER = $(shell whoami)
USER_ID = $(shell id -u)
GROUP_ID = $(shell id -g)

# number of CPUs to use
CPU_NUMBER = $(shell perl -wln -e "/^cpu_number = \K.*/ and print $$&;"  bird_image_classification_mva.conf)
# memory usage limit
MEMORY_LIMIT = $(shell perl -wln -e "/^memory_limit = \K.*/ and print $$&;" bird_image_classification_mva.conf)
# port to use for notebooks
PORT = $(shell perl -wln -e "/^port = \K.*/ and print $$&;" bird_image_classification_mva.conf)

DOCKER_IMAGE_NAME = bird_image_classification_mva-$(USER):latest

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
	docker build --cache-from $(DOCKER_IMAGE_NAME) -f docker/Dockerfile -t $(DOCKER_IMAGE_NAME) .

format-check:
	bash scripts/format-check.sh $(jenkins)

run:
	docker run --cpus=$(CPU_NUMBER) -e ID=$(USER_ID) --memory=$(MEMORY_LIMIT) --rm -it -v $(PWD):/deploy -p $(PORT):8700 --name bird_image_classification_mva-container-deploy-$(USER) $(DOCKER_IMAGE_NAME)

test:
	docker run --cpus=$(CPU_NUMBER) -e ID=$(USER_ID) --memory=$(MEMORY_LIMIT) --rm -it -v $(PWD):/deploy --name bird_image_classification_mva-container-test-$(USER) $(DOCKER_IMAGE_NAME) pytest -vv .

train:
	docker run --cpus=$(CPU_NUMBER) -e ID=$(USER_ID) --memory=$(MEMORY_LIMIT) --rm -it -v $(PWD):/deploy --name bird_image_classification_mva-container-training_ner-$(USER) $(DOCKER_IMAGE_NAME) /deploy/scripts/run_training.sh $(USER_ID)

bash:
	docker run --cpus=$(CPU_NUMBER) -e ID=$(USER_ID) --memory=$(MEMORY_LIMIT) --rm -it -v $(PWD):/deploy -p $(PORT):8700 --name bird_image_classification_mva-container-bash-$(USER) $(DOCKER_IMAGE_NAME) bash

predict:
	docker run --cpus=$(CPU_NUMBER) -e ID=$(USER_ID) --memory=$(MEMORY_LIMIT) --rm -it -v $(PWD):/deploy --name bird_image_classification_mva-container-predict_ner-$(USER) $(DOCKER_IMAGE_NAME) /deploy/scripts/run_prediction.sh $(USER_ID)

distclean:
	docker rmi $(DOCKER_IMAGE_NAME)
