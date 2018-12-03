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

cd ${INSTALL_DIR}/src/auto_tuning/proxy

git submodule update

PREFIX=${INSTALL_DIR}/install
mkdir -p $PREFIX

######################################################################################
# Print info about possible issues
echo ""
echo "Note that you sometimes need to upgrade your pip to the latest version"
echo "to avoid well-known issues with user/system space installation:"

SUDO="sudo "
if [[ ${CK_PYTHON_PIP_BIN_FULL} == /home/* ]] ; then
  SUDO=""
fi

######################################################################################
# Check if has --system option
${CK_ENV_COMPILER_PYTHON_FILE} -m pip install --help > tmp-pip-help.tmp
if grep -q "\-\-system" tmp-pip-help.tmp ; then
 SYS=" --system"
fi
rm -f tmp-pip-help.tmp

######################################################################################
echo "Downloading and installing Python deps ..."
echo ""

EXTRA_PYTHON_SITE=${INSTALL_DIR}/python-lib
rm -rf ${EXTRA_PYTHON_SITE}
mkdir -p ${EXTRA_PYTHON_SITE}

${CK_ENV_COMPILER_PYTHON_FILE} -m pip install --ignore-installed lxml scipy -t ${EXTRA_PYTHON_SITE}  ${SYS}
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
       order=6 compileMode=release \
       arch=${CK_SEISSOL_TARGET_ARCH} \
       memLayout=../config/dense.xml \
       numberOfMechanisms=1 \
       compiler=${COMPILER_TYPE}

if [ "${?}" != "0" ] ; then
    echo "Error: compilation failed!"
    exit 1
fi

mkdir ${PREFIX}/bin
cp -rf build/bin/* ${PREFIX}/bin/
if [ "${?}" != "0" ] ; then
    echo "Error: copy version.h failed!"
    exit 1
fi
