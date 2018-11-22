#
# Developers:
#   - Grigori Fursin, cTuning foundation / dividiti, 2018
#

import os
import sys

# *********************************************************************************
# Post-process function

def ck_postprocess(i):
    ck=i['ck_kernel']
    del i['ck_kernel']

    rt=i['run_time']
    deps=i['deps']
    pass_to_make = i
    pli = i['misc']

    env=i.get('env',{})
    new_env={} # generate new environment and pass to run scripts

    rr={}

    ck.out('***************************************************************************************')

    # Load last job info
    r=ck.load_json_file({'json_file':'tmp-last-run.json'})
    if r['return']>0: 
       if r['return']!=16: return r

       ck.out('Information about last job (tmp-last-run.json) was not found!')

       return {'return':0}

    d=r['dict']

    env=d.get('env',{})
    job_id=d.get('job_id','')
    if job_id!='':
       jm=env.get('JOB_MANAGER','')
       if jm!='':
          if jm=='slurm':
             f='slurm-'+job_id+'.out'

             ck.out('Checking status of a job '+job_id+' ...')
             ck.out('')

             r=ck.run_and_get_stdout({'cmd':'squeue', 'shell':'yes'})
             if r['return']>0: return r
             s=r['stdout'].split('\n')

             found=False
             for x in s:
                 if job_id in x:
                    ck.out(x)
                    found=True

             if not found:
                ck.out('JOB not found in the queue - likely completed - check logs!')

    # Finish
    rr['return']=0
    rr['new_env']=new_env
    return rr

# Do not add anything here!
