#
# Developers:
#   - Grigori Fursin, cTuning foundation / dividiti, 2018
#

import os
import sys

# Taken from https://dl.acm.org/citation.cfm?id=3126948 (See section A.5)
validation=[
  {"key":" Wall time", "value":"50007.9 seconds"},
  {"key":" Total   measured HW-GFLOP", "value":"4.68102e+10"},
  {"key":" Total calculated NZ-GFLOP", "value":"2.14946e+10"},
  {"key":" WP calculated HW-GFLOP", "value":"4.42614e+10"},
  {"key":" WP calculated NZ-GFLOP", "value":"1.9178e+10"},
  {"key":" DR calculated HW-GFLOP", "value":"2.54884e+09"},
  {"key":" DR calculated NZ-GFLOP", "value":"2.31664e+09"},
  {"key":" Time wave field writer backend", "value":"103.908"},
  {"key":" Time wave field writer frontend", "value":"0.222447"},
  {"key":" Time checkpoint frontend", "value":"0.922489"},
  {"key":" Time checkpoint backend", "value":"188.573"},
  {"key":" Time fault writer backend", "value":"59.5376"},
  {"key":" Time fault writer frontend", "value":"0.293896"},
  {"key":" Time free surface writer backend", "value":"99.9163"},
  {"key":" Time free surface writer frontend", "value":"0.136493"}
]

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
       ck.out('Validating output (beta functionality):')

       # Search if SeisSol completed
       j=s.find('SeisSol done. Goodbye.')
       if j<0:
          ck.out('')
          ck.out('SeisSol simulation did not complete ...')
       else:
          # Detect vars
          for x in validation:
              k=x['key']
              v=x['value']

              ck.out('')
              ck.out('* '+k+' :')

              j=s.find(k)
              if j>0:
                 j1=s.find(':',j)
                 if j1>0:
                    j2=s.find('\n',j1)
                    if j2>0:
                       vnew=s[j1+1:j2].strip()
                       j3=vnew.find('(')
                       if j3>0:
                          vnew=vnew[:j3]

                       ck.out("      Authors' value: "+v)
                       ck.out("           New value: "+vnew)

    # Finish
    rr['return']=0
    rr['new_env']=new_env
    return rr

# Do not add anything here!
