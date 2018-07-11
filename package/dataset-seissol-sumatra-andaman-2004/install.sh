#!/bin/bash

cd ${INSTALL_DIR}

mkdir data
cd ${INSTALL_DIR}/data

echo "Downloading seissol dataset ..."

wget https://zenodo.org/record/439946/files/1003_topo30sec_wSplays_sim5_pumgenSM2.dtc1-v2-suma.20.nc
if [ "${?}" != "0" ] ; then
  echo "Error: download failed!"
  exit 1
fi

wget https://zenodo.org/record/439946/files/1003_topo30sec_wSplays_sim5_pumgenSM2_rec.dat
if [ "${?}" != "0" ] ; then
  echo "Error: download failed!"
  exit 1
fi

wget https://zenodo.org/record/439946/files/parameters.par
if [ "${?}" != "0" ] ; then
  echo "Error: download failed!"
  exit 1
fi

exit 0
