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




echo "**************************************************************"
echo "Obtaining EasyBuild ..."
echo ""

wget https://raw.githubusercontent.com/easybuilders/easybuild-framework/develop/easybuild/scripts/bootstrap_eb.py



echo "**************************************************************"
echo "Bootstrapping EasyBuild ..."
echo ""

export EASYBUILD_PREFIX=$PWD/install

python bootstrap_eb.py $EASYBUILD_PREFIX

if [ "${?}" != "0" ] ; then
    echo "Error: bootstrapping failed!"
    exit 1
fi



echo "**************************************************************"
echo "Configuring EasyBuild ..."
echo ""


export EASYBUILD_MODULES_TOOL=EnvironmentModulesC

module use $EASYBUILD_PREFIX/modules/all

module load EasyBuild
