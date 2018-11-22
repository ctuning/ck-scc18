#!/bin/bash

# Hack to fix problem on some Cray machines with libgpfs.so
if [ "${CK_LIB_GPFS}" == "" ]; then
  CK_LIB_GPFS=/usr/lib64/libgpfs.so
fi

if [ -f ${CK_LIB_GPFS} ]; then
  cp -f ${CK_LIB_GPFS} ${CK_ENV_LIB_SEISSOL_BIN}

  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${CK_ENV_LIB_SEISSOL_BIN}
fi

chmod 755 ./ck_run_slurm_generated.sh
sbatch ./ck_run_slurm_generated.sh $1
