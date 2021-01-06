#!/usr/bin/env bash

if ! command -v axel &> /dev/null; then
  echo "axel not found, please install it before executing this script"
  exit 1
fi

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
DST="${DIR}/acfr-multifruit-2016.zip"
URL="https://data.acfr.usyd.edu.au/ag/treecrops/2016-multifruit/acfr-multifruit-2016.zip"
axel -n 250 --insecure -o "${DST}"  "${URL}"

unzip -d /tmp ${DST} >/dev/null || exit 1
mv /tmp/acfr-fruit-dataset ~/dataset || exit 1
