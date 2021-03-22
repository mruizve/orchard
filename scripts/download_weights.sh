#!/usr/bin/env bash

function gdrive_download () {
  URL="https://drive.google.com/uc?export=download"
  confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "${URL}&id=$1" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
  wget --load-cookies /tmp/cookies.txt "${URL}&confirm=${confirm}&id=${1}" -O "${2}"
  rm -rf /tmp/cookies.txt
}

if ! command -v wget &> /dev/null; then
  echo "axel not found, please install it before executing this script"
  exit 1
fi

declare -A targets=(
  [efficientnetb7_pathology.h5]="1cNpEwAIPB7UUjcknjCZU1IHwGmKEUnqO"
  [mask_rcnn_orchard.h5]="1TqsMTvLLeaUqymbPFzpovuqyBdlrGucx"
)

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/../weights"

for weights in ${!targets[@]}; do
  gdrive_download "${targets[$weights]}" "${DIR}/${weights}"
done
