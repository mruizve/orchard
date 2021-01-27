#!/usr/bin/env bash

if ! command -v axel &> /dev/null; then
  echo "axel not found, please install it before executing this script"
  exit 1
fi

DST="/tmp/acfr-multifruit-2016.zip"
URL="https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/acfr-multifruit-2016.zip"

echo -e "downloading the ACFR dataset... "
axel -n 20 --insecure -o "${DST}" "${URL}" > /dev/null
echo "done"

unzip -d /tmp "${DST}" >/dev/null || exit 1
mv /tmp/acfr-fruit-dataset ~/dataset || exit 1
