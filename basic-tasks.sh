#!/bin/bash

cd "$(dirname "$0")"

source .venv/bin/activate
cd tonic

# downloads the OLiMPiC dataset
python3 -m tonic.SERVal.olimpic -c 1

# predicts for samples in the first chunk of OLiMPiC
# (as this is the only automatically downloaded dataset with annotations in MusicXML)
python3 -m demo -i datasets/olimpic-1.0-scanned/samples/4919798/ -o predicted

# evaluates the predictions
python3 -m tonic.SERVal predicted/ datasets/olimpic-1.0-scanned/samples/4919798/ -v