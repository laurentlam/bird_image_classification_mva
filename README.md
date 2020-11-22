# Bird Image Classification Kaggle Competition

This repository contains all the code for the Bird Image Classification Kaggle Competition for the Object Recognition and Computer Vision MVA course.

## Getting Started
This project consists in producing a model that manages to classify accurately 20 categories of birds using a subset of the [Caltech-UCSD Birds-200-2011 bird dataset](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html). 

The goal of this [Kaggle competition](https://www.kaggle.com/c/mva-recvis-2020) is to provide the model with the highest possible acccuracy on a test dataset containing the same categories.

### Prerequisites
The only dependencies in order to run this project are:

*  [Python 3](https://www.python.org/) for handling the project code.
*  [make](https://www.gnu.org/software/make/) to run the project.

### Configuration
Be aware that there will be **no inline arguments** when running this project since all arguments and configuration variables are contained within the `bird_image_classification_mva.conf` file.

Therefore, **please check and modify directly that configuration file** if you want to try out new settings parameters for image pre-processing, training or paths management.

### Building the project
Make sure that your default Python 3 packages install and run command is made via `python3` and `pip3`. Otherwise, please modify the different Python commands accordingly within the bash scripts in `./scripts/run_*.sh`.

Then simply run:

```bash
make build
```

### Pre-processing the images
The provided image dataset is pre-processed through different steps:

An optional step is used before-hand for optimal results and is implemented within a script of its own via

```bash
make extract
```

- Extracting the Region of Interest (here the bird) from each image, using an Object Detector [Mask-RCNN](https://arxiv.org/abs/1703.06870) model from this [repository](https://github.com/matterport/Mask_RCNN). It is pre-trained on the [MS COCO dataset](https://cocodataset.org/). The detected bounding box will then be cropped and used as the new image.

*If you have issues running the script, please go to the `Troubleshooting` section.*

This step can be desactivated within the configuration file as well as the next pre-processing steps.


The next steps of pre-processing are contained:

- Resampling the provided training and validation sets *(the validation ratio size is fixed within the configuration file)*
- Augmenting the training set via Data Augmentation applying various image transformations with the [imgaug](https://imgaug.readthedocs.io/) package *(the number of generated images per original image is fixed within the configuration file)*

### Training the Pipeline
The image classification task is done with an [EfficientNet](https://arxiv.org/abs/1905.11946) model, pre-trained on [ImageNet](http://www.image-net.org/). The supported architectures are from **B0 to B7**.
After setting up the configuration file with the parameters you want, simply run:

```bash
make train
```

### Predicting with the Pipeline
In order to use the trained pipeline to predict on the testing set and generate a `submissions.csv` for the Kaggle competition, simply run:

```bash
make predict
```

### Going further
If you want to go deeper in the understanding of the different steps of the pipeline, feel free to take a look at the `bird_image_classification_mva_report.pdf` report PDF file, describing all steps with references and providing results and metrics of the project.

### Troubleshooting
If you have issues running the `make extract` command script, it might be due to compatibility reasons since the cloned Mask-RCNN repository was based on Tensorflow *1.x <= 1.9*. That would be incompatible with the rest of the scripts. 

Therefore we propose an alternative script contained within a jupyter notebook that would solve this issue. The notebook is located at `./notebooks/MaskRCNN_extraction.ipynb` and can be executed with Colab for example.

However, be aware that infering the detections on all the 1702 images of the dataset using Mask-RCNN might take a long time, many hours might be required.
