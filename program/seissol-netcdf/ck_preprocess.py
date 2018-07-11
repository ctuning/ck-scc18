#
# Convert raw output of the Caffe 'time' command
# to the CK timing format.
#
# Developers:
#   - Grigori Fursin, cTuning foundation / dividiti, 2016
#   - Anton Lokhmotov, dividiti, 2016-2017
#

import os
import sys

### copy linux directory 
import shutil, errno

def ck_preprocess(i):
    ck=i['ck_kernel']
    del i['ck_kernel']
    rt=i['run_time']
    deps=i['deps']
    env=i.get('env',{})
    pass_to_make = i
    pli = i['misc']
    rr={}

    # First copy dataset files to the current tmp dir
    dataset_path=deps['dataset-seissol']['dict']['env']['CK_ENV_DATASET_SEISSOL']
    cur_path=os.getcwd()

    ck.out('')
    ck.out('Copying dataset files to tmp directory - can take some time ...')
    ck.out('')
    for f in os.listdir(dataset_path):
        ck.out(' * '+f)

        f1=os.path.join(dataset_path,f)
        f2=os.path.join(cur_path,f)

        shutil.copy2(f1, f2)

    # Generate DGPATH
    maple_path=deps['lib-seissol']['dict']['env']['CK_ENV_LIB_SEISSOL_MAPLE']

    r=ck.save_text_file({'text_file':'DGPATH', 'string':maple_path+'\n'})
    if r['return']>0: return r

    rr['return']=0
    return rr

# Do not add anything here!
