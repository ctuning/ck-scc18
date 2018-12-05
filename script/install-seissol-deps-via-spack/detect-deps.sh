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

ck detect soft:lib.mpi --extra_tags=vspack --extra_name="(spack)" --search_dir=$PWD/spack/opt/spack

ck detect soft:lib.hdf5.static --extra_tags=vparallel,vmpi,vspack --extra_name="(spack)" --search_dir=$PWD/spack/opt/spack

ck detect soft:lib.netcdf --extra_tags=vspack --extra_name="(spack)" --search_dir=$PWD/spack/opt/spack
