#!/usr/bin/env bash

(
  set -x

  DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
  Mask_RCNN="${DIR}/../Mask_RCNN"
  weights="${DIR}/../weights"
  samples="${DIR}/../samples"

  # Update pip
  sudo -H pip3 install -U pip

  # Install customized Mask_RCNN package (including all dependencies)
  cd "${Mask_RCNN}"
  sudo -H pip3 install -r requirements.txt

  # Install orchard dependencies
  sudo -H pip3 install pycocotools efficientnet sklearn
  sudo -H pip3 install .

  # Apply Keras patches (TO DO: shall these patches be part of this repository instead of the Mask_RCNN one?)
  sudo patches/apply.sh

  # Install orchard package
  cd "${DIR}/.."
  sudo -H pip3 install .

  # Copy pre-trained model's weights
  mv "${weights}" ~/

  # Copy sample notebooks
  mv "${samples}" ~/
)
