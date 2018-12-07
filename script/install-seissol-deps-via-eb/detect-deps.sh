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

module load EasyBuild

ck detect soft:compiler.gcc --extra_tags=veasybuild --extra_name="(easybuild)" --search_dir=${EASYBUILD_PREFIX}/software
