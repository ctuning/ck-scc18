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

#On Piz Daint unload this module to make spack work ...
#module unload PrgEnv-cray



echo "**************************************************************"
echo "Cloning spack ..."
echo ""

git clone https://github.com/LLNL/spack



echo "**************************************************************"
echo "Finding compilers ..."
echo ""

spack compiler find



echo "**************************************************************"

more spack/etc/spack/defaults/packages.yaml

echo ""
echo "Update 'compilers:' in spack/etc/spack/defaults/packages.yaml to select compiler"

read -p "Press enter to continue"

echo "**************************************************************"
echo "spack/bin/spack install openmpi@1.10.7 %gcc"
spack/bin/spack install openmpi@1.10.7 %gcc

if [ "${?}" != "0" ] ; then
    echo "Error: installation failed!"
    exit 1
fi

echo "**************************************************************"
echo "spack/bin/spack install netcdf@4.4.1 %gcc +mpi +dap -pic -shared ^openmpi@1.10.7 ^hdf5@1.10.4 +mpi +fortran -shared -pic"
spack/bin/spack install netcdf@4.4.1 %gcc +mpi +dap -pic -shared ^openmpi@1.10.7 ^hdf5@1.10.4 +mpi +fortran -shared -pic

if [ "${?}" != "0" ] ; then
    echo "Error: installation failed!"
    exit 1
fi
