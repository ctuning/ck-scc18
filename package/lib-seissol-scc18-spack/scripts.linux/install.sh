#! /bin/bash

#
# Extra installation script
#
# See CK LICENSE.txt for licensing details.
# See CK COPYRIGHT.txt for copyright details.
#
# Developer(s):
# - Grigori Fursin, grigori.fursin@cTuning.org, 2018
#

cd ${INSTALL_DIR}/src/

git submodule update

PREFIX=${INSTALL_DIR}/install
mkdir -p $PREFIX

######################################################################################
# Obtaining spack
echo "****************************************************************"
echo "Obtaining spack ..."
echo ""

cd ${INSTALL_DIR}
git clone https://github.com/spack/spack spack-bin

SPACK_DIR=${INSTALL_DIR}/spack-bin
SPACK_INSTALL=${INSTALL_DIR}/spack

. spack-bin/share/spack/setup-env.sh

# Add path to Spack
export PATH=${SPACK_DIR}/bin:$PATH

# Prepare config.yaml
echo ""
echo "Preparing config.yaml ..."
mkdir -p ${SPACK_DIR}/etc/spack
echo "config:" > ${SPACK_DIR}/etc/spack/config.yaml
echo "  install_tree: ${SPACK_INSTALL}" >> ${SPACK_DIR}/etc/spack/config.yaml
echo "" >> ${SPACK_DIR}/etc/spack/config.yaml
echo "  install_path_scheme: '\${PACKAGE}'" >> ${SPACK_DIR}/etc/spack/config.yaml
echo "" >> ${SPACK_DIR}/etc/spack/config.yaml
echo "  build_jobs: ${CK_HOST_CPU_NUMBER_OF_PROCESSORS}" >> ${SPACK_DIR}/etc/spack/config.yaml


## Prepare config.yaml
#SPACK_COMPILERS=$HOME/.spack/linux/compilers.yaml
#echo ""
#echo "Preparing compilers.yaml ..."

# Compilers
echo "spack compiler find"
spack compiler find


echo "spack install python@2.7.15 scons@3.0.1 ^python@2.7.15"
spack install python@2.7.15 scons@3.0.1 ^python@2.7.15

if [ "${?}" != "0" ] ; then
    echo "Error: spack installation failed!"
    exit 1
fi

echo "spack install openmpi@3.1.3 %gcc"
spack install openmpi@3.1.3 %gcc

if [ "${?}" != "0" ] ; then
    echo "Error: spack installation failed!"
    exit 1
fi

echo "spack install libxsmm@1.8.2 %gcc"
spack install libxsmm@1.8.2 %gcc

if [ "${?}" != "0" ] ; then
    echo "Error: spack installation failed!"
    exit 1
fi

echo "spack install netcdf@4.4.1 %gcc +mpi -shared ^openmpi@3.1.3 ^hdf5@1.10.4 +mpi +fortran -shared"
spack install netcdf@4.4.1 %gcc +mpi -shared ^openmpi@3.1.3 ^hdf5@1.10.4 +mpi +fortran -shared

if [ "${?}" != "0" ] ; then
    echo "Error: spack installation failed!"
    exit 1
fi

# Add python, scons and openmpi to Path
export PATH=${SPACK_INSTALL}/python/bin:${SPACK_INSTALL}/scons/bin:$PATH
export PATH=${SPACK_INSTALL}/openmpi/bin:$PATH

# Back to src
cd ${INSTALL_DIR}/src/

######################################################################################
echo "Downloading and installing Python deps ..."
echo ""

EXTRA_PYTHON_SITE=${INSTALL_DIR}/python-lib
rm -rf ${EXTRA_PYTHON_SITE}
mkdir -p ${EXTRA_PYTHON_SITE}

python2 -m pip install --ignore-installed lxml scipy -t ${EXTRA_PYTHON_SITE}  ${SYS}
if [ "${?}" != "0" ] ; then
  echo "Error: installation failed!"
  exit 1
fi

export PYTHONPATH=${EXTRA_PYTHON_SITE}:$PYTHONPATH

######################################################################################
echo "Continue installation ..."
echo ""

COMPILER_TYPE="gcc"
if [ "${CK_CC}" == "icc" ] ; then
   COMPILER_TYPE="intel"
fi

#FIX ME USE CK VARIABLES
# i.e.,  arch: .  Valid values are: ['snoarch', 'dnoarch', 'swsm', 'dwsm', 'ssnb', 'dsnb', 'sknc', 'dknc', 'shsw', 'dhsw', 'sknl', 'dknl'
# dsnb = sandy bridge
scons -j ${CK_HOST_CPU_NUMBER_OF_PROCESSORS}  \
       logLevel=${CK_SEISSOL_LOG_LEVEL} \
       logLevel0=${CK_SEISSOL_LOG_LEVEL0} \
       order=${CK_SEISSOL_ORDER} \
       compileMode=${CK_SEISSOL_COMPILE_MODE} \
       generatedKernels=${CK_SEISSOL_GENERATED_KERNELS} \
       arch=${CK_SEISSOL_TARGET_ARCH} \
       parallelization=${CK_SEISSOL_PARALLELIZATION} \
       commThread=yes \
       netcdf=yes \
       netcdfDir=${SPACK_INSTALL}/netcdf \
       compiler=${COMPILER_TYPE} \
       hdf5=${CK_SEISSOL_HDF5} \
       hdf5Dir=${SPACK_INSTALL}/hdf5

if [ "${?}" != "0" ] ; then
    echo "Error: compilation failed!"
    exit 1
fi

cp ${INSTALL_DIR}/src/src/version.h ${PREFIX}
if [ "${?}" != "0" ] ; then
    echo "Error: copy version.h failed!"
    exit 1
fi
