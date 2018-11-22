#!/bin/bash

# Check parameters of a mesh (to calculate rankings)

echo ""
echo "Detecting mesh parameters (MPI rank should be multiple of 'partitions')"
echo "================================================="

${CK_ENV_LIB_NETCDF_BIN}/ncdump -h ${CK_SEISSOL_MESH_FILE_NC}

# Continue execution with a job manager if any ...
echo "================================================="

RUN_TYPE=$1
SCRIPT="ck_run_${RUN_TYPE}.sh"

ORIG_SCRIPT=${SCRIPT}

if [ "${JOB_MANAGER}" != "" ] ; then 
  SCRIPT="ck_run_${JOB_MANAGER}.sh"
fi

echo "Executing ../${SCRIPT} ..."
echo ""

../${SCRIPT} ${ORIG_SCRIPT}
