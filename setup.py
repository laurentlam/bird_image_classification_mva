#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name='bird_image_classification_mva',
    version='0.0.1',
    description='Bird image classification competition for Object Recognition and Computer Vision MVA course',
    author='Laurent Lam',
    packages=find_packages(),
    package_data={'': ['*.png']},
    install_requires=[],
)
