# Fast Optical Music Recognition Using the YOLO Platform

- Vojtěch Dvořák, Bachelor's thesis, MFF UK, 2025
- supervised by Mgr. Jiří Mayer

This repository contains the code for the Bachelor's Thesis on "Fast Optical Music Recognition Using the YOLO Platform."

This is a snapshot created for archiving along with the text of the thesis, a version, with possible updates, can be found online at [https://github.com/v-dvorak/bachelor-thesis](https://github.com/v-dvorak/bachelor-thesis).

It is strongly recommended that this project be run on Linux and use Python 3.11 or above.

## Structure

The project contains three Python libraries:

- [`od-tools`](od-tools/README.md)
    - library and framework designed for handling annotations used as both inputs and outputs in object detection models
    - developed in a [separate GitHub repo](https://github.com/v-dvorak/od-tools)
- [`stalix`](stalix/README.md)
    - lightweight library designed for staff line detection, primarily used for refining measure bounding boxes in optical music recognition (OMR) pipelines
    - developed in a [separate GitHub repo](https://github.com/v-dvorak/stalix)
- [`tonic`](tonic/README.md)
    - algorithm for converting raw object detections of grand staff, measures and noteheads into structured MusicXML representations
    - developed in a [separate GitHub repo](https://github.com/v-dvorak/tonic)

## Usage

This is a self-contained version - all custom libraries created for this thesis are already located in this directory and do not have to be cloned or installed separately. These scripts were tested and run on Linux.

A virtual environment for this project can be set up by running [`setup.sh`](setup.sh) or [`setup.ps1`](setup.ps1). The script automatically downloads all external dependencies and installs the above mentioned libraries into the created venv.

```bash
# on Linux
./setup.sh <path-to-python>

# on Windows
.\setup.ps1 -Python <path-to-python>
```

Each library contains its README with a description of how it should be used and run. The most important output of this thesis is the `tonic` library, how to run a demo inference and experiments is described in its [`README`](tonic/README.md).

If any other documentation tells you to "setup venv", "install requirements" etc., do not install anything, the venv is already set up from the script above and all scripts inside this directory can be run directly.

## Quality of Life Scripts

- **setup**, described above, creates a venv from which the project can be run

- **basic-tasks** is a script that checks the core functionalities of this project
    - OLiMPiC dataset and detection models are downloaded
    - single evaluation on the OLiMPiC dataset is run (special "OLiMPiC mode")
    - predictions are run on the first few examples from the OLiMPiC dataset (standard mode)
    - predictions and ground truth data are compared

- **reset-project** is a script that deletes all files that might be automatically created (by Python or our scripts) during the usage of the script
    - `__pycache__`, `.egg-info`, ...
    - downloaded `models`, `datasets`, `images`, ...
