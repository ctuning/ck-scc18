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

    f='stdout.log' # Output file without job logs

    env=d.get('env',{})
    job_id=d.get('job_id','')
    if job_id!='':
       jm=env.get('JOB_MANAGER','')
       if jm!='':
          if jm=='slurm':
             f='slurm-'+job_id+'.out'

    # Reading output
    if f!='':
       ck.out('Trying to read '+f+' ...')

       r=ck.load_text_file({'text_file':f})
       if r['return']>0: 
          if r['return']!=16: return r

          ck.out('')
          ck.out('The log file from the last job was not found - maybe this job did not start yet?!')

          return {'return':0}

       s=r['string']

       ck.out('')
       ck.out(s)

       # Validating output
       ck.out('***************************************************************************************')
       ck.out('TBD: validate output against authors results ...')

    # Finish
    rr['return']=0
    rr['new_env']=new_env
    return rr

# Do not add anything here!
