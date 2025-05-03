Set-Location -Path $PSScriptRoot

& .\.venv\Scripts\Activate.ps1
Set-Location -Path "tonic"

# downloads the OLiMPiC dataset
python -m tonic.SERVal.olimpic -c 1

# predicts for samples in the first chunk of OLiMPiC
# (as this is the only automatically downloaded dataset with annotations in MusicXML)
python -m demo -i datasets/olimpic-1.0-scanned/samples/4919798/ -o predicted

# evaluates the predictions
python -m tonic.SERVal predicted/ datasets/olimpic-1.0-scanned/samples/4919798/ -v
