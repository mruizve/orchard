#!/usr/bin/env bash

declare -A datasets=(
 [orchard]="acfr-fruit-dataset.zip"
 [pathology]="plant-pathology-2020-fgvc7.zip"
)

mkdir -p ~/datasets

for ds in ${!datasets[@]}; do
  ZIP="/tmp/${datasets[$ds]}"
  SRC="/tmp/${datasets[$ds]%.*}"
  DST=~/datasets/"${ds}"

  echo -n "Extracting /tmp/${datasets[$ds]}... "
  unzip -d "${SRC}" "${ZIP}" >/dev/null || exit 1
  items=$(find "${SRC}"/* -maxdepth 0|wc -l)
  if [ "${items}" -eq "1" ]; then
    mv "${SRC}/${datasets[$ds]%.*}" "${DST}" || exit 1
  else
    mv "${SRC}" "${DST}" || exit 1
  fi
  echo "done!"
done
