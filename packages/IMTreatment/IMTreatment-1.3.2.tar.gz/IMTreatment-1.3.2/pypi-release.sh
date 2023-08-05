#!/bin/bash

sudo python3 -m pip install --upgrade setuptools wheel twine bumpversion
bumpversion minor
sudo rm -rf dist
sudo python3 setup.py sdist bdist_wheel
twine upload dist/*
git push
git push --tags
