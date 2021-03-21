#!/usr/bin/env bash

if ! command -v axel &> /dev/null; then
  echo "axel not found, please install it before executing this script"
  exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/.."
DST="${DIR}/dataset/acfr-fruit-dataset.zip"
URL="https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/acfr-multifruit-2016.zip"

echo -n "downloading the ACFR dataset... "
axel -n 20 --insecure -o "${DST}" "${URL}" > /dev/null
echo "done!"
